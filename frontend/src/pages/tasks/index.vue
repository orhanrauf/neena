<script setup lang="ts">
import { VDataTable } from "vuetify/labs/VDataTable";
import axios from "@axios";
import dayjs from "dayjs";

const options = ref({
  page: 1,
  itemsPerPage: 10,
  sortBy: [""],
  sortDesc: [false],
});

const loading = ref(false);
const search = ref("");

// Items per page options
const itemsPerPage = [5, 10, 25, 50, 100];

// Headers
const headers = [
  { title: "NAME", key: "task_name" },
  { title: "PARAMETERS", key: "parameters_formatted" },
  { title: "CREATED DATE", key: "created_date_formatted" },
  { title: "TAGS", key: "tags" },
  { title: "", key: "actions", sortable: false },
];

// Data
let items = ref([]);

const taskDefinitions = computed(() => {
  return items.value.map((item) => ({
    ...item,
    parameters_formatted: item.parameters
      .map((param) => `${param.data_type}: ${param.name}`)
      .join(", "),
    created_date_formatted: dayjs(item.created_date).format("D MMM YYYY"),
  }));
});

const getTasks = () => {
  loading.value = true;

  axios
    .get("/v1/task_definitions/all", {
      params: {
        skip: 0,
        limit: 10,
      },
    })
    .then((response) => {
      items.value = response.data;
    })
    .finally(() => (loading.value = false));
};

onMounted(() => getTasks());
</script>

<template>
  <VCard>
    <!-- Filters -->
    <VCardText>
      <VRow>
        <VCol cols="12" md="4">
          <AppTextField
            v-model="search"
            density="compact"
            placeholder="Search Task"
            append-inner-icon="tabler-search"
            single-line
            hide-details
            dense
            outlined
          />
        </VCol>

        <VCol cols="12" offset-md="4" md="2">
          <VSelect label="Select tags" />
        </VCol>
        <VCol cols="12" md="2">
          <VSelect :items="itemsPerPage" v-model="options.itemsPerPage" />
        </VCol>
      </VRow>
    </VCardText>

    <!-- Data Table  -->
    <VDataTable
      :headers="headers"
      :items="taskDefinitions"
      :search="search"
      :items-per-page="options.itemsPerPage"
      :page="options.page"
      @update:options="options = $event"
    >
      <!-- Name -->
      <template #item.name="{ item }">
        <span class="text-prim" v-html="item.value.name"></span>
      </template>

      <!-- Parameters -->
      <template #item.parameters="{ item }">
        <span v-html="item.value.parameters"></span>
      </template>

      <!-- Actions -->
      <template #item.actions="{ item }">
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-mail" size="26" />
        </button>
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-eye" size="26" />
        </button>
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-dots-vertical" size="26" />
        </button>
      </template>

      <!-- Datatable footer -->
      <template #bottom>
        <VCardText class="pt-4">
          <VRow>
            <VCol lg="2" cols="3">
              <p style="font-size: 14px">
                Showing 1 to 10 of {{ items.length }} entries
              </p>
            </VCol>

            <VCol lg="10" cols="9" class="d-flex justify-end">
              <VPagination
                v-model="options.page"
                total-visible="5"
                :length="Math.ceil(items.length / options.itemsPerPage)"
              />
            </VCol>
          </VRow>
        </VCardText>
      </template>
    </VDataTable>
  </VCard>
</template>

<style>
.text-prim {
  color: #67b6f0 !important;
}

.text-green {
  color: #28c76f !important;
}

.text-blue {
  color: #67b6f0 !important;
}

.text-purple {
  color: #7367f0 !important;
}
</style>
