<template>
  <div v-else>

    <form enctype="multipart/form-data" id="med_form" @submit.prevent="validateBeforeSubmit">
      <!--alerts BEGINS-->
      <div class="row">
        <div class=""></div>

        <b-alert class="col-12" variant="success" dismissible fade :show="showSuccess">
          <strong>Success!</strong> New Medication added.
        </b-alert>

        <b-alert class="col-12" variant="danger" dismissible fade :show="showDanger">
          <strong>Problem:</strong> Did you fill out all fields? Are you connected to the internet?
        </b-alert>

        <div class=""></div>
      </div>
      <!--alerts ENDS-->
      <div class="container-fluid">
        <div class="row">
          <div class="divTableCell col center">
            <div>
              <fg-input label="Add A Medication" id="newMedication">
                <div class="row">
                    <div class="col-sm-2"></div>
                    <div class="col-md-2">
                      <b-form-input onfocus="this.value=''"
                                          v-model="name" v-validate="'required'" placeholder="Name"></b-form-input>
                    </div>
                    <div class="col-md-2">
                      <b-form-input onfocus="this.value=''"
                                          v-model="manufacturer" v-validate="'required'" placeholder="Manufacturer"></b-form-input>
                    </div>
                    <div class="col-md-2">
                      <b-form-input onfocus="this.value=''"
                                          v-model="duration" v-validate="'required'" placeholder="Duration"></b-form-input>
                    </div>
                    <div class="col-md-2">
                      <b-form-input onfocus="this.value=''"
                                          v-model="frequency" v-validate="'required'" placeholder="Frequency"></b-form-input>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-2"></div>
                    <div class="col-sm-2">
                      <b-form-select v-model="dosage_unit" :options="dosage_options"></b-form-select>
                    </div>
                    <div class="col-sm-2">
                      <b-form-textarea onfocus="this.value=''"
                                          v-model="dosage_guidelines" v-validate="'required'" placeholder="Dosage Guidelines"
                                       :rows="3" :max-rows="6"></b-form-textarea>
                    </div>
                    <div class="col-sm-4">
                      <b-form-textarea onfocus="this.value=''"
                                          v-model="notes" v-validate="'required'" placeholder="Notes"
                                       :rows="3" :max-rows="6"></b-form-textarea>
                    </div>
                  </div>

              </fg-input>
            </div>
          </div>
        </div>
      </div>
      <div class="row align-center">
        <div class="col-sm-4"></div>
        <div class="col-sm-4 center">
          <!--photo upload-->
          <span v-if="window.width < 500">
            <input style="display: none" type="file" @change="onFileChanged1" ref="fileInput1">
            <button class="btn" @click="$refs.fileInput1.click()">Upload Image 1</button>
            <input style="display: none" type="file" @change="onFileChanged2" ref="fileInput2">
            <button class="btn" @click="$refs.fileInput2.click()">Upload Image 2</button>
            <input style="display: none" type="file" @change="onFileChanged3" ref="fileInput3">
            <button class="btn" @click="$refs.fileInput3.click()">Upload Image 3</button>
          </span>
          <span v-else>
            <input class="btn btn-primary" type="file" @change="onFileChanged1">
            <input class="btn btn-primary" type="file" @change="onFileChanged2">
            <input class="btn btn-primary" type="file" @change="onFileChanged3">
          </span>
        </div>
        <div class="col-4"></div>
      </div>
      <div class="col form-group container-fluid">
        <div class="d-flex justify-content-center row">
          <button :disabled="errors.any()"
                  type="submit"
                  name="cat-button"
                  value="button1"
                  class="btn btn-primary submit-button rectangle-79 save">Save</button>
          <button type="reset"
                  name="cat-exit"
                  value="button2"
                  class="btn btn-primary submit-button rectangle-79 exit" v-b-toggle.collapse3>Exit</button>
        </div>
      </div>
    </form>

  </div>
</template>

<script>
  import { DatePicker, TimeSelect, Slider, Tag, Input, Button, Select, Option } from 'element-ui'
  import axios from 'axios';
  import {Observable} from 'rxjs';
  import SecondStep from './Wizard/SecondStep.vue'
  import initialStateAddaCat from '../Tables/ExtendedTables';
  import showSwal from '../Tables/ExtendedTables';
  import {
    Progress as LProgress,
    Switch as LSwitch,
    Radio as LRadio,
    Checkbox as LCheckbox,
    FormGroupInput as FgInput
  } from '../../../components/index'


  export default {
    name: "AddMedication",
    data () {
      return {
        catType: '',
        name: '',
        notes:'',
        duration: '',
        manufacturer: '',
        frequency: '',
        dosage_unit: null,
        dosage_options: [
          {value: null, text: 'Dosage Unit'},
          {value:'ML', text:'Milliliters'},
          {value:'CC', text:'Cubic Centimeters'},
          {value:'OZ', text:'Ounces'},
          {value:'G', text:'Grams'},
        ],
        dosage_guidelines: '',
        package_photo_1: null,
        package_photo_2: null,
        package_photo_3: null,
        selectedFile: null,
        cats: [],
        singleCat: [],
        showSuccess: false,
        showDanger: false,
        showSuccess_litter: false,
        showDanger_litter: false,
        window: {
          width: 0,
          height: 0
        }
      }
    },
    methods: {
      handleResize() {
        this.window.width = window.innerWidth;
        this.window.height = window.innerHeight;
      },
      resetWindow (){
        this.$data = initialStateAddaCat();
      },
      onFileChanged1 (event) {
        this.package_photo_1 = event.target.files[0];
        // this.onUpload();
      },
      onFileChanged2 (event) {
        this.package_photo_2 = event.target.files[0];
        // this.onUpload();
      },
      onFileChanged3 (event) {
        this.package_photo_3 = event.target.files[0];
        // this.onUpload();
      },
      onUpload() {
        // upload file, get it from this.selectedFile
        const formData = new FormData();
        formData.append('name', this.name);
        formData.append('package_photo_1', this.package_photo_1, this.package_photo_1.name);
        formData.append('package_photo_2', this.package_photo_2, this.package_photo_2.name);
        formData.append('package_photo_3', this.package_photo_3, this.package_photo_3.name);
        axios.put(`/api/v1/medications/`,formData,{
          onUploadProgress: progressEvent => {
            console.log('Upload progress: ' + Math.round(progressEvent.loaded / progressEvent.total * 100) + '%')
          }
        })
          .then(response => {
            console.log(response.data.package_photo_1);
            response.status === 201 ? this.showSuccess = true : this.showDanger = true;
            this.singleCat = response.data;
          })
          .catch(error => {
            console.log(error);
            this.showDanger = true;
          })
      },
      onSubmitted() {
        let formData = new FormData();
        formData.append('name', this.name);
        formData.append('duration', this.duration);
        formData.append('manufacturer', this.manufacturer);
        formData.append('frequency', this.frequency);
        formData.append('dosage_unit', this.dosage_unit);
        formData.append('dosage_guidelines', this.dosage_guidelines);
        formData.append('notes', this.notes);
        formData.append('package_photo_1', this.package_photo_1, this.package_photo_1.name);
        formData.append('package_photo_2', this.package_photo_2, this.package_photo_2.name);
        formData.append('package_photo_3', this.package_photo_3, this.package_photo_3.name);
        axios.post(`/api/v1/medications/`, formData,{
          headers: {
            'Content-Type': 'multipart/form-data'
          },
        })
          .then(response => {
            console.log(response);
            response.status === 201 ? this.showSuccess = true : this.showDanger = true;

          })
          .catch(error => {
            console.log(error);
            this.showDanger = true;
          })
      },
      validateBeforeSubmit() {
        this.$validator.validateAll()
          .then((result) => { console.log(result);
            this.onSubmitted();
          }).catch(error => {
          console.log(error);
          this.showDanger = true;
        });
      },
      showModal () {
        this.$refs.myModalRef.show();
        this.cat_form = false;
      },
      hideModal () {
        this.$refs.myModalRef.hide();
      },
      hideMe () {
        document.getElementById("rectangle-255").click();
      },
      getError (fieldName) {
        return this.errors.first(fieldName)
      },
      validate () {
        return this.$validator.validateAll().then(res => {
          console.log("fuq");
          this.$emit('on-validated', res, this.model);
          return res
        })
      }
    },
    beforeMount() {
      this.getLitterNames()
    },
    created() {
      window.addEventListener('resize', this.handleResize)
      this.handleResize();
    },
    destroyed() {
      window.removeEventListener('resize', this.handleResize)
    },
    components: {
      SecondStep,
      FgInput,
      [DatePicker.name]: DatePicker,
      [TimeSelect.name]: TimeSelect,
      [Slider.name]: Slider,
      [Tag.name]: Tag,
      [Input.name]: Input,
      [Button.name]: Button,
      [Option.name]: Option,
      [Select.name]: Select,
      LSwitch,
      LProgress,
      LRadio,
      LCheckbox
      // 'b-modal': bModal,
      // 'b-container': bContainer,
      // 'b-alert': bAlert
    },
    directives: {
      // 'b-modal': bModalDirective
    },
  }
</script>

<style scoped>
  /*add-a-cat menu begins*/
  .bg-copy-10 {
    height: 17px;
    width: 59px;
    border: 1px solid #E7E7E9;
    border-radius: 4px;
    background-color: #FFFFFF;
    font-family: Roboto;
    font-size: 11px;
    line-height: 17px;
    text-align: center;
  }
  .date_picker {
    height: 17px;
    width: 84px;
  }
  .save-button{
    margin-right: 5px;
  }
  .exit-button{
    margin-left: 5px;
  }
  .rectangle-79 {
    height: 29px;
    width: 106px;
    border: 1px solid #979797;
    border-radius: 4px;
    background-color: #23CCEF;
  }
  .save{
    height: 29px;
    width: 94px;
    color: #4A4A4A;
    font-family: Roboto;
    font-size: 14px;
    font-weight: bold;
    line-height: 20px;
    text-align: center;
  }
  .exit{
    height: 29px;
    width: 94px;
    color: #4A4A4A;
    font-family: Roboto;
    font-size: 14px;
    font-weight: bold;
    line-height: 20px;
    text-align: center;
  }
  .el-picker-panel .el-date-picker {
    height: 64px;
    width: 99px;
  }
  .name{
    width: 59px;
  }
  .gender{
    width: 59px;
  }
  .litter_name{
    width: 122px;
  }
  .weight{
    width: 64px;
  }
  .unit{
    width: 53px;
  }
  /*add-a-cat menu ends*/
</style>
