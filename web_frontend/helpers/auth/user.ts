import type { JWT, User } from "~/types/user";

export async function loadUser(userToken: JWT): Promise<User> {
  return {
    state: "ready",
    id: userToken.sub,
    name: userToken.sub,
    avatar: undefined,
    token: userToken,
  };
}
