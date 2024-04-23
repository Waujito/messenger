<script setup lang="ts">
import { useUserStore } from "~/stores/user";

const userStore = useUserStore();

const user = userStore.readyUser;
</script>

<template>
  <div>
    <p>{{ user.username }}</p>
  </div>
  <NuxtLink to="/board">Dashboard</NuxtLink>
  <div
    @click="userStore.logout"
    style="
      height: 30px;
      width: 70px;
      cursor: pointer;
      background-color: cornflowerblue;
      display: flex;
      justify-content: center;
      align-items: center;
    "
  >
    Logout
  </div>
</template>
