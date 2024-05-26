import { ref } from "vue";
import { useCookies } from "vue3-cookies";

const { cookies } = useCookies();
const userInfo = ref({});
const loggedIn = ref(false);

export function useAuth() {
  const generateJWT = (user) => {
    try {
      const userInfoString = JSON.stringify(user);
      const userInfoBase64 = btoa(userInfoString);
      return userInfoBase64;
    } catch (error) {
      console.error("Error generating JWT:", error);
      return null;
    }
  };

  const getUserInfoFromJWT = (jwt) => {
    try {
      if (!jwt) {
        console.error("JWT is empty");
        return null;
      }

      const userInfoString = atob(jwt);
      if (!userInfoString) {
        console.error("Decoded JWT is empty");
        return null;
      }

      const userInfo = JSON.parse(userInfoString);
      return userInfo;
    } catch (error) {
      console.error("Error parsing JWT:", error);
      return null;
    }
  };

  const login = (user) => {
    const jwt = generateJWT(user);
    if (jwt) {
      cookies.set("user_jwt", jwt, {
        expire: "1d",
        secure: true,
        sameSite: "Strict",
      });
      userInfo.value = user;
      loggedIn.value = true;
    }
  };

  const logout = () => {
    cookies.remove("user_jwt");
    userInfo.value = {};
    loggedIn.value = false;
  };

  const initializeUser = () => {
    const jwt = cookies.get("user_jwt");
    if (jwt) {
      const userInfoFromJWT = getUserInfoFromJWT(jwt);
      if (userInfoFromJWT) {
        userInfo.value = userInfoFromJWT;
        loggedIn.value = true;
      } else {
        logout(); // 如果解析失败，清除无效的 JWT
      }
    }
  };

  return {
    userInfo,
    loggedIn,
    login,
    logout,
    initializeUser,
  };
}
