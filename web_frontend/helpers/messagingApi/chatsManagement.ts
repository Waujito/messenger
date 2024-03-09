import type { ApiChat, Chat, ChatCreateData } from "~/types/chat";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";
import type { ApiChatMembership } from "../../types/chat";

export async function loadChats(user: ReadyUser): Promise<Chat[]> {
  const api = getAuthorizedApi(user);

  const chatsResponse = await api.get("/chats");

  const chats = chatsResponse.data as ApiChat[];
  return chats;
}

export async function createChat(
  user: ReadyUser,
  chatInfo: ChatCreateData
): Promise<Chat> {
  const api = getAuthorizedApi(user);

  const response = await api.post("/chats", chatInfo);

  const chat = response.data as ApiChat;

  return chat;
}
