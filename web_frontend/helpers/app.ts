/**
 * An origin URL for the application
 */
export function baseURL() {
  return `${window.location.origin}/`;
}

export function API_URL() {
  return useRuntimeConfig().public.apiURL;
}

export function API_URI() {
  return useRuntimeConfig().public.apiURI;
}
