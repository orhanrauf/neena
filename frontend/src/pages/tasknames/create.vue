<script setup lang="ts">
import TaskForm from "@/components/tasknames/TaskForm.vue";
</script>

<template>
  <VRow class="match-height">
    <!-- Task form -->
    <VCol cols="12" md="9">
      <TaskForm />
    </VCol>

    <!-- View task -->
    <VCol cols="12" md="3">
      <ViewTask />
    </VCol>
  </VRow>
</template>
