<template>
  <!-- second chart group -->
  <div class="chart-block container-fluid">
    <div class="row">
      <div ref="line"></div>
      <div ref="column"></div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    props: ['message'],
    name: 'app',
    created(){
      this.getFeedingsAgain(this.message);
      this.getMedicationsAgain(this.message);
    },
    updated(){
      this.getFeedingsAgain(this.message);
      this.getMedicationsAgain(this.message);
    },
    data() {
      return {
        chartCatID: this.message,
        catFeedingsAgain: [],
        catMedicationsAgain: [],
      }
    },
    watch: {
      catFeedingsAgain: function() {
        AmCharts.makeChart( this.$refs.line, {
          "type": "serial",
          "dataProvider": this.catFeedingsAgain,
          "categoryField": "created",
          "autoMargins": false,
          "marginLeft": 0,
          "marginRight": 5,
          "marginTop": 0,
          "marginBottom": 0,
          "graphs": [ {
            "valueField": "weightAfterFood",
            "showBalloon": false,
            "lineColor": "#ffbf63",
            "negativeLineColor": "#289eaf"
          } ],
          "valueAxes": [ {
            "gridAlpha": 0,
            "axisAlpha": 0,
            "guides": [ {
              "weightAfterFood": 0,
              "lineAlpha": 0.1
            } ]
          } ],
          "categoryAxis": {
            "gridAlpha": 0,
            "axisAlpha": 0,
            "startOnAxis": true
          }
        });
      },
      catMedicationsAgain: function(){
        AmCharts.makeChart( this.$refs.column, {
          "type": "serial",
          "dataProvider": this.catMedicationsAgain,
          "categoryField": "created",
          "autoMargins": false,
          "marginLeft": 0,
          "marginRight": 0,
          "marginTop": 0,
          "marginBottom": 0,
          "graphs": [ {
            "valueField": "medicationDosageGiven",
            "type": "column",
            "fillAlphas": 1,
            "showBalloon": false,
            "lineColor": "#ffbf63",
            "negativeFillColors": "#289eaf",
            "negativeLineColor": "#289eaf"
          } ],
          "valueAxes": [ {
            "gridAlpha": 0,
            "axisAlpha": 0
          } ],
          "categoryAxis": {
            "gridAlpha": 0,
            "axisAlpha": 0
          }
        } );
      }
    },
    mounted () {
      /**
       * Line Chart #2
       */
      // TODO: line = weight(waf) / day(created?)
      AmCharts.makeChart( this.$refs.line, {
        "type": "serial",
        "dataProvider": [ {
          "created": 1,
          "weightAfterFood": 120
        }, {
          "created": 2,
          "weightAfterFood": 54
        }, {
          "created": 3,
          "weightAfterFood": -18
        }, {
          "created": 4,
          "weightAfterFood": -12
        }, {
          "created": 5,
          "weightAfterFood": -51
        }, {
          "created": 6,
          "weightAfterFood": 12
        }, {
          "created": 7,
          "weightAfterFood": 56
        }, {
          "created": 8,
          "weightAfterFood": 113
        }, {
          "created": 9,
          "weightAfterFood": 142
        }, {
          "created": 10,
          "weightAfterFood": 125
        } ],
        "categoryField": "created",
        "autoMargins": false,
        "marginLeft": 0,
        "marginRight": 5,
        "marginTop": 0,
        "marginBottom": 0,
        "graphs": [ {
          "valueField": "weightAfterFood",
          "showBalloon": false,
          "lineColor": "#ffbf63",
          "negativeLineColor": "#289eaf"
        } ],
        "valueAxes": [ {
          "gridAlpha": 0,
          "axisAlpha": 0,
          "guides": [ {
            "weightAfterFood": 0,
            "lineAlpha": 0.1
          } ]
        } ],
        "categoryAxis": {
          "gridAlpha": 0,
          "axisAlpha": 0,
          "startOnAxis": true
        }
      } );

      /**
       * Column Chart #2
       */
      // TODO: column = dose(dosageGuidelines) / day(created?)
      AmCharts.makeChart( this.$refs.column, {
        "type": "serial",
        "dataProvider": [ {
          "created": 1,
          "medicationDosageGiven": -5
        }, {
          "created": 2,
          "medicationDosageGiven": 3
        }, {
          "created": 3,
          "medicationDosageGiven": 7
        }, {
          "created": 4,
          "medicationDosageGiven": -3
        }, {
          "created": 5,
          "medicationDosageGiven": 3
        }, {
          "created": 6,
          "medicationDosageGiven": 4
        }, {
          "created": 7,
          "medicationDosageGiven": 6
        }, {
          "created": 8,
          "medicationDosageGiven": -3
        }, {
          "created": 9,
          "medicationDosageGiven": -2
        }, {
          "created": 10,
          "medicationDosageGiven": 6
        } ],
        "categoryField": "created",
        "autoMargins": false,
        "marginLeft": 0,
        "marginRight": 0,
        "marginTop": 0,
        "marginBottom": 0,
        "graphs": [ {
          "valueField": "medicationDosageGiven",
          "type": "column",
          "fillAlphas": 1,
          "showBalloon": false,
          "lineColor": "#ffbf63",
          "negativeFillColors": "#289eaf",
          "negativeLineColor": "#289eaf"
        } ],
        "valueAxes": [ {
          "gridAlpha": 0,
          "axisAlpha": 0
        } ],
        "categoryAxis": {
          "gridAlpha": 0,
          "axisAlpha": 0
        }
      } );
    },
    methods:{
      // getFeedingsAgain(value) {
      //   axios.get(`/api/v1/feedings/?cat__slug&cat__name=${value}`)
      //     .then(response => {console.log("getFeedingsAgain: ");console.log(response.data.results);
      //       this.catFeedingsAgain = response.data.results
      //     })
      //     .catch(error => console.log(error));
      // },
      getFeedingsAgain(value) {
        axios.post('http://localhost:8000/graphql', {
          query:`{
            cat(name: "${value}"){
              name
              litter{
                name
              }
              carelogSet{
                foodType
                amountOfFoodTaken
                stimulated
                weightBeforeFood
                weightAfterFood
                stimulated
                stimulationType
              }
            }
          }`
        }).then(response => {console.log("catFeedingsAgain: ");
          console.log(response.data.data.cat.carelogSet); this.catFeedingsAgain = response.data.data.cat.carelogSet})
          .catch(error => console.log(error));
      },
      // getMedicationsAgain(value) {
      //   axios.get(`/api/v1/medications/?cat__slug=&cat__name=${value}`)
      //     .then(response => {console.log("catMedicationsAgain: ");console.log(response.data.results);
      //       this.catMedicationsAgain = response.data.results})
      //     .catch(error => console.log(error));
      // },
      getMedicationsAgain(value) {
        axios.post('http://localhost:8000/graphql', {
          query:`{
            cat(name: "${value}"){
              name
              litter{
                name
              }
              carelogSet{
                medicationDosageGiven
              }
            }
          }`
        }).then(response => {console.log("getMedicationsAgain: ");
          console.log(response.data.data.cat.carelogSet); this.catMedicationsAgain = response.data.data.cat.carelogSet})
          .catch(error => console.log(error));
      },
    }
  }
</script>

<style lang="scss">
  .chart-block{
    padding-top:50px;
    @media screen and (max-width: 375px) {
      padding-top:10px;
      padding-bottom:20px;
    }
  }
  .chart-block div{
    vertical-align: middle;
    display: inline-block;
    width: 50%;
    height: 30px;
  }
  .amcharts-chart-div a{
    text-indent: -9999px;
    @media screen and (max-width: 375px) {
      text-indent: -400px;
    }
    @media screen and (max-width: 667px) {
      text-indent: 100px;
    }
    outline: none;
  }
</style>
