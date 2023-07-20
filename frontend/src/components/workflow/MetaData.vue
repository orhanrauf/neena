<script setup lang="ts">
const props = defineProps<{
  modelValue: object;
}>();
const emit = defineEmits(["update:modelValue"]);

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>

<template>
  <VCard
    title="Metadata"
    subtitle="Specify your custom parameters for the request"
  >
    <VCardText>
      <VRow>
        <VCol cols="12" md="6">
          <AppTextField
            name="paramater name 1"
            label="Parameter name"
            v-model="value[0].name"
            required
          />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField
            name="paramater value 1"
            label="Parameter value"
            v-model="value[0].value"
            required
          />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField
            name="paramater name 2"
            v-model="value[1].name"
            required
          />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField
            name="paramater value 2"
            v-model="value[1].value"
            required
          />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField
            name="paramater name 3"
            v-model="value[2].name"
            required
          />
        </VCol>

        <VCol cols="12" md="6">
          <AppTextField
            name="paramater value 3"
            v-model="value[2].value"
            required
          />
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>
