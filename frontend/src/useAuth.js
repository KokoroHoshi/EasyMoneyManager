import { ref } from "vue";
import { useCookies } from "vue3-cookies";

const { cookies } = useCookies();
const userInfo = ref({});
const loggedIn = ref(false);

export function useAuth() {
  const generateJWT = (user) => {
    try {
      const userInfoString = JSON.stringify(user);
      const encoder = new TextEncoder();
      const userInfoBytes = encoder.encode(userInfoString);
      const userInfoBase64 = btoa(String.fromCharCode(...userInfoBytes));
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

      const base64Regex = /^[a-zA-Z0-9-_]+$/;
      if (!base64Regex.test(jwt)) {
        console.error("Invalid Base64 string:", jwt);
        return null;
      }

      const utf8UserInfoString = atob(jwt);
      if (!utf8UserInfoString) {
        console.error("Decoded JWT is empty");
        return null;
      }

      const userInfo = JSON.parse(utf8UserInfoString);
      return userInfo;
    } catch (error) {
      console.error("Error parsing JWT:", error);
      return null;
    }
  };

  const login = (user) => {
    const jwt = generateJWT(user);
    cookies.set("user_jwt", jwt, {
      expire: "1d",
      secure: true,
      sameSite: "Strict",
    });
    userInfo.value = user;
    loggedIn.value = true;
  };

  const logout = () => {
    cookies.remove("user_jwt");
    userInfo.value = {};
    loggedIn.value = false;
  };

  const initializeUser = async () => {
    const jwt = cookies.get("user_jwt");
    if (jwt) {
      const userInfoFromJWT = await getUserInfoFromJWT(jwt);
      userInfo.value = userInfoFromJWT;
      loggedIn.value = true;
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
