<script setup lang="ts">
import type { Chat } from "~/types/chat";
import type { Message, MessageContent } from "~/types/message";
import { loadChatHistory } from "~/helpers/messagingApi/messagesManagement";
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

const messageHistory: Ref<Message[] | undefined> = ref();
const renderedMessageHistory = computed(() =>
  messageHistory.value?.filter((message) => message.state != "hidden")
);

const messageHistoryElem: Ref<HTMLDivElement[] | undefined> = ref();

function scrollToLastMessage(smooth: boolean = false) {
  console.log(messageHistory.value);
  if (messageHistoryElem.value && messageHistoryElem.value.length > 0)
    messageHistoryElem.value[
      messageHistoryElem.value.length - 1
    ].scrollIntoView(smooth ? { behavior: "smooth" } : {});
}
// todo: Add paging
function tryLoadHistory() {
  if (chat.value) {
    messageHistory.value = undefined;

    loadChatHistory(chat.value, user.value)
      .then((h) => {
        messageHistory.value = h;
        nextTick(scrollToLastMessage);
      })
      .catch((err) => {
        throw err;
      });
  }
}

tryLoadHistory();

watch(chat, async (newChat, oldChat) => {
  tryLoadHistory();
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

  messageHistory.value.push(newMessage);
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
      <div :class="$style.messageHistory" v-if="messageHistory">
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
