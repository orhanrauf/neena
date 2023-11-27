<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  df: any;
  nodeId: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", v: boolean): void;
  (e: "update"): void;
}>();

const show = computed({
  get() {
    localDataNode.value = getDataNode();

    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});

let df = props.df;
const getDataNode = () => {
  return df.getNodeFromId(props.nodeId);
};

let localDataNode = ref(getDataNode());

const save = () => {
  update();
  emit("update");

  show.value = false;
};

const getNodeIdByTaskName = (taskName) => {
  const nodes = df.export().drawflow.Home.data;
  let nodeId = null;

  Object.keys(nodes).forEach((key) => {
    const node = nodes[key];
    if (node.data.task_definition.task_name === taskName) {
      nodeId = node.id;
    }
  });

  return nodeId;
};

const update = () => {
  createConnections(localDataNode.value.data.task_definition.parameters);

  df.updateNodeDataFromId(props.nodeId, localDataNode.value.data);

  localDataNode.value = getDataNode();
};

const createConnections = (parameters) => {
  // Add connections for each of the parameters
  parameters.forEach((parameter, index) => {
    if (!parameter.value || parameter.source !== "@tasks()") {
      return;
    }

    const splitValue = parameter.value.split(".");

    if (splitValue[1] === "output") {
      const outputNode = getNodeIdByTaskName(splitValue[0]);

      if (outputNode) {
        df.addConnection(
          outputNode,
          props.nodeId,
          "output_1",
          `input_${index + 1}`
        );
      }
    }
  });
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
            v-model="localDataNode.data.task_definition.task_name"
          />
        </div>
      </template>

      <!-- DESCRIPTION -->
      <h2 class="fs-2 font-weight-medium mb-2">Description</h2>
      <p class="px-0 font-weight-light text-sm-body-1">
        {{ localDataNode.data.task_definition.description }}
      </p>

      <!-- PARAMETERS -->
      <h2 class="fs-2 font-weight-medium mb-0 mt-8">Parameters</h2>
      <VCard
        v-for="(parameter, index) in localDataNode.data.task_definition
          .parameters"
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
            {{ localDataNode.data.task_definition.output_name }}:
            <span
              :class="`text-${localDataNode.data.task_definition.output_type}`"
            >
              {{ localDataNode.data.task_definition.output_type }}
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
