import type { Author, JWT, User } from "~/types/user";
import { getAuthorizedApi } from "../api";

export async function loadUser(userToken: JWT): Promise<User> {
  const api = getAuthorizedApi(userToken);
  const response = await api.get("/user");
  const author: Author = response.data;

  return {
    state: "ready",
    token: userToken,
    ...author,
  };
}
