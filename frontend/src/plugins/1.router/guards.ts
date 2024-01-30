import type { Router } from 'vue-router'
import store from '@/store'

// TODO: Add vuex store check if token refresh is required
export const setupGuards = (router: Router) => {
  // 👉 router.beforeEach
  // Docs: https://router.vuejs.org/guide/advanced/navigation-guards.html#global-before-guards
  router.beforeEach(to => {

    const isLoggedIn = store.state.auth.token !== null && Object.keys(store.state.auth.token).length !== 0;

    /*
      * If it's a public route continue navigation.
      * This kind of pages are allowed to be visited by login & non-login users without any restrictions.
      * Examples of public routes are 404, under maintenance, etc.
    */
    if (to.meta.public) {
      return
    }

    /*
      If user is logged in and is trying to access login like page, redirect to home
      else allow visiting the page
      (WARN: Don't allow executing further by return statement because next code will check for permissions)
      */
    if (to.meta.unauthenticatedOnly) {
      if (isLoggedIn) {
        return '/' // send to default page (that gets picked up by router)
      }
      else {
        return undefined
      }
    }
    
    if (!isLoggedIn) {
      return '/login' // send to login
    }
  })

}
