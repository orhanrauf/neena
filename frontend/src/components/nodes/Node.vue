<script>
import {
  defineComponent,
  getCurrentInstance,
  nextTick,
  onMounted,
  readonly,
  ref,
} from "vue";
import NodeHeader from "./NodeHeader.vue";
import NodeBody from "@/components/nodes/NodeBody.vue";
export default defineComponent({
  components: {
    NodeBody,
    NodeHeader,
  },
  setup() {
    const el = ref(null);
    const nodeId = ref(0);
    let df = null;
    const url = ref("");
    const method = ref("get");
    const dataNode = ref({});

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
    });

    return {
      el,
      url,
      method,
      options,
      updateSelect,
    };
  },
});
</script>

<template>
  <div ref="el">
    <NodeHeader> look_up_acc_number_by_email </NodeHeader>
    <NodeBody>Looks up account number based on given email.</NodeBody>
    <NodeFooter name="acc_number" type="string" :is-output="true" />
  </div>
</template>
