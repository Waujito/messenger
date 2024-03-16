<script setup lang="ts">
import type { Message, MessageContent } from "~/types/message";

const messageContent = ref<MessageContent>("");
const isEditing = ref<boolean>(false);
const editingMessage = ref<Message | null>();
const displaySenderInfo = computed<boolean>(() => isEditing.value);

const emit = defineEmits<{
  (e: "sendMessage", messageContent: MessageContent): void;
  (e: "editMessage", messageContent: MessageContent, message: Message): void;
}>();

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
watch(messageContent, () => nextTick(updateTextareaHeight));

function focusToTextarea() {
  if (!textareaField.value) return;

  textareaField.value.focus();
}

function messageEditFlow(message: Message) {
  messageContent.value = message.content;
  isEditing.value = true;
  editingMessage.value = message;
  focusToTextarea();
}

defineExpose({
  messageEditFlow,
  focusToTextarea,
});

function sendButton() {
  if (isEditing.value) {
    isEditing.value = false;

    if (editingMessage.value)
      emit("editMessage", messageContent.value, editingMessage.value);
  } else emit("sendMessage", messageContent.value);

  messageContent.value = "";
}
</script>

<template>
  <div :class="$style.sendMessage" @click="focusToTextarea">
    <div :class="$style.senderInfo" v-if="displaySenderInfo">
      <div
        :class="[$style.editingMessage, $style.messagedInfo]"
        v-if="isEditing"
      >
        <p :class="$style.infoText">Editing message</p>
        <div
          :class="$style.closeInfo"
          @click="
            isEditing = false;
            messageContent = '';
          "
        >
          CLOSE
        </div>
      </div>
    </div>
    <div :class="$style.messagePrompt">
      <div :class="$style.messageContentWrapper">
        <textarea
          :class="$style.messageContent"
          :style="{ height: textareaHeight + 'px' }"
          v-model="messageContent"
          ref="textareaField"
          @keypress.enter.exact="
            (e) => {
              e.preventDefault();
              sendButton();
            }
          "
        ></textarea>
      </div>
      <div :class="$style.messageSendButton" @click="sendButton">Send</div>
    </div>
  </div>
</template>

<style module lang="scss">
.sendMessage {
  width: 100%;
  display: flex;
  flex-direction: column;

  background-color: $bg-func;
  color: $cl-func;

  border-left: 2px solid $bg-func-active;

  .senderInfo {
    height: 50px;
    width: 100%;

    border-bottom: 3px solid $bg-message;
    display: flex;

    .messagedInfo {
      display: flex;
      flex-direction: row;

      height: 100%;
      width: 100%;

      justify-content: space-between;
      text-align: center;
      align-items: center;

      padding: 0 10px;

      .closeInfo {
        height: 100%;
        padding: 0 10px;

        cursor: pointer;

        display: flex;
        align-items: center;
      }
    }
  }

  .messagePrompt {
    display: flex;
    flex-direction: row;

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
