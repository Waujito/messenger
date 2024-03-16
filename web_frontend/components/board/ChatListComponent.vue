<script setup lang="ts">
import { Chat } from "~/helpers/messagingApi/Chat";
import type { ChatsArr } from "~/types/chat";
const props = defineProps<{
  chatList: ChatsArr;
  activeChat: Chat | undefined;
}>();

const { chatList } = toRefs(props);

const emits = defineEmits<{
  (e: "chatSelected", chat: Chat): void;
}>();

const showCreatePrompt = ref<boolean>();
function chatCreated(chat: Chat) {
  chatList.value[chat.id] = chat;
  emits("chatSelected", chat);
}
</script>

<template>
  <div :class="$style.chatList">
    <div>
      <div
        :class="[
          $style.chatUnit,
          activeChat?.id == chat.id ? $style.activeChat : undefined,
        ]"
        v-for="chat of chatList"
        :key="chat.id"
        @click="() => emits('chatSelected', chat)"
      >
        {{ chat.name }}
      </div>
      <div :class="$style.createChat" @click="showCreatePrompt = true">
        Create Chat
      </div>
      <BoardChatCreateComponent
        v-if="showCreatePrompt"
        @close="showCreatePrompt = false"
        @chat-created="chatCreated"
      />
    </div>
  </div>
</template>

<style module lang="scss">
.chatList {
  display: flex;
  flex-direction: column;

  height: 100%;
  overflow-y: auto;

  width: 100%;

  background-color: $bg-func;
  color: $cl-func;

  padding: 10px 0;

  .chatUnit {
    width: 100%;
    height: 40px;

    display: flex;
    align-items: center;

    padding: 5px 10px;
    cursor: pointer;
    user-select: none;

    &.activeChat {
      background-color: $bg-func-active;
    }

    &:hover {
      background-color: $hov-func;
    }
  }

  .createChat {
    width: 100%;
    height: 60px;

    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;

    background-color: $bg-func-active;

    margin-top: 10px;
    &:hover {
      background-color: $hov-func;
    }
  }
}
</style>
