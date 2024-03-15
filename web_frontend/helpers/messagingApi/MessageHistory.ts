import { Chat } from "./Chat";
import type { ApiMessage, Message } from "~/types/message";
import type { ReadyUser } from "~/types/user";
import { getAuthorizedApi } from "../api";
import { getMessagePrivileges, responseToMessage } from "./messagesManagement";
import { sendMessage as apiSendMessage } from "./messagesManagement";

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
  private downFilled: boolean = false;
  private loading: Promise<void> | null = null;
  private readonly pushedMessages = new Set<number>();
  /**
   * An unique id for new messages that is being processed.
   * MUST be decrement each use.
   */
  private messageSendId = -1;
  /**
   * Updates on new message. May be handled by watch() method in any component.
   * Used for autoscrolling on new message.
   */
  readonly newMessageId = reactive({
    id: 0,
  });

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

    if (!args) {
      if (this.history.length === 0) {
        args = { loadDirection: "up", loadAmount: 250 };
      } else {
        this.downFilled = false;

        while (!this.downFilled) {
          await this.loadHistory({
            loadDirection: "down",
            loadAmount: 1000,
          });
        }

        return;
      }
    }

    if (args.loadDirection == "up" && this.upFilled) return;
    if (args.loadDirection == "down" && this.downFilled) return;

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

    const preApiHistory = messageHistoryResponse.data as ApiMessage[];
    preApiHistory.reverse();

    const preHistory: Message[] = preApiHistory.map((apiMessage) =>
      responseToMessage(apiMessage, this.chat, this.user)
    );

    if (args.loadDirection == "up") {
      if (preHistory.length < limit) this.upFilled = true;

      if (this.history.length !== 0)
        while (
          preHistory.length &&
          preHistory[preHistory.length - 1].id >= this.history[0].id
        )
          preHistory.pop();
      else {
        this.downFilled = true;
      }

      this.history.unshift(...preHistory);
    } else {
      if (preHistory.length < limit) this.downFilled = true;

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

  getDownMessageIndex(): number {
    if (this.history.length != 0)
      return this.history[this.history.length - 1].id;
    else return -1;
  }

  getUpMessageIndex(): number {
    if (this.history.length != 0) return this.history[0].id;
    else return -1;
  }

  isUpFilled() {
    return this.upFilled;
  }

  /**
   * Manipulates with pushed messages to prevent duplicates.
   *
   * @param id Id of the message.
   * @returns Decision to push or not message. true = push allowed, false = disallowed.
   */
  private markNewId(id: number): boolean {
    if (this.pushedMessages.has(id)) return false;

    this.pushedMessages.add(id);
    return true;
  }

  /**
   * Pushes the message to chat history. Handles duplicates
   * @param message
   */
  newMessage(message: Message) {
    if (this.markNewId(message.id)) this.history.push(message);
    this.newMessageId.id = message.id;
  }

  async sendMessage(messageContent: string) {
    messageContent = messageContent.trim();
    if (!messageContent) return;

    const newMessage: Message = reactive({
      id: this.messageSendId--,
      author: this.user,
      content: messageContent,
      created_at: "now",
      privileges: "author",
      state: "pending",
    });

    this.newMessage(newMessage);

    try {
      const sentMessage = await apiSendMessage(
        messageContent,
        this.chat,
        this.user
      );

      // If the sent message id marked as not new, the message already dilevered as websockets event.
      // So we need to hide old `pending` message and keep version that sent by websocket.
      if (!this.markNewId(sentMessage.id)) {
        console.log("too long");
        newMessage.state = "hidden";
        return;
      }

      // Overwrite all the message but keep the reference.
      for (const key in newMessage) {
        // @ts-expect-error Typescript cannot normally operate with keys object mapping
        newMessage[key] = sentMessage[key];
      }
    } catch {
      newMessage.state = "postingError";
    }

    return newMessage;
  }
}
