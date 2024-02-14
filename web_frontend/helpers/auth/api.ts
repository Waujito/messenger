import { getAxiosInstance } from "../microservices/api";

/**
 * base URL for the authorization server microservice
 */
export const AS_URL = useRuntimeConfig().public.authorizationServerURL;

export default getAxiosInstance(AS_URL);
