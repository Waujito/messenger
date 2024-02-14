export default defineNuxtRouteMiddleware(async (to, from) => {
  if (window == undefined) return;
  const userStore = useUserStore();

  const user = await userStore.getUser();

  if (user.state !== "ready") return navigateTo("/");
});
