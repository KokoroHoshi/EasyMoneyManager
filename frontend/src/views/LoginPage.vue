<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div v-if="loggedIn">
      <div>
        <h1>{{ userInfo.name }}</h1>
        <h3>Log out or continue?</h3>
      </div>
      <div class="d-flex justify-content-between w-100 mt-3">
        <button class="btn btn-danger" @click="logout">Logout</button>
        <button class="btn btn-primary" @click="redirect">Continue</button>
      </div>
    </div>
    <div v-else>
      <GoogleLogin :callback="callback" />
    </div>
  </div>
</template>

<script>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/useAuth";
import { decodeCredential, googleLogout } from "vue3-google-login";

export default {
  setup() {
    const router = useRouter();
    const { userInfo, loggedIn, login, logout, initializeUser } = useAuth();

    const callback = (res) => {
      const decoded = decodeCredential(res.credential);
      login(decoded);
      router.push("/record");
    };

    onMounted(() => {
      initializeUser();
    });

    return {
      userInfo,
      loggedIn,
      callback,
      logout: () => {
        googleLogout();
        logout();
      },
      redirect: () => {
        router.push("/record");
      },
    };
  },
};
</script>
