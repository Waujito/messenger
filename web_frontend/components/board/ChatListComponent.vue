<script setup lang="ts">
import type { Chat } from "~/types/chat";
const props = defineProps<{
  chatList: Chat[];
}>();

const emits = defineEmits<{
  (e: "chatSelected", chat: Chat): void;
}>();
</script>

<template>
  <div :class="$style.chatList">
    <div
      :class="$style.chatUnit"
      v-for="chat of chatList"
      :key="chat.id"
      @click="() => emits('chatSelected', chat)"
    >
      {{ chat.name }}
    </div>
  </div>
</template>

<style module lang="scss">
.chatList {
  display: flex;
  flex-direction: column;

  height: 100%;
  overflow-y: scroll;

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

    &:hover {
      background-color: $dark-hov0;
    }
  }
}
</style>
