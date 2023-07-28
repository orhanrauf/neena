<script>
import { defineComponent } from "vue";

export default defineComponent({
  props: ["title"],
});
</script>

<template>
  <div class="header">
    <slot />
  </div>
</template>

<style scoped>
div {
  background: #d5ebf8;

  margin-block: -15px 15px;
  margin-inline: -15px;
  padding-block: 10px;
  padding-inline: 15px;

  font-size: 18px;
  color: #6f6b7d;
}
</style>
