import { createApp } from 'vue'

import App from '@/App.vue'
import { registerPlugins } from '@core/utils/plugins'
import ElementPlus from "element-plus";
import store from './store';  // Import the store


// Styles
import '@core/scss/template/index.scss'
import '@styles/styles.scss'
import "element-plus/dist/index.css";

// Create vue app
const app = createApp(App)

// Register plugins
registerPlugins(app)

app.use(ElementPlus)

// Use the Vuex store
app.use(store); 

// Mount vue app
app.mount('#app')
