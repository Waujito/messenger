import type { Chat } from "~/types/chat";
import type { Message } from "~/types/message";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";

export const nonBlankRegex = /(.|\s)*\S(.|\s)*/;

export async function loadChatHistory(
  chat: Chat,
  user: ReadyUser
): Promise<Message[]> {
  const api = getAuthorizedApi(user);

  const messageHistoryResponse = await api.get(`/chats/${chat.id}/messages`);

  const messageHistory = messageHistoryResponse.data as Message[];
  messageHistory.reverse();

  return messageHistory;
}

export async function sendMessage(
  content: string,
  chat: Chat,
  user: ReadyUser
): Promise<Message> {
  const api = getAuthorizedApi(user);

  const response = await api.post(`/chats/${chat.id}/messages`, content, {
    headers: {
      "Content-Type": "text/plain",
    },
  });

  return response.data as Message;
}
