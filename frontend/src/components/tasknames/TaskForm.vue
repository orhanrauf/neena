<script setup lang="ts">
import { useTheme } from "vuetify";

const vuetifyTheme = useTheme();
</script>

<template>
  <VCard>
    <VCardText>
      <VForm @submit.prevent="() => {}">
        <div class="mb-4">
          <VLabel for="taskName" class="mb-1" text="Task name" />
          <VTextField id="taskName" placeholder="Verify- details" />
        </div>

        <div class="mb-4">
          <VLabel for="parameters" class="mb-1" text="Parameters" />
          <VTextarea
            id="parameters"
            placeholder="Object : details &#10;Callable : Condition"
            rows="2"
          />
        </div>

        <div class="mb-4">
          <VLabel for="output" class="mb-1" text="Output" />
          <VTextField id="output" placeholder="bool : verified" />
        </div>

        <div class="mb-4">
          <VLabel for="description" class="mb-1" text="Description" />
          <VTextarea
            id="description"
            placeholder="This is a long description of this task. In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available."
            rows="6"
          />
        </div>
      </VForm>
    </VCardText>
  </VCard>
</template>
