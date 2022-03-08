Vue.component('clustercontrol', {
    props: ["thisid"],
    data: function() {
        return {
            ph: 7,
            frag: 15,
            chartInstance: "",
            clusterNum: 2
        }
    },
    methods: {
        fetchData(){
            return new Promise((resolve, reject) => {
                urlStr = "/group?ph="+this.ph.toString()+"&num="+this.clusterNum+"&fraglen="+this.frag.toString()
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
            const ctx = document.getElementById(this.thisid).getContext("2d");
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
        }
    },
    watch:{
        ph(newPH){
            this.ph = newPH;
            this.refreshChart();
        },
        frag(newLen){
            this.frag = newLen;
            this.refreshChart();
        },
        clusterNum(newNum){
            this.clusterNum = newNum;
            this.refreshChart();
        }
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
    template: '<div><label class="form-label">Fragment Length: {{frag}}</label><input type="range" min=1 max=30 class="form-range" v-model="frag" /><label class="form-label">pH: {{ph}}</label><input type="range" min=0 max=14 class="form-range" v-model="ph" /><label class="form-label">Cluster Number: {{clusterNum}}</label><input type="range" min=1 max=5 class="form-range" v-model="clusterNum" /></div>'
});
        

