<template>
  <TitleBar title="Easy Money Manager" />
  <div
    class="login-page d-flex flex-column justify-content-center align-items-center min-vh-100"
  >
    <!-- 已登入狀態 -->
    <div v-if="loggedIn">
      <div class="text-center mb-4">
        <h1>{{ userInfo.name }}</h1>
        <h4>Log out or continue?</h4>
      </div>
      <div class="d-flex justify-content-center gap-3">
        <button class="btn btn-danger" @click="logout">Logout</button>
        <button class="btn btn-primary" @click="redirect">Continue</button>
      </div>
    </div>

    <!-- 未登入狀態 -->
    <div v-else class="page-container text-center">
      <div class="inner mt-4">
        <div class="button-column d-flex flex-column align-items-center gap-3">
          <GoogleLogin :callback="callback" />
          <button class="btn btn-secondary btn-lg" @click="guestMode">
            Continue as Guest
          </button>
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
  components: { TitleBar },
  setup() {
    const router = useRouter();
    const { userInfo, loggedIn, login, logout, initializeUser } = useAuth();

    // Google 登入 callback
    const callback = (res) => {
      try {
        const decoded = decodeCredential(res.credential);
        login(decoded);
        router.push("/record");
      } catch (err) {
        console.error("Google login failed:", err);
      }
    };

    const guestMode = () => {
      router.push("/record");
    };

    onMounted(() => {
      initializeUser();
    });

    return {
      userInfo,
      loggedIn,
      callback,
      guestMode,
      logout: () => {
        googleLogout();
        logout();
      },
      redirect: () => router.push("/record"),
    };
  },
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding: 20px;
}

/* 保留標題的原本樣式 */
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.inner {
  margin-top: 20px;
  font-size: 20px;
}

/* 垂直排列按鈕，置中 */
.button-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

/* 可統一按鈕寬度 */
.button-column > * {
  width: 220px;
  text-align: center;
}
</style>
