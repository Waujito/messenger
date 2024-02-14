export type JWT = {
  rawToken: string;

  sub: string;
  aud: string;
  nbf: string;
  scope: string[];
  iss: string;
  exp: number;
  iat: number;
  jti: string;
};

export type StatedUser = { state: "unauthenticated" | "loading" };

export type ReadyUser = {
  state: "ready";
  id: string;
  name: string;
  avatar?: string;
  token: JWT;
};

export type User = StatedUser | ReadyUser;
