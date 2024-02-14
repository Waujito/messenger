import auth from "./auth";
import type { RouteLocationNormalized } from "vue-router";

export function isProtected(to: RouteLocationNormalized): boolean {
  if (to.path.startsWith("/board")) return true;

  return false;
}

export default defineNuxtRouteMiddleware(async (to, from) => {
  if (isProtected(to)) return await auth(to, from);
});
