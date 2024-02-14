import { defineStore } from "pinia";
import type { ReadyUser, User } from "~/types/user";
import { deleteJWT, getJWT, getJWTOrNull } from "~/helpers/auth/jwt";
import { loadUser } from "~/helpers/auth/user";
import { OAuth2AuthorizeFlow } from "~/helpers/auth/oauth2";

export const useUserStore = defineStore("user", () => {
  const router = useRouter();

  const user: Ref<User> = ref({ state: "loading" });

  if (getJWTOrNull()) reloadUser(true);
  else user.value = { state: "unauthenticated" };

  function setUser(newUser: User) {
    user.value = newUser;
  }

  async function reloadUser(force: boolean = false): Promise<User> {
    const userToken = getJWT();

    if (user.value.state == "loading" && !force) return await getUser();
    else {
      setUser({ state: "loading" });

      setUser(await loadUser(userToken));

      return await getUser();
    }
  }

  async function getUser(): Promise<User> {
    if (user.value.state == "loading") await awaitForUserLoading();

    return user.value;
  }

  async function getReadyUser(): Promise<ReadyUser> {
    const user = await getUser();

    if (user.state === "ready") return user;
    else throw new Error("User is not ready!");
  }

  async function awaitForUserLoading() {
    await new Promise((resolve) => {
      const interval = setInterval(async () => {
        if (!(user.value.state == "loading")) {
          clearInterval(interval);
          resolve(undefined);
        }
      }, 10);
    });
  }

  /**
   *
   * Perform oauth2 login with an authorization server
   *
   */
  async function loginFlow() {
    try {
      await OAuth2AuthorizeFlow();
      await reloadUser(true);
      postLogin();
    } catch (e) {
      if (e instanceof Error)
        alert(`Login failed with an error: \n${e.message ?? ""}`);
      else alert(`An unhandled error occurred`);
    }
  }

  async function isAuthenticated(): Promise<boolean> {
    const user = await getUser();

    return user.state != "unauthenticated";
  }

  function logout() {
    deleteJWT();
    setUser({ state: "unauthenticated" });

    router.push("/");
  }

  function postLogin() {
    router.push("/board");
  }

  return {
    user: computed(() => user),
    readyUser: computed(() => user as Ref<ReadyUser>),
    getUser,
    getReadyUser,
    reloadUser,
    loginFlow,
    isAuthenticated,
    logout,
  };
});
