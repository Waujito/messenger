export type Chat = {
  id: string;
  name: string;
  icon?: string;
  createdAt?: string;
  updatedAt?: string;
};

export type ApiChat = {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
};

export type ApiChatMembership = {
  userId: string;
  chat: ApiChat;
  id: string;
  joinedAt: string;
};
