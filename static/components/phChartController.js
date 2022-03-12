Vue.component('line-chart', {
    props: ["thisid","api", "params", "info", "axes"],
    data: function() {
        return {
            fraglen: 15,
            chartInstance: "",
            valDict: {}
        }
    },
    computed: {
      apiUrl(){
         base = "/"+this.api+"?&info="+this.info
         this.params.forEach((item,index)=>{
             paramStr = "&"+item.name+"="+this.valDict[item.name]
             base += paramStr
         })
         return base
      }
    },
    methods: {
      initValDict(){
          vdict ={}
          this.params.forEach((item,index)=>{
              vdict[item.name] = item.default
          })
          this.valDict = vdict
          return vdict
      },
       vhandler(e, name){
          this.valDict[name] = e;
          this.refreshChart();
       },
        fetchData(){
            return new Promise((resolve, reject) => {
                urlStr = this.apiUrl
                fetch(urlStr)
                    .then((res) => {
                        resolve(res.json())
                    });
            });

        },
        getDataObj(apiRes){
            dataList = []
            for (let i = 0; i < apiRes.species.length; i++) {
                var dataObj = {
                    label: apiRes.species[i],
                    data: apiRes.val[i],
                    fill: false,
                    borderColor: apiRes.colors[i],
                    lineTension: 0
                };
                dataList.push(dataObj);
            }
            var dataParams = {
                datasets: dataList
            };
            return dataParams
        },
        newChart(dataParams, title){
            const ctx = document.getElementById(this.thisid).getContext("2d");
            var options = {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: "linear",
                        display:true,
                        position: 'bottom',
                        title: {
                            display: true,
                            align: "center",
                            text: this.axes.x.label
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            align: "center",
                            text: this.axes.y.label
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: title
                    },
                    tooltip: {
                        callbacks: {
                            title: function(ctx) {
                                console.log(ctx[0]);
                                //let title = ctx.dataset.label;
                               return ctx[0].dataset.label;
                            }
                        }
                    }
                }
            }
            const chart = new Chart(ctx, {
                type: "line",
                data: dataParams,
                options: options
            });
            this.chartInstance = chart;
        },
        refreshChart(){
            this.fetchData()
            .then((data) => {
                apiRes = data;
                var dataParams = this.getDataObj(apiRes);
                this.chartInstance.destroy();
                this.newChart(dataParams, apiRes.title);
            });
        }
    },
    created(){
      this.initValDict();
    },
    mounted: function(){
        this.$nextTick(() => {
            this.fetchData()
            .then((data) => {
                apiRes = data;
                var dataParams = this.getDataObj(apiRes);
                this.newChart(dataParams, apiRes.title);
            });
        });
    },
    template: `
              <div>
                  <template v-for='paramObj in params'>
                      <vue-range :val='valDict[paramObj.name]' v-on:vchange='vhandler($event, paramObj.name)' :min=paramObj.pmin :max=paramObj.pmax :label=paramObj.label></vue-range>
                  </template>
              </div>
              `
});
