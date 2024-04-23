import { defineStore } from "pinia";
import type { JWT, ReadyUser, User } from "~/types/user";
import { deleteJWT, getJWT, getJWTOrNull } from "~/helpers/auth/jwt";
import { loadUser } from "~/helpers/auth/user";
import { passwordLogin as passwordLoginHelper } from "~/helpers/auth/login";

export const useUserStore = defineStore("user", () => {
  const router = useRouter();

  const user: Ref<User> = ref({ state: "loading" });

  if (getJWTOrNull()) reloadUser(true);
  else user.value = { state: "unauthenticated" };

  function setUser(newUser: User) {
    user.value = newUser;
  }

  function setNullUser() {
    setUser({ state: "unauthenticated" });
    return user.value;
  }

  function setLoadingUser() {
    setUser({ state: "loading" });
    return user.value;
  }

  async function reloadUser(force: boolean = false): Promise<User> {
    const userToken = getJWTOrNull();
    if (!userToken) return setNullUser();

    if (user.value.state == "loading" && !force) return await getUser();
    else {
      setUser({ state: "loading" });

      try {
        const loaded = await loadUser(userToken);
        setUser(loaded);
      } catch {
        return dropUser();
      }

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

  async function passwordLogin(login: string, password: string) {
    console.log(`${login}:${password}`);
    const awtf = passwordLoginHelper(login, password);

    await defaultLoginFlowAwaiter(awtf);
  }

  async function defaultLoginFlowAwaiter(awt_func: Promise<JWT>) {
    try {
      setLoadingUser();

      const jwt = await awt_func;

      setUser(await loadUser(jwt));
      postLogin();
    } catch (e) {
      alert(e instanceof Error ? e.message : "An unexpected error occured!");
      setNullUser();
    }
  }

  async function isAuthenticated(): Promise<boolean> {
    const user = await getUser();

    return user.state != "unauthenticated";
  }

  function dropUser() {
    deleteJWT();
    return setNullUser();
  }

  function logout() {
    dropUser();
    console.log("user logged out!");

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
    passwordLogin,
    isAuthenticated,
    logout,
  };
});
