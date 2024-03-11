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

export type Author = {
  id: string;
  username: string;
  avatar?: string;
  created_at: string;
  updated_at?: string;
};

export type ReadyUser = {
  state: "ready";
  token: JWT;
} & Author;

export type User = StatedUser | ReadyUser;

export type RegisterForm = {
  username: string;
  password: string;
};
