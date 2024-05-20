import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// install bootstrap
import "bootstrap/dist/css/bootstrap.css";
// install @canvasjs/charts
// https://www.npmjs.com/package/@canvasjs/vue-stockcharts
import CanvasJSStockChart from "@canvasjs/vue-stockcharts";

const app = createApp(App);

app.use(router);
app.use(CanvasJSStockChart);

app.mount("#app");
