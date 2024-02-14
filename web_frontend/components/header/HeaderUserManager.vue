<script lang="ts" setup>
import { useUserStore } from "~/stores/user";
import type { User } from "~/types/user";
const userStore = useUserStore();

const user = computed(() => userStore.user);
</script>

<template>
  <div>
    <div v-if="user.state == 'unauthenticated'">
      <HeaderNoUser />
    </div>
    <div v-else-if="user.state == 'loading'">
      <HeaderUserLoading />
    </div>
    <div v-else>
      <HeaderUserAuthenticated />
    </div>
  </div>
</template>

<style module lang="scss"></style>
