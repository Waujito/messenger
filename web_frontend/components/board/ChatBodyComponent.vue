<script setup lang="ts">
import { Chat } from "~/helpers/messagingApi/Chat";
import type { Message, MessageContent } from "~/types/message";

import {
  deleteMessage as apiDeleteMessage,
  editMessage as apiEditMessage,
} from "~/helpers/messagingApi/messagesManagement";
import SendMessageComponent from "./SendMessageComponent.vue";
import ChatHistoryComponent from "./ChatHistoryComponent.vue";
import { getChatSocket } from "~/helpers/messagingApi/chatSocket";

const props = defineProps<{
  chat: Chat;
}>();

const { chat } = toRefs(props);

const userStore = useUserStore();
const user = userStore.readyUser;

const chatSocket = getChatSocket(user.value);
chatSocket.emit("subscribe", { chat_id: chat.value.id });

const messageHistory = computed(() => chat.value.chatHistory);
const chatHistoryElement: Ref<
  InstanceType<typeof ChatHistoryComponent> | undefined
> = ref();
const messageSender = ref<InstanceType<typeof SendMessageComponent> | null>(
  null
);

async function initChat() {
  await chat.value.chatHistory.loadHistory();
  messageSender.value?.focusToTextarea();
  await chatHistoryElement.value?.scrollToLastMessage(false);
}

onMounted(() => initChat());

function messageEditFlow(message: Message) {
  messageSender.value?.messageEditFlow(message);
}

const sendId = ref<number>(-1);

async function sendMessage(messageContent: MessageContent) {
  const sendMessagePromise = chat.value.chatHistory.sendMessage(messageContent);

  nextTick(() => chatHistoryElement.value?.scrollToLastMessage(true));

  await sendMessagePromise;
}

async function editMessage(messageContent: MessageContent, message: Message) {
  messageContent = messageContent.trim();

  if (!message || !messageContent) return;

  const oldContent = message.content;
  const wasUpdated = message.updated_at;
  message.content = messageContent;
  message.updated_at = "now";

  try {
    await apiEditMessage(messageContent, message, chat.value, user.value);
  } catch {
    message.content = oldContent;
    message.updated_at = wasUpdated;
  }
}

async function deleteMessage(message: Message) {
  if (!chat.value) return;

  message.state = "hidden";

  try {
    await apiDeleteMessage(message, chat.value, user.value);
  } catch {
    console.log("Couldn't delete message.");
  }
}

const showInfo = ref<boolean>(false);
</script>

<template>
  <div :class="$style.chatBody">
    <div :class="$style.head" @click="showInfo = true">
      {{ chat.name }}
    </div>
    <ChatHistoryComponent
      :key="chat.id"
      v-if="messageHistory"
      :message-history="messageHistory"
      @edit-message="messageEditFlow"
      @delete-message="deleteMessage"
      ref="chatHistoryElement"
    />

    <KeepAlive>
      <SendMessageComponent
        @send-message="sendMessage"
        @edit-message="editMessage"
        ref="messageSender"
        :key="chat.id"
      />
    </KeepAlive>
    <BoardChatInfoComponent
      :chat="chat"
      v-show="showInfo"
      @close="showInfo = false"
    />
  </div>
</template>

<style module lang="scss">
.chatBody {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;

  .head {
    padding: 15px 10px;

    display: flex;
    flex-direction: row;

    align-items: center;

    background-color: $bg-func;
    border-left: 2px solid $bg-func-active;

    cursor: pointer;
  }
}
</style>
