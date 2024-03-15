<script setup lang="ts">
import { ChatHistory } from "~/helpers/messagingApi/MessageHistory";
import type { Message } from "~/types/message";
import MessageComponent from "./MessageComponent.vue";

const emit = defineEmits<{
  (e: "deleteMessage", message: Message): void;
  (e: "editMessage", message: Message): void;
}>();
const props = defineProps<{ messageHistory: ChatHistory }>();
const { messageHistory } = toRefs(props);

const windowSizeCap = ref<number>(50);

const window: { start: number; size: number } = reactive({
  start: 0,
  size: windowSizeCap.value / 2,
});

function scrollbarAtBottom(el: HTMLDivElement) {
  const sh = el.scrollHeight,
    st = el.scrollTop,
    ht = el.offsetHeight;

  return ht == 0 || Math.abs(st - (sh - ht)) < 10;
}
function scrollbarAtTop(el: HTMLDivElement) {
  return el.scrollTop == 0;
}

async function changeWindow(
  start: number,
  size: number = window.size,
  historyView?: HTMLDivElement
) {
  const length = messageHistory.value.history.length;

  // fixes scrollbar stuck in up and down
  let teleportScrollbar: number = !historyView
    ? -1
    : scrollbarAtTop(historyView)
      ? 100
      : scrollbarAtBottom(historyView)
        ? historyView.scrollTop - 500
        : -1;

  if (start < 0) start = 0;
  else if (length - (start + size) <= 0) {
    if (await messageHistory.value.shiftWindow(start, size)) {
      await historyScroll();
    } else {
      start = Math.max(length - size, 0);
      teleportScrollbar = -1;
    }
  }

  if (start == 0 && teleportScrollbar != 100) teleportScrollbar = -1;

  // Fixes scrollbar stuck in up and down.
  if (teleportScrollbar != -1 && historyView) {
    historyView.scrollTop = teleportScrollbar;
  }

  window.start = start;
  window.size = size;
}

const historyView: Ref<HTMLDivElement | undefined> = ref();
const messageElems: Ref<HTMLDivElement[] | undefined> = ref();

const asdf = ref<number>(1);
async function historyScroll() {
  asdf.value++;
  if (!historyView.value) return;

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
  const length = messageHistory.value.history.length;

  const start = length - (window.start + window.size);
  const end = length - window.start;

  return messageHistory.value.history
    .slice(start, end)
    .filter((message) => message.state != "hidden");
});

function scrollDown(smooth: boolean = false) {
  if (historyView.value) {
    historyView.value.scrollTo({
      top: historyView.value.scrollHeight,
      behavior: smooth ? "smooth" : "instant",
    });
  }
}

async function scrollToLastMessage(smooth: boolean = false) {
  await changeWindow(0);
  await nextTick();

  scrollDown(smooth);
}

const showArrow = computed<boolean>(() => {
  asdf.value;
  if (!historyView.value) return false;

  if (
    window.start == 0 &&
    historyView.value.scrollTop >= historyView.value.scrollHeight - 1000
  )
    return false;

  return true;
});

defineExpose({
  scrollToLastMessage,
});

onMounted(() => {
  scrollToLastMessage(false);
});

watch(messageHistory.value.newMessageId, () => {
  if (!historyView.value) return;
  if (scrollbarAtBottom(historyView.value)) scrollToLastMessage(true);
});
</script>

<template>
  <div :class="$style.historyWrapper">
    <div
      :class="$style.messageHistory"
      v-if="messageHistory"
      @scroll="historyScroll"
      ref="historyView"
    >
      <div
        :class="[
          $style.message,
          message.privileges == 'author' ? $style.self : undefined,
        ]"
        v-for="message in renderedMessageHistory"
        :key="message.id"
        ref="messageElems"
      >
        <MessageComponent
          :message="message"
          @delete-message="
            (message: Message) => $emit('deleteMessage', message)
          "
          @edit-message="(message: Message) => $emit('editMessage', message)"
        />
      </div>
    </div>
    <div :class="$style.scrollDownWrapper">
      <div
        :class="$style.scrollDownArrow"
        @click="
          async () => {
            await nextTick();
            await scrollToLastMessage(true);
          }
        "
        v-if="showArrow"
      ></div>
    </div>
  </div>
</template>

<style module lang="scss">
.historyWrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow-y: hidden;

  .messageHistory {
    display: flex;
    flex-direction: column;

    overflow-y: scroll;
    height: 100%;

    padding: 10px 20px;

    .message {
      max-width: 70%;
      min-width: 30%;
      align-self: flex-start;
      margin: 5px 0;

      &.self {
        align-self: flex-end;
      }
    }
  }

  .scrollDownWrapper {
    width: 100%;
    position: relative;

    .scrollDownArrow {
      height: 50px;
      width: 50px;

      background-color: $bg-func;
      position: absolute;
      border-radius: 100px;

      right: 15px;
      bottom: 20px;

      cursor: pointer;

      &:after {
        display: inline-block;
        content: "";
        height: 3px;
        width: 23px;

        rotate: -35deg;
        position: absolute;
        bottom: 20px;
        right: 5px;

        background-color: $cl-ftext;
        border-radius: 10px;
      }
      &:before {
        display: inline-block;
        content: "";
        height: 3px;
        width: 23px;
        rotate: 35deg;
        position: absolute;
        bottom: 20px;
        left: 5px;

        background-color: $cl-ftext;
        border-radius: 10px;
      }
    }
  }
}
</style>
