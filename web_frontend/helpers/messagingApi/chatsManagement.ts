import type { ApiChat, ChatCreateData, ChatsArr } from "~/types/chat";
import { Chat } from "./Chat";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";
import type { ApiChatMembership } from "../../types/chat";

export async function loadChats(user: ReadyUser): Promise<ChatsArr> {
  const api = getAuthorizedApi(user);

  const chatsResponse = await api.get("/chats");

  const apiChats = chatsResponse.data as ApiChat[];

  const chats = apiChats.map((apiChat) => new Chat(apiChat, user));

  const chatsArr: ChatsArr = {};
  for (const chat of chats) {
    chatsArr[chat.id] = chat;
  }

  return chatsArr;
}

export async function createChat(
  chatInfo: ChatCreateData,
  user: ReadyUser
): Promise<Chat> {
  const api = getAuthorizedApi(user);

  const response = await api.post("/chats", chatInfo);

  const apiChat = response.data as ApiChat;

  const chat = new Chat(apiChat, user);

  return chat;
}

export async function joinChat(
  inviteLink: string,
  user: ReadyUser
): Promise<Chat> {
  const api = getAuthorizedApi(user);

  const inviteCode = inviteLink;
  const response = await api.post(`/invite?code=${inviteCode}`);

  const apiChat = response.data as ApiChat;
  const chat = new Chat(apiChat, user);

  return chat;
}
