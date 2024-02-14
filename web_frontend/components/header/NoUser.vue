<script setup lang="ts">
import { useUserStore } from "~/stores/user";

const userStore = useUserStore();
</script>
<template>
  <div @click="userStore.loginFlow()">Login</div>
</template>
