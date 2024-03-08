import type { Chat } from "~/types/chat";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";
import type { ApiChatMembership } from "../../types/chat";

export async function loadChats(user: ReadyUser): Promise<Chat[]> {
  const api = getAuthorizedApi(user);

  const chatsResponse = await api.get("/chats");

  const chats = chatsResponse.data as Chat[];
  return chats;
}
