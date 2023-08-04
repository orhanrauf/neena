<script setup lang="ts">
defineProps<{
  name: string;
  type: string;
  isOutput: boolean;
}>();
</script>

<template>
  <div class="node-footer">
    <h1>
      {{ name }}: <span :class="`text-${type}`">{{ type }}</span>
    </h1>
    <p>{{ isOutput ? "OUTPUT" : "INPUT" }}</p>
  </div>
</template>

<style scoped>
.node-footer {
  position: relative;
  padding: 0 15px;
  background-color: #f6f6f7;
}

h1 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1d2aad;
  padding: 10px 0;
}

p {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 13px;
  font-weight: 600;
  color: #b7b5be;
}

.text-str {
  color: #28c76f;
}
.text-int {
  color: #67b6f0;
}
.text-list,
.text-object,
.text-bool {
  color: #7367f0;
}
</style>
