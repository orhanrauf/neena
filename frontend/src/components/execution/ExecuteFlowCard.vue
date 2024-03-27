<script setup>
  import { onMounted, onUnmounted, ref } from 'vue';
  import { useStore } from 'vuex';

  const store = useStore();

  const initializeExecution = async () => {
      await refreshFlowRunStateTempDebugFunction();
      const response = await http.get(`flows?id=${store.state.flowExecution.flowRun.flow}`);
      const flowBeingExecuted = response.data;
      store.commit('setFlowForFlowExecution', flowBeingExecuted);
      await store.dispatch('fetchTaskDefinitions');
      await store.dispatch('fetchIntegrations');
      initializeFlowExecutionDisplayModel();
    }
    
  const refreshFlowRunStateTempDebugFunction = async () => {
    const response = await http.get(`/flow_runs/all?limit=1`);
    store.commit('setFlowRun', response.data[0]);
  };

  const panelStatus = ref(0);
  const flowExecutionDisplayModel = ref(null);

  const initializeFlowExecutionDisplayModel = () => {
    const flowRun = store.state.flowExecution.flowRun;
    const flow = store.state.flowExecution.flow;

    var taskOperations = flow.task_operations;

    taskOperations.forEach((taskOperation) => {
      const taskDefinition = store.getters.getTaskDefinitionById(taskOperation.task_definition);
      taskOperation.integration = store.getters.getIntegrationById(taskDefinition.integration);
      taskOperation.taskRun = {
        status: 'pending'
      };
      taskOperation.taskDefinition = taskDefinition;
    });

    taskOperations.sort((a, b) => b.index - a.index);

    flowExecutionDisplayModel.value = taskOperations
  };

  const updateFlowExecutionDisplayModel = () => {

    if(!store.state.flowExecution.flowRun.id) return;
    if(!flowExecutionDisplayModel.value) return;

    const flowRun = store.state.flowExecution.flowRun;
    const flow = store.state.flowExecution.flow;

    flowExecutionDisplayModel.value.forEach((taskOperation) => {
      const taskRun = flowRun.task_runs.find((taskRun) => taskRun.task_operation_index === taskOperation.index);

      if (taskRun) {
        taskOperation.taskRun = taskRun;
      }
    });
  };

  onMounted(() => {
    initializeExecution();
  });
  
  watch(
    () => store.state.flowExecution.flowRun.id,
    async (newId, oldId) => {
      if (newId && newId !== oldId) {
        await initializeExecution();
      }
    },
    { immediate: true }
  );

  watch(
      () => store.state.flowExecution.latestUpdate,
      async () => {
        await updateFlowExecutionDisplayModel();
      },
    { immediate: true }
  );

const getIconUrl = (integrationShortName) => {
  return `${import.meta.env.VITE_APP_BASE_URL}images/icons/integrations/${integrationShortName}.svg`;
}

</script>

<template>
    <VCard class="outer-card">
      <VCardTitle class="card-title-bg card-title">
        <h2 class="pa-3">{{ store.state.flowExecution.flow.name }}</h2>
      </VCardTitle>

      <VCardSubtitle class="pa-3">
        <VRow>
          <VCol cols="auto">
          </VCol>
        </VRow>
      </VCardSubtitle>

    <div class="course-content">
      <VExpansionPanels
        v-model="panelStatus"
        variant="accordion"
        class="expansion-panel"
        
      >
        <template v-for="(taskOp, index) in flowExecutionDisplayModel" :key="taskOp.sorted_index" class="my-3">
          <VExpansionPanel elevation="2" :value="index">
            <template #title>
              <VRow class="align-center" no-gutters justify-space-between>
                <VCol cols="auto" class="d-flex align-center">
                  <img :src="getIconUrl(taskOp.integration.short_name)" class="img" />
                  <div class="px-3 text-h5">{{ taskOp.name }}</div>
                </VCol>
                <VCol cols="auto">
                  <div class="text-caption font-weight-medium text-right">
                    {{ taskOp.taskRun.status }}
                  </div>
                </VCol>
              </VRow>
            </template>
            <template #text>
              <VCol>
                
                <div class="divider"></div>
                <div class="instruction-box-header">Instructions</div>
                <textarea class="instructions-box-input"
                  placeholder="We need to get the user profile before we can process this person’s request. Use the customer’s email from the metadata to look up their account." v-model="taskOp.instructions">
                </textarea>

                <div class="parameters-box-header">Parameters</div>
                <textarea class="parameters-box-input"
                  placeholder="We need to get the user profile before we can process this person’s request. Use the customer’s email from the metadata to look up their account." v-model="taskOp.instructions">
                </textarea>

                <div class="result-box-header">Task output</div>
                <div class="result-box-input">
                <JSONViewCard :jsonData="taskOp.taskRun.result" :objectName="taskOp.taskDefinition.output_type"/>
                </div>

              </VCol>
            </template>
          </VExpansionPanel>
        </template>
      </VExpansionPanels>
    </div>

    </VCard>
  </template>

<style scoped>


.result-box-header {
  color: var(--light-solid-color-light-gray-800-hover, #777471);
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  margin-top: 16px;
  white-space: nowrap;
  font: 400 16px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.result-box-input {
  border-radius: 4px;
  border: 1.4px solid var(--light-solid-color-light-gray-800-hover, #787779);
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  display: flex;
  margin-top: 4px;
  flex-direction: column;
  padding: 10px;
  resize: both;
  color: #454443;
  /* Allows resizing on both width and height */
  overflow: auto;
  /* Necessary for 'resize' to work */
  height: 400;
  /* Minimum height */
  max-height: 600px;
  /* Optional: Constrain the max size */
  min-width: 100%;
  max-width: 100%;

}

.instruction-box-header {
  color: var(--light-solid-color-light-gray-800-hover, #777471);
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  white-space: nowrap;
  font: 400 16px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.instructions-box-input {
  border-radius: 4px;
  border: 1.4px solid var(--light-solid-color-light-gray-800-hover, #787779);
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  display: flex;
  margin-top: 4px;
  flex-direction: column;
  padding: 10px;
  resize: both;
  color: #454443;
  /* Allows resizing on both width and height */
  overflow: auto;
  /* Necessary for 'resize' to work */
  height: 400;
  /* Minimum height */
  max-height: 1000px;
  /* Optional: Constrain the max size */
  min-width: 100%;
  max-width: 100%;

}

.parameters-box-header {
  color: var(--light-solid-color-light-gray-800-hover, #777471);
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  margin-top: 16px;
  white-space: nowrap;
  font: 400 16px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.parameters-box-input {
  border-radius: 4px;
  border: 1.4px solid var(--light-solid-color-light-gray-800-hover, #787779);
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  display: flex;
  margin-top: 4px;
  flex-direction: column;
  padding: 10px;
  resize: both;
  color: #454443;
  /* Allows resizing on both width and height */
  overflow: auto;
  /* Necessary for 'resize' to work */
  height: 400;
  /* Minimum height */
  max-height: 1000px;
  /* Optional: Constrain the max size */
  min-width: 100%;
  max-width: 100%;

}

.divider {
  background-color: #dbdade;
  margin-left: -2%;
  margin-right: -2%;
  margin-bottom: 12px;
  /* margin-top: 4px; */
  height: 1px;
}

.taskOp-attributes-list .v-list-item {
  padding: 0.5rem 1rem; /* Adjust padding to your preference */
}

.taskOp-attributes-list .v-icon {
  color: #5C6BC0; /* Adjust icon color to your preference */
}

.card-title {
    /* //styleName: Light/Basic Typography/H5 Heading; */
    font-family: Helvetica;
    font-size: 12px;
    font-weight: 100;
    line-height: 24px;
    letter-spacing: 0px;
    color: #000000;
}

.card-title-bg {
    background-color: rgba(255, 217, 140, 0.6);
}

.outer-card {
    /* //styleName: Light/Basic/Basic Card; */
    background-color: #FFFFFF;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    margin: 0px;
}

.expansion-panel {
    /* //styleName: Light/Basic/Basic Card; */
    background-color: #FFFFFF;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    padding: 12px;
    margin: 0px;

}

.img {
  max-width: 30px; /* Adjust size as needed */
  height: auto; /* Maintain aspect ratio */
}

.px-3 {
  padding-left: 1rem; /* Adjust padding as needed */
  padding-right: 1rem;
}

.text-caption {
  font-size: 0.75rem; /* Smaller text for status */
}

/* Ensure text doesn't overflow on small screens */
.text-h5 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.font-weight-medium {
  font-weight: 500; /* Medium font weight for status */
}

.align-center {
  align-items: center; /* Center items vertically */
}
</style>