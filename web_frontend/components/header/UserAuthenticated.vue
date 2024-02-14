<script setup lang="ts">
import { useUserStore } from "~/stores/user";
import type { ReadyUser } from "~/types/user";

const userStore = useUserStore();

const user = computed(() => userStore.user as ReadyUser);
</script>

<template>
  <div @click="userStore.logout">{{ user.name }}</div>
</template>
