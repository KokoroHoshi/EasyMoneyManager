<template>
  <nav
    class="navbar navbar-expand-lg navbar-light d-flex justify-content-between"
  >
    <h1 class="ms-3">{{ title }}</h1>

    <div class="me-3">
      <!-- 已登入且非 guest 顯示頭像 -->
      <div v-if="loggedIn && !isGuest" class="dropdown">
        <button
          class="btn btn-light user-avatar-btn rounded-circle p-0"
          type="button"
          id="userDropdown"
          aria-expanded="false"
          @click="toggleDropdown"
        >
          <img
            :src="userInfo.picture"
            alt="User Avatar"
            class="rounded-circle user-avatar-img"
          />
        </button>
        <ul
          id="dropdown-menu"
          class="dropdown-menu dropdown-menu-end mt-2 me-2"
          aria-labelledby="userDropdown"
          :class="{ show: isDropdownOpen }"
        >
          <li>
            <a class="dropdown-item" href="#" @click="handleLogout">Log out</a>
          </li>
        </ul>
      </div>

      <!-- 未登入顯示 Sign In 按鈕 -->
      <div v-else-if="!loggedIn">
        <button class="btn btn-primary" @click="redirectToLogin">
          Sign In
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/useAuth";
import { googleLogout } from "vue3-google-login";

export default {
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  setup() {
    const router = useRouter();
    const { userInfo, loggedIn, logout, initializeUser } = useAuth();
    const isDropdownOpen = ref(false);

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };

    const handleLogout = () => {
      googleLogout();
      logout();
      router.push("/");
    };

    const redirectToLogin = () => {
      router.push("/"); // login 頁面
    };

    const handleClickOutside = (event) => {
      if (
        isDropdownOpen.value &&
        !event.target.closest("#dropdown-menu") &&
        !event.target.closest("#userDropdown")
      ) {
        isDropdownOpen.value = false;
      }
    };

    onMounted(() => {
      initializeUser();
      document.addEventListener("click", handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    return {
      userInfo,
      loggedIn,
      isDropdownOpen,
      toggleDropdown,
      handleLogout,
      redirectToLogin,
    };
  },
};
</script>

<style scoped>
.user-avatar-btn {
  width: 60px;
  height: 60px;
  background-color: white;
  border: none;
}

.user-avatar-btn:hover {
  background-color: gray;
}

.user-avatar-img {
  width: 32px;
  height: 32px;
}

.dropdown-menu {
  right: 0;
  left: auto;
}

.dropdown-item:hover {
  background-color: gray;
  color: white;
}

h1 {
  color: rgb(0, 0, 0);
  padding-left: 4.2rem;
  font-weight: bolder;
  margin: auto;
}

.btn-primary {
  min-width: 100px;
}
</style>
