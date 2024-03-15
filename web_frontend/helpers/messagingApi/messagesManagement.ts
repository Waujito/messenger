import { Chat } from "./Chat";
import type {
  ApiMessage,
  Message,
  MessageContent,
  MessagePrivileges,
} from "~/types/message";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";

export function getMessagePrivileges(
  message: ApiMessage,
  chat: Chat,
  user: ReadyUser
): MessagePrivileges {
  if (message.author.id === user.id) return "author";
  if (chat.ownerId == user.id) return "owner";

  return "viewer";
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

  const apiMessage = response.data as ApiMessage;
  const message: Message = responseToMessage(apiMessage, chat, user);

  return message;
}

export async function deleteMessage(
  message: Message,
  chat: Chat,
  user: ReadyUser
): Promise<void> {
  const api = getAuthorizedApi(user);

  const response = await api.delete(`/chats/${chat.id}/messages/${message.id}`);
}

export async function editMessage(
  messageContent: MessageContent,
  message: Message,
  chat: Chat,
  user: ReadyUser
): Promise<void> {
  const api = getAuthorizedApi(user);

  const response = await api.put(
    `/chats/${chat.id}/messages/${message.id}`,
    messageContent,
    {
      headers: {
        "Content-Type": "text/plain",
      },
    }
  );
}

/**
 * Converts message response from api to system message object
 * @param apiMessage
 */
export function responseToMessage(
  apiMessage: ApiMessage,
  chat: Chat,
  user: ReadyUser
): Message {
  const message: Message = {
    ...apiMessage,
    privileges: getMessagePrivileges(apiMessage, chat, user),
  };

  return message;
}
