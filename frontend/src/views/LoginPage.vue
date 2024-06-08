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
      <div class="page-container">
        <TitleBar title="Easy Money Manager" />
        <div class="inner">
          <div class="inner-content">
            <GoogleLogin :callback="callback" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/useAuth";
import { decodeCredential, googleLogout } from "vue3-google-login";

export default {
  components: {
    TitleBar,
  },
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

<style scoped>
.page-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}

.inner {
  display: flex;
  width: 100%;
  height: 80%;
  margin-bottom: 20%;
  justify-content: center;
  align-items: center;
  font-size: 24px;
}

.inner-content {
  justify-content: center;
}
</style>
