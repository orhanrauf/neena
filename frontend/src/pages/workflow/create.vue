<script setup lang="ts">
import axios from "@axios";
import { requiredValidator } from "@validators";
import { VForm } from "vuetify/components/VForm";

const refVForm = ref<VForm>();
const showError = ref(false);

const errors = ref({
  body: undefined,
  instructions: undefined,
  metadata: [
    { name: undefined, value: undefined },
    { name: undefined, value: undefined },
    { name: undefined, value: undefined },
  ],
});

const getInitialForm = () => ({
  body: "I would like to make use of the discount that is given for customers under the age of 30.",
  instructions:
    "It's important that the customer is first verified with us. Check if their email is actually in the system. Do not give any details without verifying that the email is coupled to an account in our database.",
  metadata: [
    {
      name: "city",
      value: "New York",
    },
    {
      name: "email",
      value: "johdoe@gmail.com",
    },
    {
      name: "test",
      value: "test",
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
                    :name="`parameter name ${index + 1}`"
                    :label="index === 0 ? 'Parameter name' : ''"
                    v-model="form.metadata[index].name"
                    :rules="[requiredValidator]"
                    :error-messages="errors.metadata[index].name"
                  />
                </VCol>

                <VCol cols="12" md="6">
                  <AppTextField
                    :name="`parameter value ${index + 1}`"
                    :label="index === 0 ? 'Parameter value' : ''"
                    v-model="form.metadata[index].value"
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
