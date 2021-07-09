<template>
  <div v-if="profilePic">
    <second-step v-show="profilePic"></second-step>
  </div>
  <div v-else>

    <form id="litter_form" @submit.prevent="validateBeforeSubmitLitter">
      <!--alerts BEGINS-->
      <div class="row">
        <div class=""></div>

        <b-alert class="col-12" variant="success" dismissible fade :show="showSuccess_litter">
          <strong>Success!</strong> New Litter added.
        </b-alert>

        <b-alert class="col-12" variant="danger" dismissible fade :show="showDanger_litter">
          <strong>Problem:</strong> Did you fill out all fields? Are you connected to the internet?
        </b-alert>

        <div class=""></div>
      </div>
      <!--alerts ENDS-->
      <div class="container-fluid">
        <div class="row">
          <div class="col center">
            <div>
              <fg-input label="Create New Litter" id="newLitter">
                <div class="row">
                  <div class="col-md-4"></div>
                  <div class="col-md-2">
                    <b-form-input onfocus="this.value=''"
                                  v-model="name" v-validate="'required'" placeholder="name"></b-form-input>
                  </div>
                  <div class="col-md-2">
                    <b-form-textarea onfocus="this.value=''"
                                  v-model="notes" v-validate="'required'" placeholder="Enter cat notes"
                                     :rows="3" :max-rows="6"></b-form-textarea>
                  </div>
                  <div class="col-md-4"></div>
                </div>
              </fg-input>
            </div>
            <small v-show="errors.has('name')"
                   class="help is-danger form-text">{{ errors.first('name') }}
            </small>
          </div>
        </div>
      </div>
      <div class="col form-group container-fluid">
            <div class="d-flex justify-content-center row">
              <button :disabled="errors.any()"
                      type="submit"
                      name="cat-button"
                      value="button1"
                      class="btn btn-primary submit-button save-button rectangle-79 save">Save</button>
              <button type="reset"
                      name="cat-exit"
                      value="button2"
                      class="btn btn-primary submit-button exit-button rectangle-79 exit" v-b-toggle.collapse2>Exit</button>
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
    name: "AddLitter",
    data () {
      return {
        catType: '',
        name: '',
        notes:'',
        cats: [],
        singleCat: [],
        showSuccess: false,
        showDanger: false,
        showSuccess_litter: false,
        showDanger_litter: false,
      }
    },
    methods: {
      resetWindow (){
        this.$data = initialStateAddaCat();
      },
      onSubmitted() {
        axios.post(`/api/v1/litter/`, {
          name: this.name,
          notes: this.notes,
          litter_mates: this.litter_mates,
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
      onSubmittedLitter() {
        axios.post(`/api/v1/litter/`, {
          name: this.name,
          notes: this.notes,
        })
          .then(response => {
            console.log(response);
            response.status === 201 ? this.showSuccess_litter = true : this.showDanger_litter = true;
          })
          .catch(error => {
            console.log(error);
            this.showDanger_litter = true;
          })
      },
      validateBeforeSubmitLitter() {
        this.$validator.validateAll().then((result) => {
          if (result) {
            this.onSubmittedLitter();
          } else {
            // this.showDanger = true;
          }
        });
      },
      getLitterNames() {
        axios.get(`/api/v1/litter/`)
          .then(request => {
            console.log("litter_value: ");
            this.litter = request.data.results;
            console.log(this.litter);
          })
          .catch(error => console.log(error));
      },
      getLitterNamesObserv() {
        const litter$ = Observable.from(axios.get(`/api/v1/litter/`)
          .catch(error => console.log(error)))
          .pluck("data", "results");
        console.log(litter$);
        return {litter: litter$}
      },
      showModal () {
        this.$refs.myModalRef.show();
        this.litter_form = false;
      },
      hideModal () {
        this.$refs.myModalRef.hide();
      },
      hideMe (value) {
        document.getElementById("litter-close").click();
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
      LCheckbox,
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
