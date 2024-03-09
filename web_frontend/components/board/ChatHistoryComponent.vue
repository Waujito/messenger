<script setup lang="ts">
import { ChatHistory } from "~/helpers/messagingApi/messageHistory";
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
  const length = messageHistory.value.history.length;

  let teleport_scrollbar: boolean = historyView?.scrollTop == 0;

  if (start < 0) start = 0;
  else if (length - (start + size) < 0)
    if (await messageHistory.value.shiftWindow(start, size))
      await historyScroll();
    else {
      start = length - size;
      teleport_scrollbar = false;
    }

  // Fixes scrollbar stuck in 0.
  if (teleport_scrollbar && historyView) historyView.scrollTop = 100;

  window.start = start;
  window.size = size;
}

const historyView: Ref<HTMLDivElement | undefined> = ref();
const messageElems: Ref<HTMLDivElement[] | undefined> = ref();

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
  const length = messageHistory.value.history.length;

  const start = length - (window.start + window.size);
  const end = length - window.start;

  return messageHistory.value.history
    .slice(start, end)
    .filter((message) => message.state != "hidden");
});

function scrollDown(smooth: boolean = false) {
  if (messageElems.value && messageElems.value.length > 0)
    messageElems.value[messageElems.value.length - 1].scrollIntoView(
      smooth ? { behavior: "smooth" } : {}
    );
}

async function scrollToLastMessage(smooth: boolean = false, noTimeout = false) {
  preventScroll.value = true;
  scrollDown(smooth);
  await changeWindow(0);

  lockScroll(1000);
  if (noTimeout) scrollDown(smooth);
  else setTimeout(() => scrollDown(smooth), noTimeout ? 0 : 80);
}

defineExpose({
  scrollToLastMessage,
});

onMounted(() => {
  console.log("mounted");
  scrollToLastMessage(false, true);
});
</script>

<template>
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
      ref="messageElems"
    >
      <MessageComponent
        :message="message"
        @delete-message="(message: Message) => $emit('deleteMessage', message)"
        @edit-message="(message: Message) => $emit('editMessage', message)"
      />
    </div>
  </div>
</template>

<style module lang="scss">
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
</style>
