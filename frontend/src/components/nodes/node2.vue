<template>
  <div ref="el">
    <NodeHeader title="Script" />
    <p>Open in navbar</p>
    <el-button type="info" size="small" @click="drawer = true">Edit</el-button>

    <teleport to="body">
      <el-drawer
        v-model="drawer"
        :direction="direction"
        :before-close="handleClose" class=" border"
      >
        <template #header="{ close, titleId, titleClass }">
          <div>
            <h2
              :id="titleId"
              :class="titleClass"
              class="fs-2 font-weight-medium"
            >
              Edit Task Operation
            </h2>

            <p class="mx-0">Lookup detail by acc number</p>
          </div>
        </template>

        <h2 class="fs-2 font-weight-medium mb-2">Description</h2>
        <p class="font-weight-light text-sm-body-1">
          Icing pastry pudding oat cake. Lemon drops cotton candy caramels cake
          caramels sesame snaps powder. Bear claw candy topping. Tootsie roll
          fruitcake cookie. Dessert topping pie. Jujubes wafer carrot cake
          jelly. Bonbon jelly-o jelly-o ice cream jelly beans candy canes cake
          bonbon. Cookie jelly beans marshmallow jujubes sweet.
        </p>

        <h2 class="fs-2 font-weight-medium mb-2 mt-8">Parameters</h2>
        <VCard flat border class="py-4 px-5">
          <VForm @submit.prevent="() => {}">
            <VRow>
              <VCol cols="12">
                <VRow no-gutters>
                  <!-- Type -->
                  <VCol cols="12" md="3" class="d-flex align-items-center">
                    <label
                      class="v-label text-body-2 text-high-emphasis"
                      for="firstName"
                      >Type:</label
                    >
                  </VCol>

                  <VCol cols="12" md="9">
                    <AppTextField
                      id="firstName"
                      placeholder="int"
                      persistent-placeholder
                    />
                  </VCol>
                </VRow>
              </VCol>

              <VCol cols="12">
                <VRow no-gutters>
                  <!-- Value -->
                  <VCol cols="12" md="3" class="d-flex align-items-center">
                    <label
                      class="v-label text-body-2 text-high-emphasis"
                      for="email"
                      >Value:</label
                    >
                  </VCol>

                  <VCol cols="12" md="9">
                    <AppTextField
                      id="email"
                      placeholder="tasks()."
                      persistent-placeholder
                    />
                  </VCol>
                </VRow>
              </VCol>

              <VCol cols="12">
                <VRow no-gutters>
                  <!-- Source -->
                  <VCol cols="12" md="3" class="d-flex align-items-center">
                    <label
                      class="v-label text-body-2 text-high-emphasis"
                      for="mobile"
                      >Source:</label
                    >
                  </VCol>

                  <VCol cols="12" md="9">
                    <AppTextField
                      id="mobile"
                      type="number"
                      placeholder="int"
                      persistent-placeholder
                    />
                  </VCol>
                </VRow>
              </VCol>

              <VCol cols="12">
                <VRow no-gutters>
                  <!-- Nullable -->
                  <VCol cols="12" md="3" class="d-flex align-items-center">
                    <label
                      class="v-label text-body-2 text-high-emphasis"
                      for="mobile"
                      >Nullable:</label
                    >
                  </VCol>

                  <VCol class="d-flex justify-end" cols="12" md="9">
                    <VSwitch
                      :label="null"
                      color="primary"
                      hide-details
                      :inset="false"
                      :model-value="true"
                    />
                  </VCol>
                </VRow>
              </VCol>
            </VRow>
          </VForm>
        </VCard>

        <div class="mt-8 d-flex justify-space-between align-center">
          <div>
            <h2 class="fs-2 font-weight-medium">Output</h2>
            <p class="mb-0">
              detail: <span style="color: #67b6f0">object</span>
            </p>
          </div>

          <VBtn> Save </VBtn>
        </div>
      </el-drawer>
    </teleport>
  </div>
</template>

<script>
import {
  defineComponent,
  ref,
  getCurrentInstance,
  nextTick,
  onMounted,
} from "vue";
import { ElMessageBox } from "element-plus";
import NodeHeader from "./NodeHeader.vue";

export default defineComponent({
  components: {
    NodeHeader,
  },
  setup() {
    const el = ref(null);
    const textarea = ref("");
    let df = null;
    const nodeId = ref(0);
    const dataNode = ref({});
    const drawer = ref(false);
    const direction = ref("rtl");
    const handleClose = (done) => {
      ElMessageBox.confirm("Are you sure you want to close this?")
        .then(() => {
          done();
        })
        .catch(() => {
          // catch error
        });
    };
    df = getCurrentInstance().appContext.config.globalProperties.$df.value;

    const updateSelect = (value) => {
      dataNode.value.data.script = value;
      df.updateNodeDataFromId(nodeId.value, dataNode.value);
    };

    onMounted(async () => {
      await nextTick();
      nodeId.value = el.value.parentElement.parentElement.id.slice(5);
      dataNode.value = df.getNodeFromId(nodeId.value);
      textarea.value = dataNode.value.data.script;
    });

    return {
      el,
      drawer,
      direction,
      handleClose,
      textarea,
      updateSelect,
    };
  },
});
</script>
<style scoped>
.fs-2 {
  font-size: 26px;
}
</style>
