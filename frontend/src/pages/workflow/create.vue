<script setup lang="ts">
import axios from "@axios";
import { requiredValidator } from "@validators";
import { VForm } from "vuetify/components/VForm";

const refVForm = ref<VForm>();
const showError = ref(false);

const errors = reactive({
  body: undefined,
  instructions: undefined,
  metadata: [
    { name: undefined, value: undefined },
    { name: undefined, value: undefined },
  ],
});

const getInitialForm = () => ({
  body: "",
  instructions: "",
  metadata: [
    {
      name: "",
      value: "",
    },
    {
      name: "",
      value: "",
    },
  ],
});

const form = reactive(getInitialForm());

const onSubmit = () => {
  // Validate form
  refVForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid) createFlow();
  });
};

const createFlow = () => {
  // Send post request to API
  axios
    .post("/v1/flow_requests", {
      request_metadata: form.metadata,
      request_instructions: form.instructions,
      request_body: form.body,
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

const handleInput = (index, event) => {
  if (index === form.metadata.length - 1 && event.target.value) {
    errors.metadata.push({ name: undefined, value: undefined });
    form.metadata.push({ name: "", value: "" });
  }
};
</script>

<template>
  <VForm ref="refVForm" @submit.prevent="onSubmit">
    <VAlert v-model="showError" color="error" class="mb-3" closable>
      Something went wrong with the API call. Please try again later.
    </VAlert>

    <VRow class="match-height">
      <!-- Describe request -->
      <VCol cols="12" md="7">
        <VCard title="Describe Request">
          <VCardText>
            <VTextarea
              v-model="form.body"
              name="body"
              rows="10"
              required
              placeholder="I would like to make use of the discount that is given for customers under the age of 30."
              :rules="[requiredValidator]"
              :error-messages="errors.body"
            />
          </VCardText>
        </VCard>
      </VCol>

      <!-- Instructions -->
      <VCol cols="12" md="5">
        <VCard title="Provide instructions">
          <VCardText>
            <VTextarea
              v-model="form.instructions"
              name="instructions"
              rows="10"
              required
              placeholder="It's important that the customer is first verified with us. Check if their email is actually in the system. Do not give any details without verifying that the email is coupled to an account in our database."
              :rules="[requiredValidator]"
              :error-messages="errors.instructions"
            />
          </VCardText>
        </VCard>
      </VCol>

      <!-- Meta data -->
      <VCol cols="12" md="12">
        <VCard
          title="Metadata"
          subtitle="Specify your custom parameters for the request"
        >
          <VCardText>
            <VRow>
              <template v-for="(meta, index) in form.metadata" :key="index">
                <VCol cols="12" md="6">
                  <AppTextField
                    v-model="form.metadata[index].name"
                    :name="`parameter name ${index + 1}`"
                    :label="index === 0 ? 'Parameter name' : ''"
                    :placeholder="index === 0 ? 'city' : ''"
                    :rules="[requiredValidator]"
                    :error-messages="errors.metadata[index].name"
                    @input="handleInput(index, $event)"
                  />
                </VCol>

                <VCol cols="12" md="6">
                  <AppTextField
                    v-model="form.metadata[index].value"
                    :name="`parameter value ${index + 1}`"
                    :label="index === 0 ? 'Parameter value' : ''"
                    :placeholder="index === 0 ? 'New York' : ''"
                    :rules="[requiredValidator]"
                    :error-messages="errors.metadata[index].value"
                  />
                </VCol>
              </template>
            </VRow>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Buttons -->
      <VCol cols="12" md="12" class="d-flex gap-4 justify-end">
        <VBtn type="button">Generate Flow</VBtn>

        <VBtn type="submit" color="secondary"> Create Manually </VBtn>
      </VCol>
    </VRow>
  </VForm>
</template>
