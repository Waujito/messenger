<script setup lang="ts">
import { useUserStore } from "~/stores/user";

const userStore = useUserStore();

const user = userStore.readyUser;
</script>

<template>
  <div @click="userStore.logout">
    <p>{{ user.username }}</p>
  </div>
  <NuxtLink to="/board">Dashboard</NuxtLink>
</template>
