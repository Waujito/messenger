import type { ApiChat } from "~/types/chat";
import { ChatHistory } from "./MessageHistory";
import type { ReadyUser, User } from "~/types/user";

export class Chat {
  readonly id!: number;
  readonly name!: string;
  readonly icon?: string;
  readonly createdAt!: string;
  readonly updatedAt?: string;
  readonly ownerId!: number;
  readonly chatHistory!: ChatHistory;
  readonly user!: ReadyUser;

  constructor(data: ApiChat, user: ReadyUser) {
    this.id = data.id;
    this.name = data.name;
    this.icon = data.icon;
    this.createdAt = data.createdAt;
    this.updatedAt = data.updatedAt;
    this.ownerId = data.owner_id;
    this.user = user;

    this.chatHistory = new ChatHistory(this, user);
  }
}
