<script setup lang="ts">

import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const route = useRoute();
const store = useStore();

onMounted(() => {
    const id = route.params.id;
    const flow = store.dispatch('fetchFlowById', id);
    store.commit('buildDrawFlowFromApi', flow);
});

</script>

<template>
    <div class="drawflow-container">
        <DrawFlow />
  </div>
</template>
