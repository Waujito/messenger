<script setup lang="ts">
import { useUserStore } from "~/stores/user";

const userStore = useUserStore();
</script>
<template>
  <NuxtLink to="/login">Login</NuxtLink>
</template>
