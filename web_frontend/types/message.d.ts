import type { User, Author } from "./user";

export type MessageContent = string;
export type MessagePrivileges = "author" | "owner" | "viewer";
export type MessageState = "postingError" | "hidden" | "pending";

export type Message = {
  id: string;
  content: MessageContent;
  author: Author;
  created_at: string;
  updated_at?: string;
  privileges: MessagePrivileges;
  state?: MessageState;
};
