<script setup lang="ts">
import {
  ContextMenu,
  ContextMenuItem,
  type MenuOptions,
} from "@imengyu/vue3-context-menu";
import type { Message } from "~/types/message";

const props = defineProps<{
  message: Message;
}>();
const emit = defineEmits<{
  (e: "deleteMessage", message: Message): void;
  (e: "editMessage", message: Message): void;
}>();

const { message } = toRefs(props);

const menuVisible = ref<boolean>(false);
const contextMenuOptions: Ref<MenuOptions> = ref({ x: 0, y: 0, theme: "dark" });

function showMenu(e: MouseEvent) {
  e.preventDefault();

  contextMenuOptions.value = {
    zIndex: 1000,
    x: e.x,
    y: e.y,
  };
  menuVisible.value = true;
}

function deleteMessage() {
  emit("deleteMessage", message.value);
}

function editMessage() {
  emit("editMessage", message.value);
}
</script>

<template>
  <div :class="$style.message" @contextmenu="showMenu">
    <div :class="$style.messageAuthor">
      {{ message.author.username }}
    </div>
    <div :class="$style.messageContent">
      {{ message.content }}
    </div>
    <div :class="$style.timestamps">
      {{ message.created_at }}
      {{ message.updated_at ? "(updated)" : "" }}
      <div :class="$style.postingError" v-if="message.state == 'postingError'">
        sending error
      </div>
      <div :class="$style.pending" v-if="message.state == 'pending'">
        pending...
      </div>
    </div>

    <ContextMenu v-model:show="menuVisible" :options="contextMenuOptions">
      <ContextMenuItem
        label="Delete message"
        @click="deleteMessage"
        :class="$style.menuLabel"
      />
      <ContextMenuItem
        label="Edit message"
        @click="editMessage"
        :class="$style.menuLabel"
      />
    </ContextMenu>
  </div>
</template>

<style module lang="scss">
.message {
  display: flex;
  flex-direction: column;
  padding: 8px 8px;

  border-radius: 10px;

  background-color: $bg-message;

  height: 100%;
  width: 100%;
  .messageContent {
    margin-top: 5px;
    white-space: pre-wrap;
    overflow: hidden;
    word-wrap: break-word;
  }

  .timestamps {
    margin-top: 5px;
    text-align: end;
    display: flex;
    flex-direction: row;
    justify-content: end;

    & > * {
      margin-left: 5px;
    }

    .postingError {
      color: #cd2538;
    }
  }
}
.menuLabel {
  cursor: pointer;
}
</style>
