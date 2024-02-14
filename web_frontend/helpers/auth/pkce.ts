import crypto from "crypto-js";

export const codeChallengeMethod = "S256";

/**
 * Randomly generates a code verifier
 * @returns code verifier
 */
export function generateCodeVerifier(): string {
  return crypto.enc.Base64url.stringify(crypto.lib.WordArray.random(64));
}

/**
 *
 * Generates a code_challenge for given code verifier
 *
 * @param codeVerifier code verifier
 * @param codeChallengeMethod code challenge method
 * @returns code challenge
 */
export function generateCodeChallenge(codeVerifier: string): string {
  const hashed = crypto.SHA256(codeVerifier);

  const base64encoded = crypto.enc.Base64url.stringify(hashed);

  return base64encoded;
}

/**
 *
 * Generates all values for PKCE flow
 *
 * @param codeChallengeMethod code challenge method
 * @returns pkce credentials
 */
export function generate_PKCE_flow() {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = generateCodeChallenge(codeVerifier);

  return {
    codeVerifier,
    codeChallenge,
  };
}

/**
 * Generates PKCE credentials and saves the code verifier
 * @param codeChallengeMethod code challenge method
 * @param storageCodeVerifierName A name by which the code verifier is being saved in the storage
 * @returns code challenge
 */
export function performInitialPKCE_flow(
  storageCodeVerifierName = "codeVerifier"
) {
  const { codeVerifier, codeChallenge } = generate_PKCE_flow();

  // Save a code verifier to the storage
  sessionStorage.setItem(storageCodeVerifierName, codeVerifier);

  return { codeChallenge };
}

/**
 * Returns the code verifier and removes it from the storage
 * @param storageCodeVerifierName A name for field in the storage with the code verifier saved
 * @returns Code verifier
 */
export function performFinalPKCE_flow(
  storageCodeVerifierName = "codeVerifier"
): string {
  const codeVerifier = sessionStorage.getItem(storageCodeVerifierName);

  if (!codeVerifier)
    throw new Error("Code verifier is undefined. PKCE flow failed.");

  sessionStorage.removeItem(storageCodeVerifierName);

  return codeVerifier;
}
