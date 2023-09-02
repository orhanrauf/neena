<script setup lang="ts">
import { VForm } from "vuetify/components/VForm";
import { requiredValidator } from "@validators";
import { computed, reactive } from "vue"
import axios from "@axios";
import PythonCode from "@/components/PythonCode.vue";

const route = useRoute();
const taskDefinitionId = route.params.task_definition_id as string;

onMounted(async () => {
  axios.get(`/v1/task_definitions/?id=${taskDefinitionId}`)
    .then((response) => {
      const data = response.data.data;

      form.name = data.name;
      form.parameters = data.parameters;
      form.output = data.output;
      form.description = data.description;
      form.python = data.python;
    })
    .catch(() => {});
});

const form = reactive({
  name: "",
  parameters: [],
  output: "",
  description: "",
  python: "",
});

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
</script>

<template>
  <VForm ref="refVForm" @submit.prevent="() => {}">
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
              />
            </div>

            <div class="mb-4">
              <VLabel for="parameters" class="mb-1" text="Parameters" />
              <VTextarea
                v-model="formattedParameters"
                id="parameters"
                rows="2"
              />
            </div>

            <div class="mb-4">
              <VLabel for="output" class="mb-1" text="Output" />
              <VTextField
                v-model="form.output"
                id="output"
              />
            </div>

            <div class="mb-4">
              <VLabel for="description" class="mb-1" text="Description" />
              <VTextarea
                v-model="form.description"
                id="description"
                rows="6"
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
              <PythonCode :code="form.python" />
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Buttons -->
      <!--      <VCol cols="12" md="12" class="d-flex gap-4 justify-end">-->
      <!--        <VBtn type="submit" color="primary"> Create</VBtn>-->
      <!--      </VCol>-->
    </VRow>
  </VForm>
</template>
