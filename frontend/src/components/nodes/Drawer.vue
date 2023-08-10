<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  dataNode: object;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", v: boolean): void;
  (e: "update:dataNode", v: object): void;
}>();

const show = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});

const dataNode = Object.assign({}, props.dataNode); // Create a local copy
const taskOperation = ref(dataNode);

const save = () => {
  emit("update:dataNode", taskOperation);
  show.value = false;
};

const sources = ["@tasks()", "@metadata()"];
</script>

<template>
  <teleport to="body">
    <el-drawer v-model="show" direction="rtl">
      <template #header="{ close, titleId, titleClass }">
        <div class="pr-3">
          <h2 :id="titleId" :class="titleClass" class="fs-2 font-weight-medium">
            Edit Task Operation
          </h2>

          <!-- NAME -->
          <AppTextField
            class="mt-1"
            id="name"
            placeholder="Name"
            persistent-placeholder
            v-model="taskOperation.name"
          />
        </div>
      </template>

      <!-- DESCRIPTION -->
      <h2 class="fs-2 font-weight-medium mb-2">Description</h2>
      <p class="px-0 font-weight-light text-sm-body-1">
        {{ taskOperation.task_definition.description }}
      </p>

      <!-- PARAMETERS -->
      <h2 class="fs-2 font-weight-medium mb-0 mt-8">Parameters</h2>
      <VCard
        v-for="(parameter, index) in taskOperation.task_definition.parameters"
        :key="index"
        flat
        border
        class="mt-4 py-4 px-5"
      >
        <VRow>
          <!-- Name -->
          <VCol cols="12">
            <VRow no-gutters>
              <VCol cols="12" md="3" class="d-flex align-items-center">
                <label
                  class="v-label text-body-2 text-high-emphasis"
                  for="name"
                >
                  Name:
                </label>
              </VCol>

              <VCol cols="12" md="9">
                <AppTextField id="name" :value="parameter.name" readonly />
              </VCol>
            </VRow>
          </VCol>

          <!-- Source -->
          <VCol cols="12">
            <VRow no-gutters>
              <VCol cols="12" md="3" class="d-flex align-items-center">
                <label
                  class="v-label text-body-2 text-high-emphasis"
                  for="source"
                >
                  Source:
                </label>
              </VCol>

              <VCol cols="12" md="9">
                <select id="source" v-model="parameter.source" class="w-100">
                  <option v-for="item in sources" :value="item">
                    {{ item }}
                  </option>
                </select>
              </VCol>
            </VRow>
          </VCol>

          <!-- Data Type -->
          <VCol cols="12">
            <VRow no-gutters>
              <VCol cols="12" md="3" class="d-flex align-items-center">
                <label
                  class="v-label text-body-2 text-high-emphasis"
                  for="dataType"
                >
                  Type:
                </label>
              </VCol>

              <VCol cols="12" md="9">
                <AppTextField
                  id="dataType"
                  :value="parameter.data_type"
                  readonly
                />
              </VCol>
            </VRow>
          </VCol>

          <!-- Value -->
          <VCol cols="12">
            <VRow no-gutters>
              <VCol cols="12" md="3" class="d-flex align-items-center">
                <label
                  class="v-label text-body-2 text-high-emphasis"
                  for="value"
                >
                  Value:
                </label>
              </VCol>

              <VCol cols="12" md="9">
                <AppTextField id="value" v-model="parameter.value" />
              </VCol>
            </VRow>
          </VCol>

          <!-- Nullable -->
          <VCol cols="12">
            <VRow no-gutters>
              <VCol cols="12" md="3" class="d-flex align-items-center">
                <label
                  class="v-label text-body-2 text-high-emphasis"
                  for="mobile"
                  >Nullable:</label
                >
              </VCol>

              <VCol class="d-flex justify-end" cols="12" md="9">
                <VSwitch
                  color="primary"
                  hide-details
                  :inset="false"
                  :model-value="true"
                />
              </VCol>
            </VRow>
          </VCol>
        </VRow>
      </VCard>

      <!-- OUTPUT -->
      <div class="mt-8 d-flex justify-space-between align-center">
        <div>
          <h2 class="fs-2 font-weight-medium">Output</h2>
          <p class="px-0 mb-0">
            {{ taskOperation.task_definition.output_name }}:
            <span :class="`text-${taskOperation.task_definition.output_type}`">
              {{ taskOperation.task_definition.output_type }}
            </span>
          </p>
        </div>

        <!-- SAVE -->
        <VBtn @click="save"> Save </VBtn>
      </div>
    </el-drawer>
  </teleport>
</template>

<style scoped>
.text-str {
  color: #28c76f;
}
.text-int {
  color: #67b6f0;
}
.text-list,
.text-object,
.text-bool {
  color: #7367f0;
}
</style>
