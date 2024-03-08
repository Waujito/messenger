export type Chat = {
  id: string;
  name: string;
  icon?: string;
  createdAt?: string;
  updatedAt?: string;
  owner_id: string;
};

export type ApiChatMembership = {
  userId: string;
  chat: ApiChat;
  id: string;
  joinedAt: string;
};
