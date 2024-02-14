import axios, {
  AxiosError,
  type AxiosInstance,
  type CreateAxiosDefaults,
} from "axios";

/**
 * Defines an error handler for axios
 */
export function defaulErrorHandler(error: AxiosError) {
  console.error(`Axios error: ${error.message}`);
  console.error(error);

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
