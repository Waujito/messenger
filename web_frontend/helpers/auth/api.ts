import { getAxiosInstance } from "../microservices/api";

/**
 * base URL for the authorization server microservice
 */
export function AS_URL() {
  return useRuntimeConfig().public.authorizationServerURL;
}

export default function () {
  return getAxiosInstance(AS_URL());
}
