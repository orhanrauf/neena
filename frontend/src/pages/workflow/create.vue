<script setup lang="ts"></script>

<template>
  <VForm @submit.prevent="() => {}">
    <VRow class="match-height">
      <!-- Describe request -->
      <VCol cols="12" md="7">
        <DescribeRequest />
      </VCol>

      <!-- Instructions -->
      <VCol cols="12" md="5">
        <ProvideInstructions />
      </VCol>

      <!-- Meta data -->
      <VCol cols="12" md="12">
        <MetaData />
      </VCol>

      <!-- Buttons -->
      <VCol cols="12" md="12" class="d-flex gap-4 justify-end">
        <VBtn type="submit">Generate Flow</VBtn>

        <VBtn type="reset" color="secondary"> Create Manually </VBtn>
      </VCol>
    </VRow>
  </VForm>
</template>
