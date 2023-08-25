<script setup lang="ts">
import axios from "@axios"
import { Ref } from "vue"

const route = useRoute();
const flowRequestId = route.params.flow_request_id as string;

const status: Ref<number | null> = ref(null);
const doesExists = computed(() => status.value === 200);

onMounted(async () => {
  axios.get(`/v1/flow_requests/?id=${flowRequestId}`)
    .then((response) => {
      status.value = response.status;
    })
    .catch(() => {});
});
</script>

<template>
  <div>
    <div v-if="doesExists">
      <DrawFlow :flow-request-id="flowRequestId" />
    </div>
    <div v-else>
      Flow request not found!
    </div>
  </div>
</template>
