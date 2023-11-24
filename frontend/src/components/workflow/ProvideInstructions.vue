<script setup lang="ts">
import { useTheme } from "vuetify";

const vuetifyTheme = useTheme();
</script>

<template>
  <VCard title="Provide instructions" class="border">
    <VCardText>
      <VTextarea
        placeholder="It’s important that the customer is first verified with us. Check if their email is actually in the system. &#10;&#10;Do not give any details without verifying that the email is coupled to an account in our database."
        rows="10"
      />
    </VCardText>
  </VCard>
</template>
