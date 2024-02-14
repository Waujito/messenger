/**
 * Represents the unauthorized exceptions.
 *
 */
export class UnauthorizedError extends Error {}

/**
 * Handles UnauthorizedError exceptions.
 * @param err the error that was thrown
 */
export function basicUnauthorizedErrorHandler(err: UnauthorizedError) {
  alert(`An unexpected error handled: ${err.message}`);
}

export default UnauthorizedError;
