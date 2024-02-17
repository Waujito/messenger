<template>
  <div :class="$style.header">
    <h1>Header</h1>
    <div>
      <HeaderUserManager />
    </div>
  </div>
</template>

<script lang="ts" setup></script>

<style module lang="scss">
.header {
  width: 100%;
  display: flex;
  flex-direction: row;

  justify-content: space-between;
  align-items: center;
  padding: 10px;
}
</style>
