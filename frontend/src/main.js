import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// install bootstrap
import "bootstrap/dist/css/bootstrap.css";

// install vue3-toastify
import "vue3-toastify/dist/index.css";

// install vue3-google-login
import vue3GoogleLogin from "vue3-google-login";

// install Pinia
import { createPinia } from "pinia";

const app = createApp(App);

const pinia = createPinia();

app.use(router);
app.use(vue3GoogleLogin, {
  clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
});
app.use(pinia);

app.mount("#app");
