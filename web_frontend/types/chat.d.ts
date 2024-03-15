import type { Chat } from "~/helpers/messagingApi/Chat";

export type ApiChat = {
  id: number;
  name: string;
  icon?: string;
  createdAt: string;
  updatedAt?: string;
  owner_id: number;
};
// export type Chat = ApiChat;

export type ChatsArr = {
  [key: number]: Chat;
};

export type ApiChatMembership = {
  userId: string;
  chat: ApiChat;
  id: number;
  joinedAt: string;
};

export type ChatCreateData = {
  name: string;
};
