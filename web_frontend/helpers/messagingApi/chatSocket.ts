import { Socket, io } from "socket.io-client";
import { API_URL } from "../app";
import type { ReadyUser } from "~/types/user";

let socket: Socket | undefined;

function initSocket(user: ReadyUser) {
  if (!socket)
    socket = io(`${API_URL()}/chat`, {
      auth: {
        token: user.token.rawToken,
      },
    });

  return socket;
}

export function getChatSocket(user: ReadyUser) {
  if (!socket) return initSocket(user);

  return socket;
}
