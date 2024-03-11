<script setup lang="ts">
import { getApi } from "~/helpers/api";
import type { RegisterForm } from "~/types/user";

const username = ref<string>("");
const password = ref<string>("");

async function register() {
  const api = getApi();

  if (!username.value || !password.value)
    return alert("Required fields are null.");

  const form: RegisterForm = {
    username: username.value,
    password: password.value,
  };

  try {
    const response = await api.post("/register", form);
  } catch (e) {
    alert(e instanceof Error ? e.message : "An unexpected error occured");
  }

  useRouter().push("/login");
}
</script>

<template>
  <div :class="$style.registerForm">
    <h1>Register</h1>
    <div>
      <h2>Enter name:</h2>
      <input v-model="username" type="text" />
    </div>
    <div>
      <h2>Enter password:</h2>
      <input v-model="password" type="password" />
    </div>
    <button :class="$style.loginButton" @click="register">Login</button>
  </div>
</template>

<style module lang="scss">
.registerForm {
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
