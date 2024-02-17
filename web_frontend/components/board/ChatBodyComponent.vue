<script setup lang="ts">
import type { Chat } from "~/types/chat";
import type { Message } from "~/types/message";
import {
  loadChatHistory,
  nonBlankRegex,
} from "~/helpers/messagingApi/messagesManagement";
import { sendMessage as apiSendMessage } from "~/helpers/messagingApi/messagesManagement";

const props = defineProps<{
  chat: Chat | undefined;
}>();

const { chat } = toRefs(props);

const userStore = useUserStore();
const user = userStore.readyUser;

const messageHistory: Ref<Message[] | undefined> = ref();

const messageHistoryElem: Ref<HTMLDivElement[] | undefined> = ref();

function tryLoadHistory() {
  if (chat.value) {
    loadChatHistory(chat.value, user.value)
      .then((h) => (messageHistory.value = h))
      .catch((err) => {
        throw err;
      });
  } else messageHistory.value = undefined;
}

tryLoadHistory();

watch(chat, async (newChat, oldChat) => {
  tryLoadHistory();
});

const messageContent: Ref<string> = ref("");

async function sendMessage() {
  if (!chat.value || !messageContent.value) return;
  if (nonBlankRegex.test(messageContent.value)) {
    const newMessage: Message = reactive({
      id: "",
      authorId: user.value.id,
      content: messageContent.value,
      createdAt: "now",
    });

    messageHistory.value?.push(newMessage);

    if (messageHistoryElem.value)
      messageHistoryElem.value[
        messageHistoryElem.value.length - 1
      ].scrollIntoView({ behavior: "smooth" });

    const sentMessage = await apiSendMessage(
      messageContent.value,
      chat.value,
      user.value
    );

    for (const key in sentMessage) {
      // @ts-expect-error Typescript cannot normally operate with keys object mapping
      newMessage[key] = sentMessage[key];
    }
  }
}
</script>

<template>
  <div :class="$style.body">
    <div :class="$style.chatBody" v-if="chat">
      <div :class="$style.head">
        {{ chat.name }}
      </div>
      <div :class="$style.messageHistory">
        <div
          :class="$style.message"
          v-for="message in messageHistory"
          :key="message.id"
          ref="messageHistoryElem"
        >
          <div :class="$style.messageInfo">
            {{ message.authorId }} at {{ message.createdAt }}
          </div>
          <div :class="$style.messageContent">
            {{ message.content }}
          </div>
        </div>
      </div>
      <div :class="$style.sendMessage">
        <textarea
          :class="$style.messageContent"
          v-model="messageContent"
        ></textarea>
        <div :class="$style.messageSendButton" @click="sendMessage">Send</div>
      </div>
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
    padding: 10px 10px;

    display: flex;
    flex-direction: row;

    align-items: center;
  }

  .messageHistory {
    display: flex;
    flex-direction: column;

    overflow-y: scroll;

    .message {
      padding: 10px 0;
      .messageContent {
        white-space: pre-wrap;
      }
    }
  }
  .sendMessage {
    height: 50px;
    width: 100%;
    display: flex;
    flex-direction: row;

    background-color: blue;
    color: white;

    .messageContent {
      padding: 10px;
      resize: none;

      flex-grow: 1;

      background-color: inherit;
      color: inherit;
    }

    .messageSendButton {
      padding: 10px;

      display: flex;

      text-align: center;
      align-items: center;
      justify-content: center;

      background-color: inherit;
      color: inherit;

      cursor: pointer;
      user-select: none;
    }
  }
}
</style>
