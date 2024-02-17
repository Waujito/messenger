import type { ReadyUser } from "~/types/user";
import { API_URL } from "../app";
import { getAxiosInstance } from "./api";

export function getMessagingApi() {
  return getAxiosInstance(API_URL());
}
export function getAuthorizedMessagingApi(user: ReadyUser) {
  const apiAxios = getMessagingApi();
  apiAxios.defaults.headers.common.Authorization = `Bearer ${user.token.rawToken}`;

  return apiAxios;
}
