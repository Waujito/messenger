<script setup lang="ts">
import { useUserStore } from "~/stores/user";

const userStore = useUserStore();

const user = userStore.readyUser;
</script>

<template>
  <div @click="userStore.logout">
    <p>{{ user.name }}</p>
  </div>
</template>
