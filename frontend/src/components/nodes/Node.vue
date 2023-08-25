<script setup>
import { getCurrentInstance, nextTick, onMounted, ref } from "vue";
import NodeHeader from "./NodeHeader.vue";
import NodeBody from "@/components/nodes/NodeBody.vue";

const el = ref(null);
const nodeId = ref(0);
let df = null;

const showDrawer = ref(false);

df = getCurrentInstance().appContext.config.globalProperties.$df.value;

const getDataNode = () => {
  return df.getNodeFromId(nodeId.value);
};

const dataNode = ref({});

const update = () => {
  dataNode.value = getDataNode();
};

onMounted(async () => {
  await nextTick();
  nodeId.value = el.value.parentElement.parentElement.id.slice(5);
  dataNode.value = getDataNode();
});
</script>

<template>
  <div ref="el" @dblclick="showDrawer = true">
    <template v-if="dataNode.data">
      <!-- NODE -->
      <NodeHeader>
        {{ dataNode.data.task_definition.task_name }}
      </NodeHeader>
      <NodeBody>
        {{ dataNode.data.task_definition.description }}
      </NodeBody>
      <NodeFooter
        :name="dataNode.data.task_definition.output_name"
        :type="dataNode.data.task_definition.output_type"
        :is-output="true"
      />

      <!-- DRAWER -->
      <Drawer
        v-model="showDrawer"
        :df="df"
        :node-id="nodeId"
        @update="update"
      />
    </template>
  </div>
</template>
