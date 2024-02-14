/**
 * An origin URL for the application
 */
export function baseURL() {
  return `${window.location.origin}/`;
}

export function clientId() {
  return useRuntimeConfig().public.clientId;
}

export function AS_URL() {
  return useRuntimeConfig().public.authorizationServerURL;
}

export function API_URL() {
  return useRuntimeConfig().public.apiURL;
}
