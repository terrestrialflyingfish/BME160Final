Vue.component('test', {
    data: function() {
        return {
            phh: 7,
            fragg: 15,
            chartInstancee: ""
        }
    },
    methods: {
        fetchDataa(){
            return new Promise((resolve, reject) => {
                urlStr = "/api?ph="+this.phh.toString()+"&fraglen="+this.fragg.toString()
                fetch(urlStr)
                    .then((res) => {
                        resolve(res.json())
                    });
            });

        },
        getDataObjj(apiRes){
            dataList = []
            for (let i = 0; i < apiRes.species.length; i++) {
                var dataObj = {
                    label: apiRes.species[i],
                    data: apiRes.val[i],
                    fill: false,
                    borderColor: apiRes.colors[i],
                    tension: 0
                };
                dataList.push(dataObj);
            }
            var dataParams = {
                labels: apiRes.labels,
                datasets: dataList
            };
            return dataParams
        },
        newChartt(dataParams, title){
            const ctx = document.getElementById("testGraph").getContext("2d");
            var options = {
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: false
                    }
                }
            }
            const chart = new Chart(ctx, {
                type: "line",
                data: dataParams,
                options: options
            });
            this.chartInstancee = chart;
        },
        refreshChartt(){
            selff = this;
            this.fetchDataa()
            .then((data) => {
                apiRes = data;
                var dataParams = selff.getDataObjj(apiRes);
                selff.chartInstancee.destroy();
                selff.newChartt(dataParams, apiRes.title);
            });
        }
    },
    watch:{
        phh(newPH){
            this.phh = newPH;
            this.refreshChartt();
        },
        fragg(newLen){
            this.fragg = newLen;
            this.refreshChartt();
        }
    },
    mounted(){
        this.$nextTick(() => {
            selff = this;
            selff.fetchDataa()
            .then((data) => {
                apiRes = data;
                var dataParams = selff.getDataObjj(apiRes);
                selff.newChartt(dataParams, apiRes.title);
            });
        });
    },
    template: '<div><label for="a" class="form-label">Fragment Length</label><input id="a" type="range" min=1 max=30 class="form-range" v-model="fragg" /><label for="b" class="form-label">pH</label><input id="b" type="range" min=0 max=14 class="form-range" v-model="phh" /></div>'
});
        
