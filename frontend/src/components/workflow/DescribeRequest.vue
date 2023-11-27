<script setup lang="ts">
const props = defineProps<{
  modelValue: string;
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
  <VCard title="Describe Request" class="border">
    <VCardText>
      <VTextarea v-model="value" name="body" rows="10" required />
    </VCardText>
  </VCard>
</template>
