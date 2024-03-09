<script setup lang="ts">
import { createChat as apiCreateChat } from "~/helpers/messagingApi/chatsManagement";
import type { Chat, ChatCreateData } from "~/types/chat";
const userStore = useUserStore();
const user = userStore.readyUser;

const emit = defineEmits<{
  (e: "close"): void;
  (e: "chatCreated", chat: Chat): void;
}>();

const chatName = ref<string>("");
const loading = ref<boolean>(false);

async function createChat() {
  if (loading) return;

  try {
    const name = chatName.value.trim();
    if (!name) return alert("Chat name cannot be null");

    const data: ChatCreateData = {
      name,
    };

    const createdChat = await apiCreateChat(user.value, data);
    emit("chatCreated", createdChat);
    emit("close");
  } catch (e) {
    if (e instanceof Error) alert(e.message);
  }
}
</script>

<template>
  <div :class="$style.mask">
    <div :class="$style.window">
      <h1>Create chat</h1>
      <div :class="$style.inputField">
        <h3>Enter chat name:</h3>
        <input :class="$style.inputName" v-model="chatName" />
      </div>
      <div :class="$style.actions">
        <div :class="$style.submitButton" @click="createChat">Create</div>
        <div :class="$style.close" @click="emit('close')">Close</div>
      </div>
    </div>
  </div>
</template>

<style module lang="scss">
.mask {
  z-index: 10001;
  height: 100%;
  width: 100%;
  background-color: $mask-color;

  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: center;
  align-items: center;
}

.window {
  min-height: 50%;
  width: 50%;

  background-color: $bg-func;
  border-radius: 5px;

  padding: 10px;

  display: flex;
  flex-direction: column;
  align-items: center;

  .inputField {
    display: flex;
    flex-direction: column;

    & > * {
      margin-bottom: 5px;
    }
  }

  .actions {
    display: flex;
    flex-direction: row;

    margin-top: 10px;
    & > * {
      cursor: pointer;

      height: 30px;
      margin-left: 30px;

      display: flex;
      align-items: center;
      justify-content: center;
    }

    .submitButton {
      @extend %green_button;

      padding: 10px 30px;
      border-radius: 5px;
    }
    .close {
      @extend %red_button;

      padding: 10px 15px;
      border-radius: 5px;
    }
  }
}
</style>
