<script setup lang="ts">
const login = ref<string | undefined>();
const password = ref<string | undefined>();

const userStore = useUserStore();

function passwordLogin() {
  if (login.value && password.value)
    userStore.passwordLogin(login.value, password.value);
}
</script>

<template>
  <div :class="$style.authForm">
    <div>
      <h2>Enter username</h2>
      <input v-model="login" type="text" />
    </div>
    <div>
      <h2>Enter password:</h2>
      <input v-model="password" type="password" />
    </div>
    <button :class="$style.loginButton" @click="passwordLogin">Login</button>
  </div>
</template>

<style module lang="scss">
.authForm {
  display: flex;
  flex-direction: column;

  max-width: 200px;

  & > div {
    display: flex;
    flex-direction: column;

    margin-bottom: 10px;

    input {
      border: 2px solid black;
    }
  }
}
</style>
