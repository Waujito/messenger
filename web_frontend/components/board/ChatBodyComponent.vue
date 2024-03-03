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

function scrollToLastMessage(smooth: boolean = false) {
  if (messageHistoryElem.value)
    messageHistoryElem.value[
      messageHistoryElem.value.length - 1
    ].scrollIntoView(smooth ? { behavior: "smooth" } : {});
}

function tryLoadHistory() {
  if (chat.value) {
    loadChatHistory(chat.value, user.value)
      .then((h) => {
        messageHistory.value = h;
        nextTick(scrollToLastMessage);
      })
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
      author: user.value,
      content: messageContent.value,
      created_at: "now",
    });

    messageHistory.value?.push(newMessage);

    const sentMessagePromise = apiSendMessage(
      messageContent.value,
      chat.value,
      user.value
    );

    messageContent.value = "";

    nextTick(() => {
      updateTextareaHeight();
      scrollToLastMessage(true);
    });

    const sentMessage = await sentMessagePromise;

    for (const key in sentMessage) {
      // @ts-expect-error Typescript cannot normally operate with keys object mapping
      newMessage[key] = sentMessage[key];
    }
  } else {
    messageContent.value = "";

    nextTick(() => {
      updateTextareaHeight();
      scrollToLastMessage(true);
    });
  }
}

const textareaField: Ref<HTMLTextAreaElement | undefined> = ref();
const textareaMaxHeight = 200;
const textareaHeight = ref<number>(19);

function updateTextareaHeight() {
  if (!textareaField.value) return;

  textareaField.value.style.height = "0";

  textareaHeight.value = Math.min(
    textareaField.value.scrollHeight,
    textareaMaxHeight
  );

  textareaField.value.style.height = textareaHeight.value + "px";
}

onMounted(() => nextTick(updateTextareaHeight));

function focusToTextarea() {
  if (!textareaField.value) return;

  textareaField.value.focus();
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
          <div :class="$style.messageAuthor">{{ message.author.username }}</div>
          <div :class="$style.messageContent">
            {{ message.content }}
          </div>
          <div :class="$style.timestamps">
            {{ message.created_at }} {{ message.updated_at ? "(updated)" : "" }}
          </div>
        </div>
      </div>
      <div :class="$style.sendMessage" @click="focusToTextarea">
        <div :class="$style.messageContentWrapper">
          <textarea
            :class="$style.messageContent"
            :style="{ height: textareaHeight + 'px' }"
            v-model="messageContent"
            ref="textareaField"
            @input="updateTextareaHeight"
            @keypress.enter.exact="
              (e) => {
                e.preventDefault();
                sendMessage();
              }
            "
          ></textarea>
        </div>
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
      display: flex;
      flex-direction: column;
      margin: 5px 0;
      padding: 8px 8px;

      border-radius: 10px;

      background-color: $bg-message;

      max-width: 70%;
      .messageContent {
        margin-top: 5px;
        white-space: pre-wrap;
      }

      .timestamps {
        margin-top: 5px;
        text-align: end;
      }
    }
  }
  .sendMessage {
    width: 100%;
    display: flex;
    flex-direction: row;

    background-color: $bg-func;
    color: $cl-func;

    border-left: 2px solid $bg-message;

    .messageContentWrapper {
      min-height: 40px;
      flex-grow: 1;
      display: flex;
      align-items: center;
      justify-content: center;

      padding: 10px;
      .messageContent {
        resize: none;
        flex-grow: 1;

        background-color: inherit;
        color: inherit;
      }
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

      &:hover {
        background-color: $hov-func;
      }
    }
  }
}
</style>
