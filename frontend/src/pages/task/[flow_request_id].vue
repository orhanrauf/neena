<script setup lang="ts">
const route = useRoute();

const flowRequestId = route.params.flow_request_id;
</script>

<template>
  <div>
    <DrawFlow />
  </div>
</template>
