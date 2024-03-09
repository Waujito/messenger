<script setup lang="ts">
import type { Chat } from "~/types/chat";
import type { Message, MessageContent } from "~/types/message";

import { ChatHistory } from "~/helpers/messagingApi/messageHistory";

import {
  sendMessage as apiSendMessage,
  deleteMessage as apiDeleteMessage,
  editMessage as apiEditMessage,
} from "~/helpers/messagingApi/messagesManagement";
import SendMessageComponent from "./SendMessageComponent.vue";
import ChatHistoryComponent from "./ChatHistoryComponent.vue";

const props = defineProps<{
  chat: Chat | undefined;
}>();

const { chat } = toRefs(props);

const userStore = useUserStore();
const user = userStore.readyUser;

const messageHistory: Ref<ChatHistory | null> = ref(null);
const chatHistoryElement: Ref<
  InstanceType<typeof ChatHistoryComponent> | undefined
> = ref();

async function initChat() {
  if (!chat.value) return (messageHistory.value = null);

  messageHistory.value = new ChatHistory(chat.value, user.value);
  await messageHistory.value.loadHistory();
}

onMounted(() => initChat());

watch(chat, async (newChat, oldChat) => {
  initChat();
});

const messageSender = ref<InstanceType<typeof SendMessageComponent> | null>(
  null
);

function messageEditFlow(message: Message) {
  messageSender.value?.messageEditFlow(message);
}

async function sendMessage(messageContent: MessageContent) {
  messageContent = messageContent.trim();
  if (!chat.value || !messageContent) return;

  const newMessage: Message = reactive({
    id: "",
    author: user.value,
    content: messageContent,
    created_at: "now",
    privileges: "author",
    state: "pending",
  });

  messageHistory.value?.messageSent(newMessage);
  nextTick(() => chatHistoryElement.value?.scrollToLastMessage(true));

  const sentMessagePromise = apiSendMessage(
    messageContent,
    chat.value,
    user.value
  );

  let sentMessage = newMessage;
  try {
    sentMessage = await sentMessagePromise;
  } catch {
    newMessage.state = "postingError";
  }

  for (const key in newMessage) {
    if (key in sentMessage) {
      // @ts-expect-error Typescript cannot normally operate with keys object mapping
      newMessage[key] = sentMessage[key];
    } else {
      // @ts-expect-error Typescript cannot normally operate with keys object mapping
      newMessage[key] = undefined;
    }
  }
  newMessage.privileges = "author";
}

async function editMessage(messageContent: MessageContent, message: Message) {
  messageContent = messageContent.trim();

  if (!chat.value || !message || !messageContent) return;

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
    console.log("Could'nt delete message.");
  }
}
</script>

<template>
  <div :class="$style.body">
    <div :class="$style.chatBody" v-if="chat">
      <div :class="$style.head">
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

      <SendMessageComponent
        @send-message="sendMessage"
        @edit-message="editMessage"
        ref="messageSender"
      />
    </div>
    <div :class="$style.noChatBody" v-else>Nothing here</div>
  </div>
</template>

<style module lang="scss">
.body {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.noChatBody {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;

  align-items: center;
  justify-content: center;
}
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
    border-left: 2px solid $bg-message;
  }
}
</style>
