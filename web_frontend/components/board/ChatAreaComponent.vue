<script setup lang="ts">
import type { Chat } from "~/types/chat";
import { loadChats } from "~/helpers/messagingApi/chatsManagement";

const currentChat: Ref<Chat | undefined> = ref();

const userStore = useUserStore();
const user = userStore.readyUser;

const chats: Ref<Chat[] | undefined> = ref();

loadChats(user.value)
  .then((c) => (chats.value = c))
  .catch((err) => {
    throw err;
  });
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
      <BoardChatBodyComponent :chat="currentChat" />
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
