import type { Chat } from "~/types/chat";
import type {
  Message,
  MessageContent,
  MessagePrivileges,
} from "~/types/message";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";

export function getMessagePrivileges(
  message: Message,
  chat: Chat,
  user: ReadyUser
): MessagePrivileges {
  if (message.author.id === user.id) return "author";
  if (chat.owner_id == user.id) return "owner";

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

  return response.data as Message;
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
