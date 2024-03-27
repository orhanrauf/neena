<script setup lang="ts">
import { VDataTable } from 'vuetify/labs/VDataTable';
import { useStore } from 'vuex';
import dayjs from 'dayjs';
import { toRaw } from 'vue';

const store = useStore();
const router = useRouter();

const options = ref({
    page: 1,
    itemsPerPage: 10,
    sortBy: 'created_date',
    sortDesc: [false],
});

const isloading = ref(true);
const search = ref('');

// Items per page options
const itemsPerPage = [5, 10, 25, 50, 100];

function navigateToFlow(event, item) {
    router.push(`/flows/${item.item.id}`);
}

// Headers
const headers: any = [
    { title: 'Flow', key: 'name', width: '50%' },
    { title: 'BY HUMAN', key: 'created_by_human', align: 'start', width: '15%' },
    {
        title: 'CREATED DATE',
        key: 'created_date',
        align: 'start',
        width: '25%',
    },
    {
        title: 'ACTIONS',
        key: 'actions',
        sortable: false,
        align: 'start',
        width: '15%',
    },
];

let allFlows = store.state.flows;
let flows = ref([]);

function filterFlows(): any {
    const searchTerm = search.value.toLowerCase();
    flows.value = searchTerm
        ? allFlows.filter((flow: any) =>
              flow.name.toLowerCase().includes(searchTerm)
          )
        : [...allFlows];
}

function formatDate(dateString: string) {
    return dayjs(dateString).format('D MMM YYYY, h:mm A');
}

async function deleteFlow(id: string) {
    let res = await store.dispatch('deleteFlow', id);
    if (res === 200) {
        flows.value = flows.value.filter(
            (req: any) => req.id !== id
        );
    }
}

const fetchAndSetFlows = async () => {
  try {
    isloading.value = true;
    await store.dispatch('fetchFlows');
    flows.value = store.state.flows;
    allFlows = store.state.flows;
    isloading.value = false;
  } catch (error) {
    console.error('Error fetching Flows:', error);
    isloading.value = false;
  }
};

onMounted(fetchAndSetFlows);

// Watch for route changes
const route = useRoute();
watch(() => route.path, async (newPath, oldPath) => {
  // You can put more logic here to decide when to fetch new data
  if (newPath !== oldPath) {
    await fetchAndSetFlows();
  }
}, { immediate: false });
</script>

<template>
    <h1 class="page-title">Flows</h1>
    <VCard class="requests">
        <!-- Filters -->
        <VCardText>
            <VRow>
                <VCol cols="12" md="3">
                    <AppTextField
                        v-model="search"
                        density="compact"
                        placeholder="Search"
                        append-inner-icon="tabler-search"
                        single-line
                        hide-details
                        dense
                        outlined
                        @input="filterFlows()"
                    />
                </VCol>

                <VCol cols="12" offset-md="7" md="2">
                    <VSelect
                        :items="itemsPerPage"
                        v-model="options.itemsPerPage"
                    />
                </VCol>
            </VRow>
        </VCardText>

        <!-- Data Table  -->
        <VDataTable
            :headers="headers"
            :items="flows"
            :search="search"
            :sort-by="[{key: 'created_date', order: 'desc' }]"
            :loading="isloading"
            :loading-text="'Loading...'"
            :items-per-page="options.itemsPerPage"
            :page="options.page"
            @update:options="options = $event"
            :item-class="'row-hover'"
            @click:row="navigateToFlow"
        >
            <!-- details -->
            <template #item.name="{ item }">
                <span
                    v-html="item.name"
                    class="color-primary"
                ></span>
            </template>

            <template #item.flow="{ item }">
                <span
                    class="has-flow"
                    :class="item.created_by_human ? 'has-flow-yes' : 'has-flow-no'"
                >
                    {{ item.flow ? 'Yes' : 'No' }}
                </span>
            </template>

            <template #item.created_date="{ item }">
                {{ formatDate(item.created_date) }}
            </template>

            <!-- Actions -->
            <template #item.actions="{ item }">
                <button class="mx-1" @click="deleteFlow(item.id)">
                    <VIcon
                        icon="tabler-trash"
                        class="color-primary"
                        size="26"
                    />
                </button>
                <button
                    class="mx-1"
                    @click="() => $router.push(`flows/${item.id}`)"
                >
                    <VIcon icon="tabler-eye" class="color-primary" size="26" />
                </button>
            </template>

            <!-- Datatable footer -->
            <template #bottom>
                <VCardText class="pt-4">
                    <VRow>
                        <VCol lg="3">
                            <p
                                style="
                                    font-size: 14px;
                                    margin-top: 10px;
                                    margin-bottom: 0;
                                "
                            >
                                Showing
                                {{
                                    options.page * options.itemsPerPage -
                                    options.itemsPerPage +
                                    1
                                }}
                                to {{ options.page * options.itemsPerPage }} of
                                {{ flows.length }} entries
                            </p>
                        </VCol>

                        <VCol lg="9" class="d-flex justify-end">
                            <VPagination
                                v-model="options.page"
                                total-visible="5"
                                :length="
                                    Math.ceil(
                                        flows.length /
                                            options.itemsPerPage
                                    )
                                "
                            />
                        </VCol>
                    </VRow>
                </VCardText>
            </template>
        </VDataTable>
    </VCard>
</template>

<style scoped>

:deep(.v-data-table__tr--clickable:hover) {
    background-color: rgba(0, 0, 0, 0.05);
}

.v-data-table__tr--clickable:hover {
    background-color: rgba(0, 0, 0, 0.3) !important;
}   

.v-data-table .v-data-table__wrapper table tbody tr.row-hover:hover {
    background-color: rgba(0, 0, 0, 0.3) !important;
}   

.page-title {
    font-weight: 500;
    font-size: 48px;
    line-height: 68px;
    color: #5d586c;
}

.color-primary {
    color: #5d586c;
}

.has-flow {
    padding: 5px 10px 5px 10px;
    border-radius: 4px;
    border: 1px solid #4b465c8c;
}

.has-flow-yes {
    background-color: #67b6f029;
    color: #67b6f0;
}

.has-flow-no {
    background-color: #ff9f4329;
    color: #ff9f43;
}
</style>
