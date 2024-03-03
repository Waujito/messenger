import axios, {
  AxiosError,
  type AxiosInstance,
  type CreateAxiosDefaults,
} from "axios";
import { API_URL } from "./app";
import type { JWT, ReadyUser } from "~/types/user";

/**
 * Defines an error handler for axios
 */
export function defaulErrorHandler(error: AxiosError) {
  console.error(`Axios error: ${error.message}`);

  // @ts-expect-error Problems with axios data type detection. Description puts by api automatically.
  const error_desc = error.response?.data?.description;

  if (error_desc) {
    error.message = error_desc;
  }

  throw error;
}

/**
 *
 * Specifies axios config for each microservice
 *
 * @param baseURL URL of an api instance
 * @returns Axios instance for concrete API
 */
export function getAxiosInstance(baseURL: string): AxiosInstance {
  const baseOptions: CreateAxiosDefaults = {
    baseURL,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    maxRedirects: 0,
  };

  const api = axios.create(baseOptions);
  api.interceptors.response.use((r) => r, defaulErrorHandler);

  return api;
}

export function getApi() {
  return getAxiosInstance(API_URL());
}
export function getAuthorizedApi(authorization: ReadyUser | JWT) {
  const token =
    "token" in authorization && "username" in authorization
      ? authorization.token
      : authorization;

  const apiAxios = getApi();
  apiAxios.defaults.headers.common.Authorization = `Bearer ${token.rawToken}`;

  return apiAxios;
}
