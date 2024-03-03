import type { JWT } from "~/types/user";
import { getApi } from "../api";
import { getJWT, setJWT } from "./jwt";

export async function passwordLogin(
  login: string,
  password: string
): Promise<JWT> {
  const api = getApi();

  const response = await api.post("/login", {
    username: login,
    password: password,
  });

  const raw_jwt: string = response.data;
  setJWT(raw_jwt);

  return getJWT();
}
