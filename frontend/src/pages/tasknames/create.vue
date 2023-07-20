<script setup lang="ts">
import { VForm } from "vuetify/components/VForm";
import { requiredValidator } from "@validators";
import { computed } from "vue";
import axios from "@axios";

const refVForm = ref<VForm>();
const showError = ref(false);

const errors = ref({
  name: undefined,
  parameters: undefined,
  output: undefined,
  description: undefined,
  python: undefined,
});

const getInitialForm = () => ({
  name: "Verify-details",
  parameters: [
    {
      data_type: "object",
      name: "details",
      position: 0,
    },
    {
      data_type: "callable",
      name: "condition",
      position: 1,
    },
  ],
  output: "bool : verified",
  description:
    "This is a long description of this task. In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.",
  python: "",
});

const form = reactive(getInitialForm());

const formattedParameters = computed({
  get() {
    return form.parameters
      .map((param) => {
        return `${param.data_type} : ${param.name}`;
      })
      .join("\n");
  },
  set(newValue) {
    const lines = newValue.split("\n");

    form.parameters = lines.map((line, index) => {
      const [data_type, name] = line.split(" : ");
      return { data_type: data_type ?? "", name: name ?? "", position: index };
    });
  },
});

const outputType = computed(() => {
  return form.output.split(" : ")[0];
});
const outputName = computed(() => {
  return form.output.split(" : ")[1];
});

const onSubmit = () => {
  // Validate form
  refVForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid) createTaskDefinition();
  });
};

const createTaskDefinition = () => {
  // Send post request to API
  axios
    .post("/v1/task_definitions", {
      task_name: form.name,
      parameters: form.parameters,
      output_type: outputType.value,
      output_name: outputName.value,
      description: form.description,
      python_code: form.python,
    })
    .then((response) => {
      Object.assign(form, getInitialForm());
      refVForm.value.resetValidation();
    })
    .catch((error) => {
      showError.value = true;
      console.error(error);
    });
};
</script>

<template>
  <VForm ref="refVForm" @submit.prevent="onSubmit">
    <VAlert v-model="showError" color="error" class="mb-3" closable>
      Something went wrong with the API call. Please try again later.
    </VAlert>

    <VRow class="match-height">
      <!-- Task form -->
      <VCol cols="12">
        <VCard>
          <VCardText>
            <div class="mb-4">
              <VLabel for="taskName" class="mb-1" text="Task name" />
              <VTextField
                v-model="form.name"
                id="taskName"
                :rules="[requiredValidator]"
                :error-messages="errors.name"
              />
            </div>

            <div class="mb-4">
              <VLabel for="parameters" class="mb-1" text="Parameters" />
              <VTextarea
                v-model="formattedParameters"
                id="parameters"
                rows="2"
                :rules="[requiredValidator]"
                :error-messages="errors.parameters"
              />
            </div>

            <div class="mb-4">
              <VLabel for="output" class="mb-1" text="Output" />
              <VTextField
                v-model="form.output"
                id="output"
                :rules="[requiredValidator]"
                :error-messages="errors.output"
              />
            </div>

            <div class="mb-4">
              <VLabel for="description" class="mb-1" text="Description" />
              <VTextarea
                v-model="form.description"
                id="description"
                rows="6"
                :rules="[requiredValidator]"
                :error-messages="errors.description"
              />
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- View task -->
      <VCol cols="12">
        <VCard title="View Task">
          <VCardText>
            <div>
              <VLabel
                for="python"
                class="mb-1"
                text="Task definition (Python)"
              />
              <VTextarea
                v-model="form.python"
                id="python"
                rows="6"
                :rules="[requiredValidator]"
                :error-messages="errors.body"
              />
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Buttons -->
      <VCol cols="12" md="12" class="d-flex gap-4 justify-end">
        <VBtn type="submit" color="primary"> Create</VBtn>
      </VCol>
    </VRow>
  </VForm>
</template>
