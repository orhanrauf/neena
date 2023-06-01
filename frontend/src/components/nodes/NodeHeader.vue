<script>
import { defineComponent } from 'vue'

export default defineComponent({
  props: ['title'],
})
</script>

<template>
  <div class="header">
    {{ title }}
  </div>
</template>

<style scoped>
div {
  background: #494949;
  margin-block: -15px 15px;
  margin-inline: -15px;
  padding-block: 10px;
  padding-inline: 15px;
}
</style>
