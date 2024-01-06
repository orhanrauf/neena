<script lang="ts" setup>
import { layoutConfig } from '@layouts'
import { can } from '@layouts/plugins/casl'
import { useLayoutConfigStore } from '@layouts/stores/config'
import type { NavLink } from '@layouts/types'
import { getComputedNavLinkToProp, getDynamicI18nProps, isNavLinkActive } from '@layouts/utils'

const props = defineProps<{
  item: NavLink
}>()

const configStore = useLayoutConfigStore()
const hideTitleAndBadge = configStore.isVerticalNavMini()


// Use useRouter and useRoute to get access to $router and $route
const router = useRouter();
const route = useRoute();

const isRequestCreate = computed(() => {
  return props.item.title === 'Create Request';
});

const className = computed(() => {
  if (isRequestCreate.value) {
    return 'head-item-style';
  } else if (isNavLinkActive(props.item, router)) {
    return 'router-link-active router-link-exact-active';
  }
  return ''
});
  
</script>

<template>
  <li
    v-if="can(item.action, item.subject)"
    :class="['nav-link', { disabled: item.disable }]"
  >
  <Component
      :is="item.to ? 'RouterLink' : 'a'"
      v-bind="getComputedNavLinkToProp(item)"
      :class="className"
    >
      <Component
        :is="layoutConfig.app.iconRenderer || 'div'"
        v-bind="item.icon || layoutConfig.verticalNav.defaultNavItemIconProps"
        class="nav-item-icon"
      />
      <TransitionGroup name="transition-slide-x">
        <!-- 👉 Title -->
        <Component
          :is="layoutConfig.app.i18n.enable ? 'i18n-t' : 'span'"
          v-show="!hideTitleAndBadge"
          key="title"
          class="nav-item-title"
          v-bind="getDynamicI18nProps(item.title, 'span')"
        >
          {{ item.title }}
        </Component>

        <!-- 👉 Badge -->
        <Component
          :is="layoutConfig.app.i18n.enable ? 'i18n-t' : 'span'"
          v-if="item.badgeContent"
          v-show="!hideTitleAndBadge"
          key="badge"
          class="nav-item-badge"
          :class="item.badgeClass"
          v-bind="getDynamicI18nProps(item.badgeContent, 'span')"
        >
          {{ item.badgeContent }}
        </Component>
      </TransitionGroup>
    </Component>
  </li>
</template>

<style lang="scss" scoped>


.layout-vertical-nav {
  .nav-link a {
    display: flex;
    align-items: center;

    &.head-item-style {
      background-color: rgb(var(--v-theme-primary)) !important;
      
      color: white;
      font-weight: bold;

    }
  }

}
</style>
