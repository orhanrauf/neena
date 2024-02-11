<!-- ❗Errors in the form are set on line 60 -->
<script setup lang="ts">
import { useGenerateImageVariant } from '@core/composable/useGenerateImageVariant'
import authV2LoginIllustrationBorderedDark from '@images/pages/auth-v2-login-illustration-bordered-dark.png'
import authV2LoginIllustrationBorderedLight from '@images/pages/auth-v2-login-illustration-bordered-light.png'
import authV2LoginIllustrationDark from '@images/pages/auth-v2-login-illustration-dark.png'
import authV2LoginIllustrationLight from '@images/pages/auth-v2-login-illustration-light.png'
import authV2MaskDark from '@images/pages/misc-mask-dark.png'
import authV2MaskLight from '@images/pages/misc-mask-light.png'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'
import { themeConfig } from '@themeConfig'
import { useAuth0 } from '@auth0/auth0-vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import {watch} from 'vue';
import { User } from '@/types';


const authThemeImg = useGenerateImageVariant(authV2LoginIllustrationLight, authV2LoginIllustrationDark, authV2LoginIllustrationBorderedLight, authV2LoginIllustrationBorderedDark, true)

const authThemeMask = useGenerateImageVariant(authV2MaskLight, authV2MaskDark)

""
definePage({
  meta: {
    layout: 'blank',
    unauthenticatedOnly: true,
  },
})
const { loginWithRedirect, isAuthenticated, getAccessTokenSilently, user } = useAuth0();
const store = useStore();
const router = useRouter();

watch(() => isAuthenticated.value, async (newValue) => {
  if (newValue) {
    try {
      const token = await getAccessTokenSilently();
      console.log('user', user.value); 
      
      store.commit('saveToken', token);
      await store.commit('setUser', user.value);
      await store.commit('setAuthDateTimestamp', Date.now());

      const userNeenaModel: User = {
        email: user.value.email,
        auth0_id: user.value.sub,
        full_name: user.value.name,
      };

      const response = await http.post('users/create_if_not_exists', userNeenaModel)
      console.log('response', response);

      router.push('/');
    } catch (error) {
      console.error('Error getting token or redirecting:', error);
    }
  }
});

const onLogin = async () => {
  await loginWithRedirect()
}

const onSignUp = async () => {
  await loginWithRedirect()
}

</script>

<template>
  <VRow
    no-gutters
    class="auth-wrapper bg-surface"
  >
    <VCol
      lg="8"
      class="d-none d-lg-flex"
    >
      <div class="position-relative bg-background rounded-lg w-100 ma-8 me-0">
        <div class="d-flex align-center justify-center w-100 h-100">
          <VImg
            max-width="505"
            :src="authThemeImg"
            class="auth-illustration mt-16 mb-2"
          />
        </div>

        <VImg
          :src="authThemeMask"
          class="auth-footer-mask"
        />
      </div>
    </VCol>

    <VCol
      cols="12"
      lg="4"
      class="auth-card-v2 d-flex align-center justify-center"
    >
    
    <div class="login-view">
      <div class="login-container">
        <h1 class="title">Get started</h1>
        <div class="buttons">
          <button class="login-button" @click="onLogin">Log in</button>
          <button class="signup-button" @click="onSignUp">Sign up</button>
        </div>
      </div>
      <footer class="login-footer">
        <div class="app-logo-and-title">
          <VNodeRenderer
          class="logo"
            :nodes="themeConfig.app.logo"
          />
          <h4 class="text-h3 mb-1 app-title">{{ themeConfig.app.title }}</h4>
        </div>

        <a href="https://openai.com/terms/" target="_blank">Terms of use</a>
        <a href="https://openai.com/privacy/" target="_blank">Privacy policy</a>
      </footer>
    </div>

    </VCol>
  </VRow>
</template>

<style scoped>
.login-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  color: #fff;
  justify-content: center;
  align-items: center;
}

.login-container {
  text-align: center;
  margin-bottom: 50px;
}

.title {
  margin-bottom: 20px;
}

.buttons {
  margin-bottom: 20px;
}

button {
  padding: 10px 60px;
  margin: 0 10px;
  border: none;
  color: #fff;
  background-color: #5865f2;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #43458b;
}

.login-footer {
  position: absolute;
  bottom: 10px;
  text-align: center;
  width: 100%;
}

.login-footer a {
  color: #696969;
  text-decoration: none;
  margin: 0 10px;
  font-size: 14px;
}

.app-logo-and-title {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.logo {
  /* Adjust the size of the logo as needed */
  height: 20px; /* Example size */
  width: auto;
  margin-right: 7px; /* Spacing between logo and title */
}

.app-title {
  margin: 0;
  font-size: 2em; /* Adjust as needed */
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>


<style lang="scss">
@use "@core/scss/template/pages/page-auth.scss";
</style>
