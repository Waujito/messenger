import type { Chat } from "~/types/chat";
import type { Message } from "~/types/message";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";
import { getMessagePrivileges } from "./messagesManagement";

export type LoadArgs = {
  loadDirection: "up" | "down";
  loadAmount: number;
};

/**
 * Manages history of the chat.
 *
 */
export class ChatHistory {
  readonly chat!: Chat;
  readonly user!: ReadyUser;
  readonly history: Message[] = [];
  private upFilled: boolean = false;
  private loading: Promise<void> | null = null;

  constructor(chat: Chat, user: ReadyUser) {
    this.chat = chat;
    this.user = user;
  }

  async loadHistory(args?: LoadArgs) {
    if (!this.loading) this.loading = this._LoadHistory(args);

    await this.loading;
    this.loading = null;
  }

  async _LoadHistory(args?: LoadArgs): Promise<void> {
    const api = getAuthorizedApi(this.user);
    if (!args) args = { loadDirection: "up", loadAmount: 250 };

    if (args.loadDirection == "up" && this.upFilled) return;

    const limit = args.loadAmount;
    const startIdx =
      args.loadDirection == "up"
        ? this.getUpMessageIndex()
        : this.getDownMessageIndex();
    const loadDirection = args.loadDirection == "up" ? 1 : -1;

    // console.log(this.getFirstMessageIndex(), this.getLastMessageIndex());

    const messageHistoryResponse = await api.get(
      `/chats/${this.chat.id}/messages?limit=${limit}&startIdx=${startIdx}&loadDirection=${loadDirection}`
    );

    const preHistory = messageHistoryResponse.data as Message[];
    preHistory.reverse();

    preHistory.map(
      (message) =>
        (message.privileges = getMessagePrivileges(
          message,
          this.chat,
          this.user
        ))
    );

    if (args.loadDirection == "up") {
      if (preHistory.length < limit) this.upFilled = true;

      if (this.history.length !== 0)
        while (
          preHistory.length &&
          preHistory[preHistory.length - 1].id >= this.history[0].id
        )
          preHistory.pop();

      this.history.unshift(...preHistory);
    } else {
      preHistory.shift();
      this.history.push(...preHistory);
    }
  }

  /**
   * Loads history when needed
   * @param start Same as in window in history component
   * @param size Same as in window in history component
   * @returns Boolean points to allow start point change or to not.
   */
  async shiftWindow(start: number, size: number): Promise<boolean> {
    if (start + size > this.history.length) {
      if (this.upFilled) return false;

      await this.loadHistory({
        loadDirection: "up",
        loadAmount: 100,
      });

      return true;
    }
    return true;
  }

  getDownMessageIndex(): string {
    if (this.history.length != 0)
      return this.history[this.history.length - 1].id;
    else return "-1";
  }

  getUpMessageIndex(): string {
    if (this.history.length != 0) return this.history[0].id;
    else return "-1";
  }

  isUpFilled() {
    return this.upFilled;
  }

  messageSent(message: Message) {
    this.history.push(message);
  }
}
