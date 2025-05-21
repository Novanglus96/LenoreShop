import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import piniaPluginPersistedState from "pinia-plugin-persistedstate";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import { VueQueryPlugin } from "@tanstack/vue-query";

loadFonts();

const pinia = createPinia();
pinia.use(piniaPluginPersistedState);
const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(vuetify);
app.use(VueQueryPlugin);
app.mount("#app");
