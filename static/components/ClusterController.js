Vue.component('scatter', {
    props: ["graphid", "api", "params", "info"],
    data: function() {
        return {
            chartInstance: "",
            valDict: {},
            components: [{"name": "vue-range", "url": "/static/modules/vue-range.js"}]
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
                console.log(this.apiUrl)
                urlStr = this.apiUrl
                fetch(urlStr)
                    .then((res) => {
                        resolve(res.json())
                    });
            });

        },
        getDataObj(apiRes){
            var datasets = []
            for (let i = 0; i < apiRes.groups.length; i++) {
              datasets.push({
                  label: apiRes.groups[i],
                  labels: apiRes.labels[i],
                  data: apiRes.val[i],
                  backgroundColor: apiRes.colors[i],
                  borderColor: apiRes.colors[i]
              });
            }
            var dataParams = {
                datasets: datasets
            };
            return dataParams
        },
        newChart(dataParams, title){
            const ctx = document.getElementById(this.graphid).getContext("2d");
            let options = {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: title
                    },
                    tooltip: {
                        callbacks: {
                            label: function(ctx) {
                                // console.log(ctx);
                                let label = ctx.dataset.labels[ctx.dataIndex];
                                label += " (" + ctx.parsed.x.toFixed(2) + ", " + ctx.parsed.y.toFixed(2) + ")";
                                return label;
                            }
                        }
                    }
                }
            }
            const chart = new Chart(ctx, {
                type: "scatter",
                data: dataParams,
                options: options
            });
            this.chartInstance = chart;
        },
        refreshChart(){
            self = this;
            this.fetchData()
            .then((data) => {
                apiRes = data;
                var dataParams = self.getDataObj(apiRes);
                self.chartInstance.destroy();
                self.newChart(dataParams, apiRes.title);
            });
        },
        getVal(varName){
            return this[varName]
        }
    },
    created(){
      this.initValDict();
    },
    mounted(){
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
