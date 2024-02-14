/**
 * An origin URL for the application
 */
export function baseURL() {
  if (!window) return "";
  return `${window.location.origin}/`;
}
