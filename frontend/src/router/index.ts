import { setupLayouts } from "virtual:generated-layouts";
import { createRouter, createWebHistory } from "vue-router";
import { isUserLoggedIn } from "./utils";
import routes from "~pages";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: (to) => {
        const userData = JSON.parse(localStorage.getItem("userData") || "{}");

        if (userData) {
          return { name: "index" };
        }

        return { name: "login", query: to.query };
      },
    },
    ...setupLayouts(routes),
  ],
});

// Docs: https://router.vuejs.org/guide/advanced/navigation-guards.html#global-before-guards
router.beforeEach((to) => {
  const isLoggedIn = isUserLoggedIn();

  if (isLoggedIn) {
    if (to.meta.redirectIfLoggedIn) {
      return "/";
    }
  } else if (!to.meta.redirectIfLoggedIn) {
    return {
      name: "login",
      query: { to: to.name !== "index" ? to.fullPath : undefined },
    };
  }
});

export default router;
