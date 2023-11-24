<script setup lang="ts">
import { useTheme } from "vuetify";

const vuetifyTheme = useTheme();
</script>

<template>
  <VCard title="Describe Request" class="border">
    <VCardText>
      <VTextarea
        placeholder="I would like to make use of the discount that is given for customers under the age of 30."
        rows="10"
      />
    </VCardText>
  </VCard>
</template>
