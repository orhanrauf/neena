<script setup>
import { getCurrentInstance, nextTick, onMounted, ref } from "vue";
import { computed } from 'vue';
import TaskOperationDrawer from "./TaskOperationDrawer.vue";
import { useStore } from 'vuex';

const store = useStore();
const el = ref(null);
const nodeId = ref(0);
const taskOp = ref({});
const showDrawer = ref(false);
const taskDefinition = ref(null);
const isDataLoaded = ref(false); // to track data loading status
const computedTaskDefinition = computed(() => taskDefinition.value);
const computedTaskOp = computed(() => taskOp.value);

let df = null;

df = getCurrentInstance().appContext.config.globalProperties.$df.value;

const dynamicHeaderClass = (source) => {
  // This function determines the class based on the task name
  // Adjust the logic according to your needs, for example:
  if (source.toLowerCase().includes('chat-gpt')) {
    return 'chat-gpt';
  } else if (source.toLowerCase().includes('gmail') || source.toLowerCase().includes('google-drive')) {
    return 'g-suite';
  } else if (source.toLowerCase().includes('salesforce')) {
    return 'salesforce';
  }
  return ''; // Default case, no additional class
};

onMounted(async () => {
  await nextTick();
  nodeId.value = el.value.parentElement.parentElement.id.slice(5);
  taskOp.value = store.getters.getTaskOperationByNodeId(parseInt(nodeId.value));
  taskDefinition.value = store.getters.getTaskDefinitionById(taskOp.value.task_definition);
  isDataLoaded.value = true;
});


const getIconUrl = (integration) => {
  return `${import.meta.env.VITE_APP_BASE_URL}images/icons/integrations/${integration}.svg`;
};

</script>

<template>
  <div ref="el" @dblclick="showDrawer = true">
    <template v-if="isDataLoaded">
      <div class="main-container">
        <div :class="['header', dynamicHeaderClass(computedTaskDefinition.source)]">
          <img :src="getIconUrl(computedTaskDefinition.source)" class="img" />
          <div class="header-text">{{ taskOp.name }}</div>
        </div>
        <div class="description">{{ computedTaskDefinition.description }}</div>
        <div class="output-container">
          <div class="output-object">{{ computedTaskDefinition.output_type }}</div>
          <div class="output-text">OUTPUT</div>
        </div>
      </div>
      <TaskOperationDrawer v-model="showDrawer" :df="df" :node-id="nodeId" />
    </template>
  </div>
</template>



<style scoped>
.main-container {
  border-radius: 2px;
  display: flex;
  /* max-width: 346px; */
  flex-direction: column;
}

.main-container .header.g-suite {
  background-color: #fff1e2;
}

.main-container .header.chat-gpt {
  background-color: #d4ede0;
}

.header {
  border-radius: 4px 4px 0px 0px;
  display: flex;
  justify-content: space-between;
  gap: 15px;
  padding: 14px 10px;
  width: 100%;
  background-color: #e0f2ff;
}

.img {
  aspect-ratio: 1;
  object-fit: contain;
  object-position: center;
  width: 32px;
  overflow: hidden;
  max-width: 100%;
}

.header-text {
  color: #6f6b7d;
  font-feature-settings: "clig" off, "liga" off;
  align-self: center;
  flex-grow: 1;
  width: 100%;
  white-space: nowrap; /* Prevents the text from wrapping to the next line */
  overflow: hidden; /* Hides the text that overflows the container */
  text-overflow: ellipsis; /* Adds an ellipsis to the end of the text that overflows */
  margin: auto 0;
  font: 500 18px/133% Helvetica Neue, -apple-system, Roboto, Helvetica, sans-serif;
}

.description {
  color: var(--Light-Typography-Color-Body-Text, #666666);
  font-feature-settings: "clig" off, "liga" off;
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  width: 100%;
  justify-content: center;
  padding: 12px 10px;
  font: 400 15px/24px Helvetica Neue, -apple-system, Roboto, Helvetica, sans-serif;
  min-height: 60px;
  /* Assuming the line-height is 24px, 2 lines would be 48px */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  /* Limits the text to 2 lines and adds an ellipsis if it overflows */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.output-container {
  display: flex;
  width: 100%;
  gap: 20px;
  justify-content: space-between;
  padding: 14px 10px;
  background-color: rgb(240, 240, 239);
}

.output-object {
  color: var(--light-solid-color-warning-warning-600-hover, #e9903d);
  font-feature-settings: "clig" off, "liga" off;
  letter-spacing: 0.43px;
  margin-top: 4px;
  margin-bottom: 4px;
  font: 500 17px Helvetica Neue, sans-serif;
}

.output-text {
  color: #b7b5be;
  text-align: right;
  white-space: nowrap;
  margin-top: -6px;
  /* font-feature-settings: "clig" off, "liga" off; */
  letter-spacing: 1px;
  text-transform: uppercase;
  font: 700 13px Helvetica Neue, sans-serif;
}
</style>