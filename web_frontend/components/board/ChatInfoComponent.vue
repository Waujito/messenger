<script setup lang="ts">
import { Chat } from "~/helpers/messagingApi/Chat";
import type { ChatInvite } from "~/types/chat";

const props = defineProps<{
  chat: Chat;
}>();

const { chat } = toRefs(props);

const emit = defineEmits<{
  (e: "close"): void;
}>();

const invites = ref<ChatInvite[] | undefined>();
const invitesLoading = ref<boolean>(false);

onMounted(async () => {
  invitesLoading.value = true;
  try {
    invites.value = await chat.value.loadInvites();
  } catch {
    console.error("Unable to load invites");
  } finally {
    invitesLoading.value = false;
  }
});

async function createInvite() {
  await chat.value.createInvite();
}
</script>

<template>
  <div :class="$style.mask">
    <div :class="$style.window">
      <div :class="$style.head">
        <h1 :class="$style.chatName">{{ chat.name }}</h1>
        <div :class="$style.closeButton" @click="emit('close')">Close</div>
      </div>
      <div :class="$style.invitesStore" v-if="chat.isOwner">
        <h2 :class="$style.invitesHead">Chat invites</h2>
        <div :class="$style.invitesList">
          <div
            :class="$style.inviteRecord"
            v-for="invite in invites"
            :key="invite.id"
          >
            {{ invite.code }}
          </div>
        </div>
        <div :class="$style.createInviteButton" @click="createInvite">
          Create invite
        </div>
      </div>
    </div>
  </div>
</template>

<style module lang="scss">
.mask {
  z-index: 10001;
  height: 100%;
  width: 100%;
  background-color: $mask-color;

  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: center;
  align-items: center;
}

.window {
  min-height: 50%;
  width: 50%;

  background-color: $bg-func;
  border-radius: 5px;

  padding: 10px;

  display: flex;
  flex-direction: column;
  align-items: center;

  .head {
    display: flex;
    flex-direction: row;

    align-items: center;
    width: 100%;

    justify-content: space-between;

    .closeButton {
      display: flex;

      @extend %red_button;

      padding: 10px 15px;
      border-radius: 5px;
    }
  }

  .invitesStore {
    width: 100%;

    .createInviteButton {
      @extend %green_button;

      padding: 10px 30px;
      border-radius: 5px;
      max-width: 200px;

      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
}
</style>
