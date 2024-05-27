import { ref } from "vue";
import { useCookies } from "vue3-cookies";

const { cookies } = useCookies();
const userInfo = ref({});
const loggedIn = ref(false);

export function useAuth() {
  const encodeBase64 = (str) => {
    try {
      return btoa(unescape(encodeURIComponent(str)));
    } catch (error) {
      console.error("Error encoding Base64:", error);
      return null;
    }
  };

  const decodeBase64 = (str) => {
    try {
      return decodeURIComponent(escape(atob(str)));
    } catch (error) {
      console.error("Error decoding Base64:", error);
      return null;
    }
  };

  const generateJWT = (user) => {
    try {
      const userInfoString = JSON.stringify(user);
      const userInfoBase64 = encodeBase64(userInfoString);
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

      const userInfoString = decodeBase64(jwt);
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
        logout();
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
