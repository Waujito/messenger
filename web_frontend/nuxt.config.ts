// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/library.scss" as *;',
        },
      },
    },
  },

  modules: ["@pinia/nuxt"],

  ssr: false,

  runtimeConfig: {
    public: {
      apiURL: "",
      apiURI: "",
    },
  },
});
