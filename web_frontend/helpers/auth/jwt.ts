import { jwtDecode } from "jwt-decode";
import type { JWT } from "~/types/user";
import UnauthorizedError from "./UnauthorizedError";

export const JWTAuthorizationTokenName = "Token";

/**
 *
 * Returns JWT Authorization token or throws an error if it does not exist
 *
 * @returns User JWT Authorization token
 */
export function getJWT(): JWT {
  const token = getJWTOrNull();

  if (!token)
    throw new UnauthorizedError(
      "Unauthorized. A JWT token does not exist or have expired"
    );

  return token;
}

/**
 *
 * Returns JWT Authorization token or null if it is not exist
 *
 * @returns User JWT Authorization token
 */
export function getJWTOrNull(): JWT | null {
  if (!window) return null;
  const rawToken = window.localStorage.getItem(JWTAuthorizationTokenName);
  if (!rawToken) return null;

  const token: JWT = { ...jwtDecode(rawToken), rawToken };

  const tokenExp = new Date(0);
  tokenExp.setUTCSeconds(token.exp);

  if (tokenExp.getTime() < new Date().getTime()) {
    console.error("A JWT token has expired.");

    deleteJWT();

    return null;
  }

  return token;
}

/**
 * Setts a user JWT Authorizaion token
 * @param rawToken JWT raw token
 */
export function setJWT(rawToken: string) {
  if (window) window.localStorage.setItem(JWTAuthorizationTokenName, rawToken);
}

/**
 * Deletes user jwt authorization token
 */
export function deleteJWT() {
  if (window) window.localStorage.removeItem(JWTAuthorizationTokenName);
}
