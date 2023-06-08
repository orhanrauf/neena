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
          <VLabel for="porometers" class="mb-1" text="Porometers" />
          <VTextarea
            id="porometers"
            placeholder="Object : details \nCallable : Condition"
            rows="4"
          />
        </div>

        <div class="mb-4">
          <VLabel for="output" class="mb-1" text="Output" />
          <VTextField id="output" placeholder="bool : verified" />
        </div>

        <div class="mb-4">
          <VLabel
            for="descriptionShort"
            class="mb-1"
            text="Description ( Short )"
          />
          <VTextarea
            id="descriptionShort"
            placeholder="Verifies is a details matches the given condition."
            rows="3"
          />
        </div>

        <div>
          <VLabel
            for="descriptionLong"
            class="mb-1"
            text="Description ( Long )"
          />
          <VTextarea
            id="descriptionLong"
            placeholder="This function takes in tow parameters, one which presents a details of a  customers, employee or product. The other is a lamsla function that encodes the condition that needs to be met."
            rows="2"
          />
        </div>
      </VForm>
    </VCardText>
  </VCard>
</template>
