<script setup lang="ts">
import type { Chat } from "~/types/chat";
import type { Message, MessageContent } from "~/types/message";

import { ChatHistory } from "~/helpers/messagingApi/messageHistory";

import {
  sendMessage as apiSendMessage,
  deleteMessage as apiDeleteMessage,
  editMessage as apiEditMessage,
} from "~/helpers/messagingApi/messagesManagement";
import MessageComponent from "./MessageComponent.vue";
import SendMessageComponent from "./SendMessageComponent.vue";

const props = defineProps<{
  chat: Chat | undefined;
}>();

const { chat } = toRefs(props);

const userStore = useUserStore();
const user = userStore.readyUser;

const messageHistory = ref<ChatHistory | null>(null);

const windowSizeCap = ref<number>(50);

const window: { start: number; size: number } = reactive({
  start: 0,
  size: windowSizeCap.value / 2,
});

const preventScroll = ref<boolean>(false);

function lockScroll(t: number) {
  preventScroll.value = true;
  setTimeout(() => (preventScroll.value = false), t);
}

async function changeWindow(
  start: number,
  size: number = window.size,
  historyView?: HTMLDivElement
) {
  const length = messageHistory.value?.history.length;
  if (length === undefined) return;

  let teleport_scrollbar: boolean = historyView?.scrollTop == 0;

  if (start < 0) start = 0;
  else if (length - (start + size) < 0)
    if (await messageHistory.value?.shiftWindow(start, size))
      await historyScroll();
    else {
      start = length - size;
      teleport_scrollbar = false;
    }

  // Fixes scrollbar stack in 0.
  if (teleport_scrollbar && historyView) historyView.scrollTop = 100;

  window.start = start;
  window.size = size;
}

const historyView: Ref<HTMLDivElement | undefined> = ref();

async function historyScroll() {
  if (!historyView.value) return;
  if (preventScroll.value) return;

  const scrollHeight = historyView.value.scrollHeight;
  const scrollTop = historyView.value.scrollTop;

  let start = window.start;
  let size = window.size;

  if (scrollTop < scrollHeight / 4) {
    if (size != windowSizeCap.value)
      size = Math.min(size + 20, windowSizeCap.value);
    else start += (windowSizeCap.value / 4) | 0;
  } else if (scrollTop > (4 * scrollHeight) / 5 && start != 0) {
    start -= (windowSizeCap.value / 4) | 0;
  }

  changeWindow(start, size, historyView.value);
}

const renderedMessageHistory = computed(() => {
  if (!messageHistory.value) return;

  const length = messageHistory.value.history.length;

  const start = length - (window.start + window.size);
  const end = length - window.start;

  return messageHistory.value.history
    .slice(start, end)
    .filter((message) => message.state != "hidden");
});

const messageHistoryElem: Ref<HTMLDivElement[] | undefined> = ref();

function scrollDown(smooth: boolean = false) {
  if (messageHistoryElem.value && messageHistoryElem.value.length > 0)
    messageHistoryElem.value[
      messageHistoryElem.value.length - 1
    ].scrollIntoView(smooth ? { behavior: "smooth" } : {});
}

async function scrollToLastMessage(smooth: boolean = false, noTimeout = false) {
  preventScroll.value = true;
  scrollDown(smooth);
  await changeWindow(0);

  lockScroll(1000);
  if (noTimeout) scrollDown(smooth);
  else setTimeout(() => scrollDown(smooth), noTimeout ? 0 : 80);
}

async function initChat() {
  if (!chat.value) return (messageHistory.value = null);

  messageHistory.value = new ChatHistory(chat.value, user.value);
  await messageHistory.value.loadHistory();
  await scrollToLastMessage(false, true);
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
  if (!chat.value || !messageContent || !messageHistory.value) return;

  const newMessage: Message = reactive({
    id: "",
    author: user.value,
    content: messageContent,
    created_at: "now",
    privileges: "author",
    state: "pending",
  });

  messageHistory.value.messageSent(newMessage);
  nextTick(() => scrollToLastMessage(true));

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
      <div
        :class="$style.messageHistory"
        v-if="messageHistory"
        @scroll="historyScroll"
        ref="historyView"
      >
        <div
          :class="$style.message"
          v-for="message in renderedMessageHistory"
          :key="message.id"
          ref="messageHistoryElem"
        >
          <MessageComponent
            :message="message"
            @delete-message="deleteMessage"
            @edit-message="messageEditFlow"
          />
        </div>
      </div>
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

  .messageHistory {
    display: flex;
    flex-direction: column;

    overflow-y: scroll;
    height: 100%;

    padding: 10px 20px;

    .message {
      max-width: 70%;
      margin: 5px 0;
    }
  }
}
</style>
