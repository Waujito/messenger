import type { User } from "./user";

export type Message = {
  id: string;
  content: string;
  author: Author;
  created_at: string;
  updated_at?: string;
};
