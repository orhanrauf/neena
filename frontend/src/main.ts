/* eslint-disable import/order */
import "@/@iconify/icons-bundle";
import App from "@/App.vue";
import layoutsPlugin from "@/plugins/layouts";
import vuetify from "@/plugins/vuetify";
import { loadFonts } from "@/plugins/webfontloader";
import router from "@/router";
import "@core/scss/template/index.scss";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import "@styles/styles.scss";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { createPinia } from "pinia";
import { createApp } from "vue";
import dayjs from "dayjs";
import "dayjs/locale/en";

dayjs.locale("en");

loadFonts();

// Create vue app
const app = createApp(App);

// Use plugins
app.use(vuetify);
app.use(createPinia());
app.use(router);
app.use(layoutsPlugin);
app.use(ElementPlus);
// @ts-ignore
app.use(dayjs);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// Mount vue app
app.mount("#app");
