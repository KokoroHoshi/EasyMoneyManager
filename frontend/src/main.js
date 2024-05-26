import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// install bootstrap
import "bootstrap/dist/css/bootstrap.css";

// install vue3-toastify
import "vue3-toastify/dist/index.css";

// install vue3-google-login
import vue3GoogleLogin from "vue3-google-login";

const app = createApp(App);

app.use(router);
app.use(vue3GoogleLogin, {
  clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
});

app.mount("#app");
