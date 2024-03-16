import type { ApiChat, ChatInvite } from "~/types/chat";
import { ChatHistory } from "./MessageHistory";
import type { ReadyUser, User } from "~/types/user";
import { getAuthorizedApi } from "../api";

export class Chat {
  readonly id!: number;
  readonly name!: string;
  readonly icon?: string;
  readonly createdAt!: string;
  readonly updatedAt?: string;
  readonly ownerId!: number;
  readonly chatHistory!: ChatHistory;
  readonly user!: ReadyUser;
  readonly isOwner!: boolean;
  private invites: ChatInvite[] | undefined;

  constructor(data: ApiChat, user: ReadyUser) {
    this.id = data.id;
    this.name = data.name;
    this.icon = data.icon;
    this.createdAt = data.createdAt;
    this.updatedAt = data.updatedAt;
    this.ownerId = data.owner_id;
    this.user = user;

    this.chatHistory = new ChatHistory(this, user);

    this.isOwner = this.user.id == this.ownerId;
  }

  /**
   * Loads and saves chat invites. undefined if user is not legit.
   */
  async loadInvites(): Promise<ChatInvite[] | undefined> {
    if (!this.isOwner) return;

    const api = getAuthorizedApi(this.user);
    const response = await api.get(`/chats/${this.id}/invites`);

    const invites = response.data as ChatInvite[];

    this.invites = invites;

    return invites;
  }

  async getInvites(): Promise<ChatInvite[] | undefined> {
    if (this.invites) return this.invites;
    else return this.loadInvites();
  }

  async createInvite(): Promise<ChatInvite> {
    const api = getAuthorizedApi(this.user);

    const response = await api.post(`/chats/${this.id}/invites`);

    const invite = response.data as ChatInvite;

    this.invites?.push(invite);

    return invite;
  }
}
