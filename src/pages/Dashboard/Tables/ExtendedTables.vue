<template>
  <div>
    <!--NOTE: paginated table-->
    <card title="">
      <div>
        <div class="col-sm-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
          <!--NOTE search box-->
            <el-input type="search" class="col-12 col-sm-3 select-default mb-3"
                    style="width: 100px"
                    placeholder="Search"
                    v-model="searchQuery"
                    aria-controls="datatables"/>
          <!--NOTE: add-a-cat button-->
            <div class="btn-group-md" role="group">
              <button id="btnGroupDrop1" type="button" class="btn btn-info dropdown-toggle"
                      data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Add
              </button>
              <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                <a class="dropdown-item" href="#" id="rectangle-255" v-b-toggle.collapse1>Cat</a>
                <a class="dropdown-item" href="#" id="litter-close" v-b-toggle.collapse2>Litter</a>
                <a class="dropdown-item" href="#" id="medication-close" v-b-toggle.collapse3>Medication</a>
              </div>
            </div>
        </div>

        <b-collapse id="collapse1" class="mt-2">
          <b-card>
            <div class="col-sm-12 no-padding">
              <div class="divTable">
                <div class="divTableHeading">
                  <AddCat></AddCat>
                </div>
              </div>
            </div>
          </b-card>
        </b-collapse>
        <b-collapse id="collapse2" class="mt-2">
          <b-card>
            <div class="col-sm-12 no-padding">
              <div class="divTable">
                <div class="divTableHeading">
                  <AddLitter></AddLitter>
                </div>
              </div>
            </div>
          </b-card>
        </b-collapse>
        <b-collapse id="collapse3" class="mt-2">
          <b-card>
            <div class="col-sm-12 no-padding">
              <div class="divTable">
                <div class="divTableHeading">
                  <AddMedication></AddMedication>
                </div>
              </div>
            </div>
          </b-card>
        </b-collapse>

        <!--NOTE: cat table begins-->
        <div class="" @load="sortedCats">
          <b-table striped
                   show-empty
                   stacked="md"
                   style="width: 100%;"
                   :fields="tableColumns"
                   :items="queriedData"
                   :current-page="pagination.currentPage"
                   :per-page="pagination.perPage"
                   :filter="filter"
                   :sort-by.sync="sortBy"
                   :sort-desc.sync="sortDesc"
                   :sort-direction="sortDirection"
                   @filtered="onFiltered">
            <template slot="id" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                <div class="d-flex justify-content-start">
                  <div style="display: table-cell">{{ scope.item.age}}</div>
                  <div style="display: table-cell">-</div>
                  <div style="display: table-cell">{{ scope.item.weight }}</div>
                  <div style="display: table-cell">{{ scope.item.gender }}</div>
                  <div style="display: table-cell">{{ scope.item.catType }}</div>
                </div>
              </div>
            </template>
            <template slot="photo" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                <div class="img-container photo-thumb-sm" v-if="scope.item.photo !== null">
                  <img class="rounded-circle img-fluid" :src="'media/' + scope.item.photo" alt="thumb">
                </div>
                <div class="img-container photo-thumb-sm" v-else>
                  <img class="rounded-circle img-fluid" src="/static/img/cat_n_mouse.png" alt="bastet">
                </div>
              </div>
            </template>
            <template slot="name" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                {{ scope.item.name }}
              </div>
            </template>
            <template slot="gender" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                {{ scope.item.gender }}
              </div>
            </template>
            <template slot="birthday" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                {{ scope.value | moment("MM-DD-YYYY") }}
              </div>
            </template>
            <template slot="age" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                {{ scope.item.birthday | moment("from", "now", true) }}
              </div>
            </template>
            <template slot="catType" slot-scope="scope">
              <div class="hand" @click.stop="scope.toggleDetails" @click="getFeedings(scope.item.name),getMedications(scope.item.name)">
                {{ scope.item.catType }}
              </div>
            </template>
            <template slot="actions" slot-scope="scope">
              <div>
                <!--<a v-tooltip.top-center="'Like'" class="btn-info btn-simple btn-link"-->
                   <!--@click="handleLike(scope.$index, scope)">-->
                  <!--<i class="fa fa-heart"></i></a>-->
                <!--<a v-tooltip.top-center="'Edit'" class="btn-warning btn-simple btn-link"-->
                   <!--@click="handleEditCatList(scope.$index, scope)"><i-->
                  <!--class="fa fa-edit"></i></a>-->
                <a v-tooltip.top-center="'Delete'" class="btn-danger btn-simple btn-link"
                   @click="handleDelete(scope.$index, scope.item, 'catRow')"><i class="fa fa-times"></i></a>
              </div>
            </template>
            <template slot="row-details" slot-scope="scope">
              <div class="table-responsive">
                <div id="accordion">
                  <div class="card">
                    <div class="card-header">
                      <!--TODO: CAT big one begins here-->
                      <b-btn id="fedMed" class="col btn btn-link" v-b-toggle.collapse4>
                        <div class="container-fluid col-">
                          <div class="divTable">
                            <div class="d-flex justify-content-around primary-cat-row row" role="button">
                              <div class="col-auto img-container-lg photo-thumb-sm" v-if="scope.item.photo !== null">
                                <img :src="'media/' + scope.item.photo" alt="thumb" class="rounded-circle img-fluid">
                              </div>
                              <div class="col-auto img-container-lg photo-thumb-sm" v-else>
                                <img src="/static/img/cat_n_mouse.png" alt="default pic" class="rounded-circle img-fluid">
                              </div>
                              <div class="col-auto cat-name">
                                <h4 style="color: #000;text-transform: capitalize;">{{scope.item.name}}</h4>
                                <div class="col-" style="border: 0px solid darkgrey; display: table" >
                                  <div class="d-flex justify-content-center">
                                    <div class="table-striped" style="display: table-row">
                                      <div style="display: table-cell">{{scope.item.age}}</div>
                                      <div style="display: table-cell">-</div>
                                      <div style="display: table-cell">{{scope.item.weight}}</div>
                                      <div style="display: table-cell">{{scope.item.gender}}</div>
                                      <div style="display: table-cell">{{scope.item.catType}}</div>
                                    </div>
                                  </div>
                                </div>
                                <span v-if="scope.item.gender === 'M' " style="color: black;">Male</span>
                                <span v-if="scope.item.gender === 'F' " style="color: black;">Female</span>
                                <p style="color: black;">{{scope.item.birthday | moment("from", "now", true)}}</p>
                              </div>
                              <!--TODO sparkline chart goes here-->
                              <div class="col-sm-4 col-md-5">
                                <!--<div v-if="modals['custom']">-->
                                <GattoChart :message="scope.item.name"></GattoChart>
                                <!--</div>-->
                              </div>
                              <div class="col-auto cat-litter">
                                <div class="btn-group" v-if="scope.item.litter !== null">
                                  <button type="button" class="btn btn-warning btn-outline">Litter:</button>
                                  <button type="button" class="btn btn-warning btn-outline">
                                    {{scope.item.litter ? scope.item.litter : 'none'}}
                                  </button>
                                </div>
                                <div class="btn-group" v-else>
                                  <button type="button" class="btn btn-default btn-outline">Litter:</button>
                                  <button type="button" class="btn btn-default btn-outline">
                                    {{scope.item.litter ? scope.item.litter : 'none'}}
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </b-btn>
                      <!--TODO: CAT big one ends here-->
                    </div>
                    <!--TODO: Carelog rows START here-->
                    <b-collapse id="collapse4" class="collapse" visible>
                      <card>
                        <vue-tabs value="Description">
                          <v-tab title="Carelog">
                            <b-table striped
                                     bordered
                                     stacked="sm"
                                     hover :fields="careLogColumns" :items="catFeedings">
                              <template slot="medication" slot-scope="data">
                                {{data.value.name}}
                              </template>
                              <template slot="actions" slot-scope="scope">
                                  <!--<a v-tooltip.top-center="'Like'" class="btn-info btn-simple btn-link"-->
                                     <!--@click="handleLike(scope.$index, scope.index)"><i class="fa fa-heart"></i></a>-->
                                  <!--<a v-tooltip.top-center="'Edit'" class="btn-warning btn-simple btn-link"-->
                                     <!--@click="handleEditCatList(scope.$index, scope)"><i class="fa fa-edit"></i></a>-->
                                  <a v-tooltip.top-center="'Delete'" class="btn-danger btn-simple btn-link"
                                     @click="handleDelete(scope.$index, scope.item, 'carelogRow')"><i class="fa fa-times"></i></a>
                              </template>
                            </b-table>
                            <!--TODO: add a carelog-->

                            <form id="carelogAddForm">
                              <b-collapse id="collapseForm" class="mt-2">
                                <fg-input label="Create New Carelog"
                                          class="column-sizing">
                                  <div class="row">
                                    <div class="col-md-2">
                                      <b-form-select v-model="food_type" :options="foodOptions"></b-form-select>
                                    </div>
                                    <div class="col-md-2">
                                      <b-input v-model="amount_of_food_taken" placeholder="Amount food taken"></b-input>
                                    </div>
                                    <div class="col-md-2">
                                      <b-form-select v-model="stimulated" :options="stimulatedOps"></b-form-select>
                                    </div>
                                    <div class="col-md-2">
                                      <b-form-input v-model="weight_before_food" placeholder="Weight Before Food"></b-form-input>
                                    </div>
                                    <div class="col-md-2">
                                      <b-input v-model="weight_after_food" placeholder="Weight After Food"></b-input>
                                    </div>
                                    <div class="col-md-2">
                                      <b-form-select v-model="stimulationType" :options="stimulationTypeOps"></b-form-select>
                                    </div>
                                  </div>
                                  <div class="row">
                                    <div class="col-sm-2">
                                      <b-form-select v-model="medication">
                                        <option selected :value="null">Medication</option>
                                        <option :value=catMed.name v-for="catMed in catMedications">{{catMed.name}}</option>
                                      </b-form-select>
                                    </div>
                                    <div class="col-sm-2">
                                      <b-input v-model="medication_dosage_given" placeholder="Med. Dosage"></b-input>
                                    </div>
                                  </div>
                                </fg-input>
                              </b-collapse>
                              <div class="row">
                                <div class="col-sm-12">
                                <button class="btn btn-sm btn-info float-right" @click='showButton = !showButton' v-if="showButton" v-b-toggle.collapseForm>Add New Log</button>
                                <button type="reset" class="btn btn-sm btn-warning float-right" @click='showButton = !showButton' v-if="!showButton" v-b-toggle.collapseForm>Cancel</button>
                                <button type="submit" class="btn btn-sm btn-success float-right" v-if="food_type !== 'MN' && !showButton"
                                          v-on:click="validateSubmitNoMom(scope.item.id, scope.item.name, scope.item.slug)" @click='showButton = !showButton'>Submit</button>
                                <button type="submit" class="btn btn-sm btn-success float-right" v-if="food_type === 'MN' && !showButton"
                                          v-on:click="validateSubmitMom(scope.item.id, scope.item.name)">Submit mom</button>
                                </div>
                              </div>
                            </form>

                          </v-tab>
                        </vue-tabs>
                      </card>
                    </b-collapse>
                  </div>
                </div>
              </div>
            </template>
          </b-table>
        </div>
      </div>
      <div slot="footer" class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
        <div class="">
          <!--<p class="card-category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>-->
          <!--NOTE: pagination box begins-->
          <el-select
            class="select-default mb-3"
            style="width: 70px"
            v-model="pagination.perPage"
            placeholder="Per page">
            <el-option
              class="select-default"
              v-for="item in pagination.perPageOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>
        <l-pagination class="pagination-no-border"
                      v-model="pagination.currentPage"
                      :per-page="pagination.perPage"
                      :total="pagination.total">
        </l-pagination>
      </div>
      <!--TODO: cat Modal-->
      <el-dialog
        center
        title=""
        :visible.sync="modals.custom">
        <!--TODO: old modal contents where here-->
        <p>old modal contents where here</p>
      </el-dialog>
    </card>
  </div>
</template>
<script>
  import Vue from 'vue'
  import axios from 'axios';
  import swal from 'sweetalert2'
  import { Dialog, Table, TableColumn, Select, Option, Collapse, CollapseItem, Row, Aside, Main, Button, MessageBox} from 'element-ui'
  import {Pagination as LPagination} from '../../../components/index'
  import GattoChart from '../../../components/GattoChart'
  import GattoInfo from '../../../components/GattoInfo'
  import Fuse from 'fuse.js'
  import LSwitch from '../../../components/Switch.vue'
  import VueTabs from 'vue-nav-tabs'
  import Wizard from  '../Forms/Wizard'
  import AddCat from  '../Forms/AddCat'
  import AddLitter from  '../Forms/AddLitter'
  import AddMedication from  '../Forms/AddMedication'
  import ElSelectDropdown from "element-ui/packages/select/src/select-dropdown";

  Vue.use(VueTabs);
  Vue.prototype.$confirm = MessageBox.confirm;


  export default{
    components: {
      AddCat,
      AddLitter,
      AddMedication,
      GattoChart,
      GattoInfo,
      ElSelectDropdown,
      LSwitch,
      LPagination,
      [Dialog.name]: Dialog,
      [Button.name]: Button,
      [Select.name]: Select,
      [Option.name]: Option,
      [Table.name]: Table,
      [TableColumn.name]: TableColumn,
      [Collapse.name]: Collapse,
      [CollapseItem.name]: CollapseItem,
      [Row.name]: Row,
      [Aside.name]: Aside,
      [Main.name]: Main,
      Wizard,
      [AddCat.name]: AddCat,
    },
    computed: {
      pagedData () {
        return this.cats.slice(this.from, this.to)
      },
      /***
       * Searches through table data and returns a paginated array.
       * Note that this should not be used for table with a lot of data as it might be slow!
       * Do the search and the pagination on the server and display the data retrieved from server instead.
       * @returns {computed.pagedData}
       */
      queriedData () {
        let result = this.cats;
        if (this.searchQuery !== '') {
          result = this.fuseSearch.search(this.searchQuery);
          this.pagination.total = result.length
        }
        console.log(result.slice(this.from, this.to));
        return result.slice(this.from, this.to)
      },
      to () {
        let highBound = this.from + this.pagination.perPage;
        if (this.total < highBound) {
          highBound = this.total
        }
        return highBound
      },
      from () {
        return this.pagination.perPage * (this.pagination.currentPage - 1)
      },
      total () {
        this.pagination.total = this.cats.length;
        return this.cats.length
      },
      sortedCats: function() {
        function compare(a, b) {
          if (a.created < b.created)
            return -1;
          if (a.created > b.created)
            return 1;
          return 0;
        }
        return this.cats.sort(compare);
      },
      sortedCat() {
        return this.thisCat.sort((a,b) => {
          let modifier = 1;
          if(this.currentSortDir === 'desc') modifier = -1;
          if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
          return 0;
        });
      },
    },
    data () {
      return {
        modals: {
          basic: false,
          centered: false,
          custom: false,
          confirm: false
        },
        onFiltered: '',
        variableAtParent: 'DATA FROM PARENT!',
        activeName: 'first',
        currentSort:'name',
        currentSortDir:'asc',
        collapsed: true,
        medToEdit: [],
        feedToEdit: [],
        page: 1,
        CatIndex: 0,
        pagination: {
          perPage: 5,
          currentPage: 1,
          perPageOptions: [5, 10, 25, 50],
          total: 0
        },
        sortBy: null,
        sortDesc: false,
        sortDirection: 'asc',
        filter: null,
        searchQuery: '',
        propsToSearch: ['name', 'gender', 'age', 'id', 'birthday', 'catType'],
        cat: '',
        cat_type: '',
        example1: [],
        cats: [],
        thisCat: [],
        catFeedings: [],
        catMedications: [],
        careLogTableColumns: [],
        careLogColumns: [
          'foodType',
          'amountOfFoodTaken',
          'stimulated',
          'weightBeforeFood',
          'weightAfterFood',
          'stimulationType',
          'medication',
          'medicationDosageGiven',
          'actions',
        ],
        tableColumns: [
          {
            key: 'id',
            prop: 'id',
            label: 'ID',
            minWidth: 90
          },
          {
            key: 'photo',
            prop: 'photo',
            label: 'Photo',
            minWidth: 100
          },
          {
            key: 'name',
            prop: 'name',
            label: 'Name',
            minWidth: 100,
            sortable: true
          },
          {
            key: 'gender',
            prop: 'gender',
            label: 'Sex',
            minWidth: 50,
            sortable: true
          },
          {
            key: 'birthday',
            prop: 'birthday',
            label: 'Birthdate',
            minWidth: 140,
            sortable: true
          },
          {
            key: 'age',
            prop: 'birthday',
            label: 'Age',
            minWidth: 100,
            sortable: false
          },
          {
            key: 'catType',
            prop: 'catType',
            label: 'Type',
            minWidth: 60,
            sortable: true
          },
          {
            key: 'actions',
            prop: 'actions',
            label: 'Actions',
            minWidth: 60
          },
        ],
        fuseSearch: null,
        weight_before_food: '',
        weight_after_food: '',
        amount_of_food_taken: '',
        food_type: null,
        notes:    '',
        stimulated: null,
        stimulatedOps: [
          { value: null, text: 'Stimulated' },
          'true',
          'false'
        ],
        stimulationType: null,
        stimulationTypeOps: [
          { value: null, text: 'Stim. Type' },
          { value: 'UR', text: 'Urine'},
          { value: 'FE', text: 'feces'},
          { value: 'UF', text: 'Urine / Feces'},
        ],
        showSuccess: false,
        showDanger: false,
        constant: 0,
        dismissSecs: 4,
        dismissCountDown: 0,
        dismissCountDown2: 0,
        nursing: false,
        handleAdd: true,
        showRow: true,
        showButton: true,
        showButton2: true,
        dosage_unit: 'ML',
        dosage:    '',
        dosageGuidelines: '',
        weightBeforeFood: '',
        amountOfFoodTaken: '',
        foodType: '',
        medication: null,
        duration: '',
        frequency: '',
        name:   '',
        medication_dosage_given: '',
        foodOptions:[
          { value: null, text: 'Food Type' },
          { value: 'MN', text: 'Mom (Nursing)' },
          { value: 'BO', text: 'Bottle' },
          { value: 'BS', text: 'Bottle/Syringe' },
          { value: 'SG', text: 'Syringe Gruel'},
          { value: 'GG', text: 'Syringe Gruel / Gruel'},
          { value: 'G', text: 'Gruel'},
        ],

      }
    },
    beforeMount () {
      this.getCats();
      console.log("beforeMount: " + this.cats);
    },
    created () {
      console.log("created: " + this.cats);
    },
    mounted () {
      console.log("mounted: " + this.cats);
    },
    events: {
      'event_name': function (data) {
        this.$broadcast('event_name', data);
      },
    },
    methods: {
      updateSearch(){
        axios.get(`/api/v1/cats/`)
          .then((response) => {
            console.log("update-before: "+ this.cats);
            this.cats = response.data.results;
            console.log("update-after: "+ this.cats);
            this.fuseSearch = new Fuse(this.cats, {keys: ['name', 'gender']})
          })
          .catch(error => console.log(error));
      },
      foodName(food){
        console.log(food);
        switch (food){
          case "MN":{
            console.log("Mom");
            return "Mom";
            break;
          }
          case "G":{
            return "Gruel";
            break;
          }
          case "GG":{
            return "Syringe Gruel / Gruel";
            break;
          }
          case "SG":{
            return "Syringe Gruel";
            break;
          }
          case "BS":{
            return "Bottle/Syringe";
            break;
          }
          case "BO":{
            return "Bottle";
            break;
          }
        }
      },
      sort(s) {
        //if s == current sort, reverse
        if(s === this.currentSort) {
          this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
        }
        this.currentSort = s;
      },
      openModal (name) {
        this.modals[name] = true;
      },
      closeModal (name) {
        this.modals[name] = false
      },
      async handleClose (done) {
        try {
          await this.$confirm('Are you sure you want to close this dialog?');
          done()
        } catch (e) {}
      },
      showSwal (type, message) {
        if (type === 'basic') {
          swal({
            title: message,
            buttonsStyling: false,
            confirmButtonClass: 'btn btn-success btn-fill'
          })
        } else if (type === 'title-and-text') {
          swal({
            title: `Here's a message!`,
            text: `It's pretty, isn't it?`,
            buttonsStyling: false,
            confirmButtonClass: 'btn btn-info btn-fill'
          })
        } else if (type === 'success-message') {
          swal({
            title: `Good job!`,
            text: message,
            buttonsStyling: false,
            confirmButtonClass: 'btn btn-success btn-fill',
            type: 'success'
          })
        } else if (type === 'warning-message-and-confirmation') {
          swal({
            title: 'Are you sure?',
            text: `You won't be able to revert this!`,
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success btn-fill',
            cancelButtonClass: 'btn btn-danger btn-fill',
            confirmButtonText: 'Yes, delete it!',
            buttonsStyling: false
          }).then(function () {
            swal({
              title: 'Deleted!',
              text: 'Your file has been deleted.',
              type: 'success',
              confirmButtonClass: 'btn btn-success btn-fill',
              buttonsStyling: false
            })
          })
        } else if (type === 'warning-message-and-cancel') {
          swal({
            title: 'Are you sure?',
            text: 'You will not be able to recover this imaginary file!',
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, keep it',
            confirmButtonClass: 'btn btn-success btn-fill',
            cancelButtonClass: 'btn btn-danger btn-fill',
            buttonsStyling: false
          }).then(function () {
            swal({
              title: 'Deleted!',
              text: 'Your cat record has been deleted.',
              type: 'success',
              confirmButtonClass: 'btn btn-success btn-fill',
              buttonsStyling: false
            })
          }, function (dismiss) {
            // dismiss can be 'overlay', 'cancel', 'close', 'esc', 'timer'
            if (dismiss === 'cancel') {
              swal({
                title: 'Cancelled',
                text: 'Your cat record is safe :)',
                type: 'error',
                confirmButtonClass: 'btn btn-info btn-fill',
                buttonsStyling: false
              })
            }
          })
        } else if (type === 'custom-html') {
          swal({
            title: 'HTML example',
            buttonsStyling: false,
            confirmButtonClass: 'btn btn-success btn-fill',
            html: 'You can use <b>bold text</b>, ' +
            '<a href="http://github.com">links</a> ' +
            'and other HTML tags'
          })
        } else if (type === 'auto-close') {
          swal({
            title: message,
            text: 'I will close in 2 seconds.',
            timer: 2000,
            showConfirmButton: false
          })
        } else if (type === 'input-field') {
          swal({
            title: 'Input something',
            html: '<div class="form-group">' +
            '<input id="input-field" type="text" class="form-control" />' +
            '</div>',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success btn-fill',
            cancelButtonClass: 'btn btn-danger btn-fill',
            buttonsStyling: false
          }).then(function (result) {
            swal({
              type: 'success',
              html: 'You entered',
              confirmButtonClass: 'btn btn-success btn-fill',
              buttonsStyling: false

            })
          }).catch(swal.noop)
        }
      },
      getError (fieldName) {
        return this.errors.first(fieldName)
      },
      getOneCat (catID) {
        axios.get(`/api/v1/cats/${catID}/`)
          .then(response => {
            // console.log(response.data);
            this.cat = response.data;
            this.openModal('custom');
            this.getMedications(this.cat.name);
            this.getFeedings(this.cat.name);
          })
          .catch(error => console.log(error));
      },
      openCat (index, row) {
        this.getOneCat(row.id)
      },
      getCats () {
        axios.post('http://localhost:8000/graphql', {
          query: `{
              allCats {
              weight
              name
              slug
              id
              photo
              birthday
              gender
              catType
              litter{
                id
                name
              }
              carelogSet{
                id
                foodType
                amountOfFoodTaken
                stimulated
                weightBeforeFood
                weightAfterFood
                stimulated
                stimulationType
                medicationDosageGiven
                medication{
                  id
                  name
                  slug
                  duration
                  frequency
                  dosageGuidelines
                  notes
                }
              }
            }
          }`
        }).then((result) => {
          this.cats = result.data.data.allCats;
          this.fuseSearch = new Fuse(this.cats, {keys: ['name', 'gender']})
        })
          .catch(error => console.log(error));
      },
      deleteCat (catID) {
        axios.delete(`/api/v1/cats/${catID}/`)
          .then(response => {
            console.log("un Gatto gone:");
            this.showSwal('basic','un gatto gone');
            // this.cat = response.data.results // NOTE: this line caused pagination on catlist page to hault when deleting a cat
            this.updateSearch();
          })
          .catch(error => console.log(error));
      },
      deleteFeeding (slug) {
        axios.delete(`/api/v1/carelogs/${slug}/`)
          .then(response => {console.log("carelog gone:"); console.log(response);})
          .catch(error => console.log(error));
      },
      getFeedings(value) {
        axios.post('http://localhost:8000/graphql', {
          query:`{
            cat(name: "${value}"){
              id
              slug
              name
              carelogSet{
                slug
                id
                foodType
                amountOfFoodTaken
                stimulated
                weightBeforeFood
                weightAfterFood
                stimulated
                stimulationType
                medication{
                  name
                }
                medicationDosageGiven
              }
            }
          }`
        }).then(response => {console.log("Carelogs: ");
          console.log(response.data.data.cat.carelogSet);
          this.catFeedings = response.data.data.cat.carelogSet;
          this.careLogTableColumns = Object.keys(this.catFeedings[0]);
          console.log(this.careLogTableColumns);
        })
          .catch(error => console.log(error));
      },
      postFeedings(catID, catName) {
        axios.post(`/api/v1/carelogs/`,{
          cat: {id: catID, name: catName},
          weight_unit_measure: 'G',
          weight_before_food: this.weight_before_food,
          food_unit_measure: 'G',
          amount_of_food_taken: this.amount_of_food_taken,
          food_type: this.food_type,
          weight_after_food: this.weight_after_food,
          stimulated: this.stimulated,
          stimulation_type: this.stimulationType,
          medication: {name: this.medication, duration: this.duration, frequency: this.medication_dosage_given, dosage: this.dosage, notes: this.notes},
          medication_dosage_unit: 'ML',
          medication_dosage_given: this.medication_dosage_given,
          notes: this.notes
        })
          .then(response => {
            console.log(response);
            response.status === 201 ? this.showSwal('success-message','Carelog added') : null;
            this.getFeedings(catName);
          })
          .catch(error => {
            console.log(catID, catName);
            console.log(error);
            this.showSwal('auto-close', error);
          })
      },
      postFeedingsMom(catID, catName) {
        axios.post(`/api/v1/carelogs/`,{
          cat: {id: catID, name: catName},
          weight_unit_measure: 'G',
          weight_before_food: '0',
          food_unit_measure: 'G',
          amount_of_food_taken: '0',
          food_type: this.food_type,
          weight_after_food: this.weight_after_food,
          stimulated: false,
          stimulation_type: 'NA',
          notes: 'kitten',
        })
          .then(response => {
            console.log(response);
            response.status === 201 ? console.log("success") : console.log("fail");
            this.getFeedings(catName);
          })
          .catch(error => {
            console.log(error);
            this.dismissCountDown = true;
            console.log("fail");
          })
      },
      getMedications(value) {
        axios.post('http://localhost:8000/graphql', {
          query:`{
            allMedications{
              name
            }
          }`
        }).then(response => {console.log("getMedications: ");
          console.log(response.data.data.allMedications);
          this.catMedications = response.data.data.allMedications})
          .catch(error => console.log(error));
      },
      addCarelogs(catID, catName){
        axios.post(`/api/v1/carelogs/`,{
          cat: {id: catID, name: catName, slug: catName},
          medication: {name: this.name, duration: this.duration, frequency: this.frequency, dosage: this.dosage, notes: this.notes},
          medication_dosage_unit: 'ML',
          medication_dosage_given: this.dosage,
          notes: this.notes
        })
          .then(response => {
            console.log(response);console.log(this.showButton);
            this.showButton = true;
            response.status === 201 ? this.showSwal('success-message','CareLog Medication added') : console.log(response);
            this.getMedications(catName);
          })
          .catch(error => {
            console.log(error);
            this.showSwal('auto-close', error);
          })
      },
      editFeedings(medID, medName, catID, catName) {
        // TODO: PUT and PATCH will not work...something is wrong on millers code
        axios.patch(`/api/v1/carelogs/${medID}/`,{
          cat: {id: catID, name: catName},
          weight_unit_measure: 'G',
          weight_before_food: this.weight_before_food,
          food_unit_measure: 'G',
          amount_of_food_taken: this.amount_of_food_taken,
          food_type: this.food_type,
          weight_after_food: this.weight_after_food,
          stimulated: this.stimulated,
          stimulation_type: this.stimulation_type,
          notes: this.notes,
        })
          .then(response => {
            console.log(response); console.log(medID, medName, catID, catName);
            response.status === 201 ? console.log("error") : this.showSwal('success-message');
          })
          .catch(error => {
            console.log(error);
          })
      },
      feedingsBeforeSubmit(medID, medName, catID, catName) {
        this.$validator.validateAll().then((result) => {
          if (result) {
            this.postFeedings(catID, catName);
          }else{console.log('it blew up: ');}
        });
      },
      validateSubmitNoMom(catID, catName, catSlug) {
        this.$validator.validateAll()
          .then((result) => {
            this.postFeedings(catID, catName, catSlug);
            console.log(catSlug);
            console.log("validatedNoMom: ");
            console.log(result);
          })
          .catch(error => {
            console.log('it blew up 1: ');
            console.log(error);
        })
      },
      validateSubmitMom(catID, catName) {
        this.$validator.validateAll()
          .then((result) => {
            this.postFeedingsMom(catID, catName);
            console.log("validatedNoMom: ")
            ;console.log(result);
          })
          .catch(error => {
            console.log('it blew up 1: ');
            console.log(error);
          })
      },
      updateDeleteMedsSubmit(medID, medName, catID, catName) {
        this.$validator.validateAll().then((result) => {
          if (result) {
            // this.addMedications(catID, catName);
            this.editMedications(medID, medName, catID, catName);
            console.log("ping");console.log(catID, catName);
          }else{console.log('it blew up: ');}
        });
      },
      updateDeleteFeedsSubmit(fedID, fedName, catID, catName) {
        this.$validator.validateAll().then((result) => {
          if (result) {
            this.editFeedings(fedID, fedName, catID, catName);
            console.log("updateDeleteFeedsSubmit: ");console.log(catID, catName);
          }else{console.log('it blew up: ');}
        });
      },
      validateMedicationsBeforeSubmit(catID, catName) {
        this.$validator.validateAll()
          .then((result) => {
            this.addCarelogs(catID, catName);
            // this.addMedications(catID, catName);
            // this.editMedications(medID, medName, catID, catName);
            console.log("validatedMedications: ");console.log(result);
          })
          .catch(error => {
            console.log('it blew up: ');
            console.log(error);
          });
      },
      handleLike (index, row) {
        alert(`You want to like ${row.name}`)
        // this.showSwal.title(`You want to like ${row.name}`)
      },
      changeHandleAdd(value){
        this.handleAdd = value;
        console.log("changeHandleAdd called 1: ")
      },
      handleEdit (bool) {
        // map / filter / reduce
        // alert(`You want to edit ${row.name}`)
        this.showRow = bool;
        console.log(this.showRow);
      },
      handleEditCatList (index, row) {
        // map / filter / reduce
        alert(`You want to edit ${row.name}`)
        this.showRow = bool;
        console.log(this.showRow);
      },
      medEdit (medID, bool) {
        // map / filter / reduce
        this.showRow = bool;
        this.medToEdit = this.catMedications.filter(function(medToChange){
          return medToChange.id == medID;
        });
      },
      feedEdit (fedID, bool) {
        // map / filter / reduce
        this.showRow = bool;
        this.feedToEdit = this.catFeedings.filter(function(fedToChange){
          return fedToChange.id == medID;
        });
      },
      handleDelete (id, propRow, row, slug) {
        console.log(propRow);
        // this.showSwal('basic', `You want to delete ${name}`);
        if (row === 'catRow'){
          console.log("propRow " + propRow.slug);
          this.deleteCat(propRow.slug);//delete cat from database
          let indexToDelete = this.cats.findIndex((tableRow) => tableRow.id === propRow.id);
          if (indexToDelete >= 0) {
            this.cats.splice(indexToDelete, 1) // remove it from array visually
          }
        }else if (row === 'carelogRow'){
          console.log("carelogRow " + propRow.slug);
         this.deleteFeeding(propRow.slug);//delete cat from database
          this.showSwal('basic', 'carelog deleted');
          let indexToDelete = this.catFeedings.findIndex((tableRow) => tableRow.id === propRow.id);
          console.log(indexToDelete);
          if (indexToDelete >= 0) {
            this.catFeedings.splice(indexToDelete, 1) // remove it from array visually
          }
        }else if (row === 'medicationRow'){
          this.showSwal('basic', 'medication removed');
          let i = this.catMedications.map(item => item.id).indexOf(id); // find index of your object
          this.catMedications.splice(i, 1) // remove it from array visually
        }
      },
      getSummaries (param) {
        const { columns } = param
        const sums = []
        columns.forEach((column, index) => {
          if (index === 0) {
            sums[index] = 'Total'
          } else if (index < columns.length - 1) {
            sums[index] = ''
          } else {
            let sum = 0
            this.productsTable.forEach((obj) => {
              sum += obj.quantity * obj.price
            })
            sums[index] = `€ ${sum}`
          }
        })
        return sums
      },
      tableRowClassName (row, index) {
        if (index === 0) {
          return 'success'
        } else if (index === 2) {
          return 'info'
        } else if (index === 4) {
          return 'danger'
        } else if (index === 6) {
          return 'warning'
        }
        return ''
      },
      fivePercenter(){
        let percent_wbf = document.getElementById("weight_before_food").value * 0.05;
        let wbf = Number(document.getElementById("weight_before_food").value);
        console.log(typeof percent_wbf);
        console.log(typeof wbf);
        document.getElementById("target_weight_after_food").innerHTML = wbf + percent_wbf;
      },
      checkFoodType(food_type_taken){
        if (this.stimulated === "false"){
          if (food_type_taken === "BO" || food_type_taken === "BS") {
            // TODO: turn these two alerts into modals?
            this.showSwal('basic','You selected Bottle or Bottle-Syringe: Did you forget to stimulate the kitten?');
          }
        }else{
          if (food_type_taken === "SG" || food_type_taken === "GG" || food_type_taken === "G") {
            this.showSwal('basic','You selected Syringe Gruel, Gruel or Both: Was the kitten stimulated');
          }
        }
      },
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.dispose();
      }
    }
  }
  export function initialStateAddaCat (){
    return {
      profilePic: false,
      name: '',
      gender: '',
      age: '',
      cat_type: '',
      catType: '',
      litter: [],
      litter_mates: null,
      litter_name: '',
      pickerOptions1: {
        shortcuts: [{
          text: 'Today',
          onClick (picker) {
            picker.$emit('pick', new Date())
          }
        },
          {
            text: 'Yesterday',
            onClick (picker) {
              const date = new Date()
              date.setTime(date.getTime() - 3600 * 1000 * 24)
              picker.$emit('pick', date)
            }
          },
          {
            text: 'A week ago',
            onClick (picker) {
              const date = new Date()
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', date)
            }
          }]
      },
      datePicker: '',
      options: {
        format: 'DD/MM/YYYY',
        useCurrent: false,
      },
      dateTimePicker: '',
      mom_cat: '',
      female: false,
      addKittens: false,
      cat_form: true,
      selectedFile: null,
      singleCat: [],
      photo: '',
      showSuccess: false,
      showDanger: false,
      showSuccess_litter: false,
      showDanger_litter: false,
      weight: '',
      weight_unit: '',
      birthday: '',
    }
  }
</script>

<style lang="scss">
  #fedmed{
    width: 100%;
  }
  .el-table th > .cell {
    text-align: center;
  }
  /*Add-a-Cat button begins*/
  .rectangle-255 {
    height: 55px;
    width: 62px;
    border: 1px solid #9B9B9B;
    border-radius: 6px;
    background-color: #FF00FF;
  }
  .a-cat-text {
    height: 20px;
    width: 58px;
    color: black;
    font-family: Roboto;
    font-size: 14px;
    font-weight: 300;
    letter-spacing: -0.9px;
    line-height: 17px;
    text-align: center;
  }
  /*Add-a-Cat button ends*/
  .el-dialog {
    width: 75%;
  }
  @media (max-width: 800px){
    .el-dialog{
      width: 90%
    }
  }
  .table-bigboy .img-container img {
    width:90%;
    @media screen and (min-width: 200px){
        width:90%;
    }
    @media screen and (min-width: 1480px){
        width:50%;
    }
  }
  .table-bigboy .img-container img {
    object-fit: cover;
  }
  #chartdiv {
    width: 30%;
    height: 210px;
  }
  .fedRow{
    border-bottom: 1px solid #D4D4D4;
  }
  .fedRow div{
    padding: 0;
    margin: 0;
    border-left: 1px solid #D4D4D4;
  }
  .fed-submit-buttons button{
    margin-top: 5px;
    margin-left: 6px;
  }
  #feedtable:nth-child(even){
    background-color: #F2F2F2;;
  }
  #feedtable button{
    margin-right: 5px;
  }
  #medtable:nth-child(even){
    background-color: #F2F2F2;;
  }
  #medtable button{
    margin-right: 5px;
  }
  .fedRow{
    border-bottom: 1px solid #D4D4D4;
  }
  .fedRow div{
    padding: 0;
    margin: 0;
    border-left: 1px solid #D4D4D4;
  }
  .medRow{
    border-bottom: 1px solid #D4D4D4;
  }
  .medRow div{
    padding: 0;
    margin: 0;
    border-left: 1px solid #D4D4D4;
  }
  .top-row div{
    font-size: 12px;
    text-transform: uppercase;
    color: #9A9A9A;
    font-weight: 400;
    padding-bottom: 5px;
  }
  .cancel-submit button{
    /*padding-right: 15px;*/
    display: block;
  }
  .el-collapse-item__header{
    border-bottom: none;
  }
  .photo-thumb img{
    width: 8.333em;
    height: 8.333em;
    object-fit: cover;
    @media screen and (max-width: 667px) {
      width: 4.167em;
      height: 4.167em;
      object-fit: cover;
    }

  }
  .photo-thumb-sm img{
    width: 4.167em;
    height: 4.167em;
    object-fit: cover;
  }
  // css transition for tabs
  .vue-tabs .tab-content {
    padding-top: 10px;
    min-height: 100px;
    display: block !important;
    .tab-container {
      display: block;
      animation: fadeIn 0.5s;
    }
  }
  .TableRow{
    display: inline-flex;
  }
  .cat-name{
    text-align: center;
  }
  .cat-actions{
    z-index: 2;
    transform-style: preserve-3d;
  }
  .primary-cat-row{
    z-index: 1;
  }
  .hand{
    cursor: pointer;
  }
  .fadecontent{
    opacity: 1;
  }
  .fade1-enter,.fade2-enter,.fade3-enter{
    transform: translateX(20px);
    opacity: 0;
  }
  .fade1-enter-active{
    transition: all 1s ease;
  }
  .fade2-enter-active{
    transition: all 1s ease 0.5s;
  }
  .fade3-enter-active{
    transition: all 1s ease 1s;
  }

  .fade1-leave-active,.fade2-leave-active,.fade3-leave-active{
    opacity: 0;
    transform: translateX(20px);
  }
  .fade1-leave-active{
    transition: all 1s ease;
  }
  .fade2-leave-active{
    transition: all 1s ease 1s;
  }
  .fade3-leave-active{
    transition: all 1s ease 2s;
  }
  #thead th {
    color: black;
  }
  .grey{
    color: grey;
  }
  .heading-row{
    padding-bottom: 7rem;
  }
  .page-heading {
    color: white;
    font-family: "Helvetica Neue";
    font-size: 48px;
    font-weight: bold;
    line-height: 58px;
    margin-bottom: 25px;
  }
  .page-heading > span{
    color: darkgrey;
  }
  .meds-table {
    padding: 3rem 1.5rem;
    text-align: left;
  }
  #feeding-select{
    left: 0px;
    top: 0px;
    text-align: left;
  }
  #feeding-select label{
    float: left;
    margin: 1px;
  }
  #lastup-date{

  }
  #lastup-time{

  }

  /* Div Table */
  .divTable{
    display: table;
    width: 100%;
  }
  .divTableRow {
    /*display: table-row;*/
    border-top: 1px solid #dee2e6;
  }
  .divTableBody .divTableRow:hover{
    background-color: #EEE;
  }
  .center {
    text-align: center;
  }
  .hand{
    cursor: pointer;
  }
  .divTableHeading {
    /*background-color: #EEE;*/
    display: table-header-group;
    font-weight: bold;
    font-size: small;
  }
  .divTableHead {
    width: max-content;
    display: inline-block;
    padding: 0.75rem;
    vertical-align: top;
    /*border-top: 1px solid #dee2e6;*/
  }
  .divTableCell {
    display: inline-block;
    vertical-align: center;
    padding: 0.75rem;
    /*border-top: 1px solid #dee2e6;*/
  }
  .divTableCell img{
    display: block;
    margin: auto;
  }
  .divTableFoot {
    background-color: #EEE;
    display: table-footer-group;
    font-weight: bold;
  }
  .divTableBody {
    display: table-row-group;
  }
  .birthday{
    padding-top: 11px !important;
  }
  .swal2-container{
    z-index: 9000 !important;
  }
  .card .table tbody td:last-child, .card .table thead th:last-child {
    padding-right: 15px;
    display: table-cell;
  }
  .form-control{
    font-size: 0.8rem !important;
  }
</style>
