Vue.component('vue-range', {
    props: ["min", "max", "label", "val"],
    template: `<div><label class="form-label">{{label}}: {{val}}</label><input type="range" :min=min :max=max class="form-range" v-bind:value='val' v-on:change='$emit("vchange", $event.target.value)' /></div>`
});
