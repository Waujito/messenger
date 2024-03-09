export type ApiChat = {
  id: string;
  name: string;
  icon?: string;
  createdAt?: string;
  updatedAt?: string;
  owner_id: string;
};
export type Chat = ApiChat;

export type ApiChatMembership = {
  userId: string;
  chat: ApiChat;
  id: string;
  joinedAt: string;
};

export type ChatCreateData = {
  name: string;
};
