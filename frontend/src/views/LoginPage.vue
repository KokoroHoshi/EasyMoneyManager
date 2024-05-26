<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div v-if="loggedIn">
      <div>
        <h2>{{ userInfo.name }}</h2>
        <h2>{{ userInfo.email }}</h2>
        <h2>{{ userInfo.sub }}</h2>
      </div>
      <button class="btn btn-danger" @click="logout">Logout</button>
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
    // onMounted(() => {
    //   initializeUser()
    //     .then(() => {})
    //     .catch((error) => {
    //       console.error("Error initializing user:", error);
    //     });
    // });

    return {
      userInfo,
      loggedIn,
      callback,
      logout: () => {
        googleLogout();
        logout();
      },
    };
  },
};
</script>
