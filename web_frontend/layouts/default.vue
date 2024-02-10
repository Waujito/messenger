<script lang="ts" setup>
import "~/assets/scss/_nullstyle.scss";
</script>

<template>
  <div id="content" :class="$style.content">
    <HeaderComponent :class="$style.header" />

    <div :class="$style.main">
      <slot />
    </div>

    <FooterComponent :class="$style.footer" />
  </div>
</template>

<style lang="scss">
html,
body,
#__nuxt,
#content {
  width: 100%;
}

html {
  min-height: 100%;
}

html,
body,
#__nuxt,
#content {
  display: flex;
  flex-direction: column;

  flex-grow: 1;
}
</style>

<style module lang="scss">
.header,
.main,
.footer {
  width: 100%;
}
.main {
  display: flex;
  flex-direction: column;
  flex: 1 0 auto;

  position: relative;
}
.footer {
  flex-shrink: 0;
}
</style>
