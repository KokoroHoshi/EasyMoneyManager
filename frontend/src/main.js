import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// install bootstrap
import "bootstrap/dist/css/bootstrap.css";

// install vue3-toastify
import "vue3-toastify/dist/index.css";

const app = createApp(App);

app.use(router);

app.mount("#app");
