<script setup>
import { getCurrentInstance, nextTick, onMounted, readonly, ref } from "vue";
import NodeHeader from "./NodeHeader.vue";
import NodeBody from "@/components/nodes/NodeBody.vue";

const el = ref(null);
const nodeId = ref(0);
let df = null;
const url = ref("");
const method = ref("get");
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

const updateSelect = (value) => {
  dataNode.value.data.method = value;
  df.updateNodeDataFromId(nodeId.value, dataNode.value);
};

onMounted(async () => {
  await nextTick();
  nodeId.value = el.value.parentElement.parentElement.id.slice(5);
  dataNode.value = df.getNodeFromId(nodeId.value);

  url.value = dataNode.value.data.url;
  method.value = dataNode.value.data.method;

  console.log(dataNode.value.data);
});
</script>

<template>
  <div ref="el" @dblclick="showDrawer = true">
    <NodeHeader> {{ dataNode.data?.task_name }} </NodeHeader>
    <NodeBody> {{ dataNode.data?.description }} </NodeBody>
    <NodeFooter
      :name="dataNode.data?.output_name"
      :type="dataNode.data?.output_type"
      :is-output="true"
    />

    <Drawer v-model="showDrawer" />
  </div>
</template>
