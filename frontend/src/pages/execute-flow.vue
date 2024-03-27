<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
let intervalId;

const refreshFlowRunState = async () => {
  try {
    if(!store.state.flowExecution.flowRun.id) return;
    await store.dispatch('getFlowRun', store.state.flowExecution.flowRun.id);
  } catch (error) {
    console.error(error);
  }
};

const refreshFlowRunStateButton = async () => {
  const response = await http.get(`/flow_runs/all?limit=1`);
  store.commit('setFlowRun', response.data[0]);
};

onMounted(() => {
  intervalId = setInterval(refreshFlowRunState, 2000);
});

const clearPollingInterval = () => {
  clearInterval(intervalId);
};

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<template>
  <VRow>
    <VCol cols="12" md="8">
      <ExecuteFlowCard />
    </VCol>
    <VCol cols="12" md="3" offset-md="1">
      <FlowExecutionMetadataCard />
    </VCol>
  </VRow>
  <VRow>
    <VBtn @click="refreshFlowRunStateButton">
      Refresh
    </VBtn>

    <VBtn @click="clearPollingInterval">
      Stop polling
    </VBtn>
  </VRow>

</template>