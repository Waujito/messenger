import type { Chat } from "~/types/chat";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedMessagingApi } from "../microservices/apis";
import type { ApiChatMembership } from "../../types/chat";

export async function loadChats(user: ReadyUser): Promise<Chat[]> {
  const api = getAuthorizedMessagingApi(user);

  const chatsResponse = await api.get("/chats");

  const chatMemberships = chatsResponse.data as ApiChatMembership[];
  const chats = chatMemberships.map((cm) => cm.chat);
  return chats;
}
