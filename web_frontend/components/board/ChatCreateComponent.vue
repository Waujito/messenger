<script setup lang="ts">
import {
  createChat as apiCreateChat,
  joinChat as apiJoinChat,
} from "~/helpers/messagingApi/chatsManagement";
import type { Chat, ChatCreateData } from "~/types/chat";
const userStore = useUserStore();
const user = userStore.readyUser;

const emit = defineEmits<{
  (e: "close"): void;
  (e: "chatCreated", chat: Chat): void;
}>();

const chatName = ref<string>("");
const inviteLink = ref<string>("");
const loading = ref<boolean>(false);

async function createChat() {
  if (loading.value) return;

  try {
    const name = chatName.value.trim();
    if (!name) return alert("Chat name cannot be null");

    const data: ChatCreateData = {
      name,
    };

    const createdChat = await apiCreateChat(data, user.value);
    emit("chatCreated", createdChat);
    loading.value = true;
    emit("close");
  } catch (e) {
    if (e instanceof Error) alert(e.message);
  }
}
async function joinChat() {
  if (loading.value) return;

  try {
    if (!inviteLink.value) return alert("Invite link cannot be null");

    const joinedChat = await apiJoinChat(inviteLink.value, user.value);
    emit("chatCreated", joinedChat);
    loading.value = true;
    emit("close");
  } catch (e) {
    if (e instanceof Error) alert(e.message);
  }
}
</script>

<template>
  <div :class="$style.mask">
    <div :class="$style.window">
      <div :class="$style.chatCreation">
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
      <div :class="$style.chatJoin">
        <h2>Or join existing one:</h2>
        <div :class="$style.inputField">
          <h3>Enter invite link:</h3>
          <input :class="$style.inputName" v-model="inviteLink" />
        </div>
        <div :class="$style.actions">
          <div :class="$style.submitButton" @click="joinChat">Join</div>
        </div>
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

  & > * {
    margin-bottom: 15px;
    width: 50%;
  }

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
    justify-content: space-between;
    & > * {
      cursor: pointer;

      height: 30px;

      display: flex;
      align-items: center;
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
