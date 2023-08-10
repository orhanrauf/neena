<script setup>
import { getCurrentInstance, nextTick, onMounted, readonly, ref } from "vue";
import NodeHeader from "./NodeHeader.vue";
import NodeBody from "@/components/nodes/NodeBody.vue";

const el = ref(null);
const nodeId = ref(0);
let df = null;
const dataNode = ref({});

const showDrawer = ref(false);

const options = readonly([
  {
    value: "get",
    label: "GET",
  },
  {
    value: "post",
    label: "POST",
  },
]);

df = getCurrentInstance().appContext.config.globalProperties.$df.value;

onMounted(async () => {
  await nextTick();
  nodeId.value = el.value.parentElement.parentElement.id.slice(5);
  dataNode.value = df.getNodeFromId(nodeId.value);
});

const update = (taskOperation) => {
  const dataNode2 = Object.assign({}, taskOperation.value); // Create a local copy
  dataNode.value.data = dataNode2;
};
</script>

<template>
  <div ref="el" @dblclick="showDrawer = true">
    <template v-if="dataNode.data">
      <!-- NODE -->
      <NodeHeader> {{ dataNode.data.name }} </NodeHeader>
      <NodeBody> {{ dataNode.data.task_definition.description }} </NodeBody>
      <NodeFooter
        :name="dataNode.data.task_definition.output_name"
        :type="dataNode.data.task_definition.output_type"
        :is-output="true"
      />

      <!-- DRAWER -->
      <Drawer
        v-model="showDrawer"
        :data-node="dataNode.data"
        @update:data-node="update"
      />
    </template>
  </div>
</template>
