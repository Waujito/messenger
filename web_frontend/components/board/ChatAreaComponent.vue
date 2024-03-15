<script setup lang="ts">
import { Chat } from "~/helpers/messagingApi/Chat";
import { loadChats } from "~/helpers/messagingApi/chatsManagement";
import { getChatSocket } from "~/helpers/messagingApi/chatSocket";
import {
  getMessagePrivileges,
  responseToMessage,
} from "~/helpers/messagingApi/messagesManagement";
import type { ChatsArr } from "~/types/chat";
import type { ApiMessage, Message } from "~/types/message";

const currentChat: Ref<Chat | undefined> = ref();

const userStore = useUserStore();
const user = userStore.readyUser;

const chats: Ref<ChatsArr | undefined> = ref();

loadChats(user.value)
  .then((c) => (chats.value = c))
  .catch((err) => {
    throw err;
  });

const chatSocket = getChatSocket(user.value);

chatSocket.off();

chatSocket.on(
  "messageSent",
  async (data: { chat_id: number; message: ApiMessage }) => {
    if (!chats.value) return;

    const { chat_id } = data;
    const chat = chats.value[chat_id];
    if (!chat) return;

    const apiMessage = data.message;

    // Websockets works much faster than api connections
    // Which is of course good, but terrible if the message sent by current client
    // (Leads to broken animations and scrollbar stuck)
    if (apiMessage.author.id == user.value.id)
      await new Promise((r) => setTimeout(r, 100));

    const message: Message = responseToMessage(apiMessage, chat, user.value);

    chat.chatHistory.newMessage(message);
  }
);

chatSocket.on(
  "messageDelete",
  async (data: { chat_id: number; message_id: number }) => {
    if (!chats.value) return;

    const { chat_id, message_id } = data;

    const chat = chats.value[chat_id];
    if (!chat) return;

    const message = chat.chatHistory.messageFromId(message_id);
    if (!message) return;

    message.state = "hidden";
  }
);

chatSocket.on(
  "messageUpdate",
  async (data: { chat_id: number; message: ApiMessage }) => {
    if (!chats.value) return;

    const { chat_id, message } = data;

    const chat = chats.value[chat_id];
    if (!chat) return;

    const chatMessage = chat.chatHistory.messageFromId(message.id);
    if (!chatMessage) return;

    for (const key in message) {
      // @ts-expect-error Typescript cannot normally operate with keys object mapping
      chatMessage[key] = message[key];
    }
  }
);
</script>
<template>
  <div :class="$style.content">
    <div :class="$style.chatList">
      <BoardChatListComponent
        :chat-list="chats"
        @chat-selected="(chat) => (currentChat = chat)"
        :activeChat="currentChat"
        v-if="chats"
      />
      <div :class="$style.chatsLoading" v-else>Loading...</div>
    </div>
    <div :class="$style.chatBody">
      <BoardChatBodyComponent
        v-if="currentChat"
        :chat="currentChat"
        :key="currentChat?.id"
      />
    </div>
  </div>
</template>

<style module lang="scss">
.content {
  display: flex;
  flex-direction: row;

  height: 100%;
  width: 100%;

  background-color: $bg-chat;
  color: $cl-func;

  .chatList {
    display: flex;
    flex-direction: row;

    height: 100%;
    width: 30%;
  }

  .chatBody {
    display: flex;
    flex-direction: row;

    height: 100%;
    width: 70%;
  }
}
</style>
