import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// install bootstrap first
import "bootstrap/dist/css/bootstrap.css";
// install vue3-highcharts
import VueHighcharts from "vue3-highcharts";

createApp(App).use(router).use(VueHighcharts).mount("#app");
