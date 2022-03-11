Vue.component('test', {
    props: ["thisid"],
    data: function() {
        return {
            ph: 7,
            frag: 15,
            chartInstance: ""
        }
    },
    methods: {
        fetchData(){
            return new Promise((resolve, reject) => {
                urlStr = "/api?ph="+this.ph+"&fraglen="+this.frag.toString()
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
                    yAxisID: "y",
                    borderColor: apiRes.colors[i],
                    tension: 0
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
                        title: {
                            display: true,
                            align: "center",
                            text: "Amino Acid Position"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            align: "center",
                            text: "Charge"
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
                            },
                            label: function(ctx) {
                                let label = "Amino Acid";
                                label += " (" + ctx.label + ")";
                                return label;
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
    watch:{
        frag(newLen){
            this.refreshChart();
        }
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
    template: '<div><label class="form-label">Fragment Length</label><input type="range" min=1 max=30 class="form-range" v-model="frag" /><label class="form-label">pH</label><input type="range" min=0 max=14 class="form-range" v-model="ph" /></div>'
});

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
