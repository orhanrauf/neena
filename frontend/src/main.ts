import { createApp } from 'vue'

import App from '@/App.vue'
import { registerPlugins } from '@core/utils/plugins'
import ElementPlus from "element-plus";
import store from './store';  // Import the store
import { createAuth0 } from '@auth0/auth0-vue';

// Styles
import '@core/scss/template/index.scss'
import '@styles/styles.scss'
import "element-plus/dist/index.css";

// Create vue app
const app = createApp(App)

// Auth0 configuration
const auth0 = createAuth0({
    domain: import.meta.env.VITE_APP_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_APP_AUTH0_CLIENT_ID,
    authorizationParams :{
      redirect_uri: window.location.origin,
    }
    // Add any other configuration parameters as required
  });
  
app.use(auth0);

// Register plugins
registerPlugins(app)

app.use(ElementPlus)

// Use the Vuex store
app.use(store); 

// Mount vue app
app.mount('#app')