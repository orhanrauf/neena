<script setup lang="ts">
import { useTheme } from "vuetify";

const vuetifyTheme = useTheme();
</script>

<template>
  <VCard
    title="Metadata"
    subtitle="Specify your custom parameters for the request"
    class="border"
  >
    <VCardText>
      <VRow>
        <VCol cols="12" md="6">
          <AppTextField label="Parameter name" placeholder="city" />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField label="Parameter value" placeholder="New York" />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField placeholder="email" />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField placeholder="johndoe@gmail.com" />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField />
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>
