<script setup lang="ts">
import { useStore } from 'vuex';

const store = useStore();

const loading = ref(true);
const isShowingAddPopup = ref(false);
const search = ref('');

let allIntegrations = store.state.integrations;
let integrationsToLoad = ref<any>([]);
let integrationPopup = ref<any>({});

function setSelectedIntegration(id: string) {
    const matchingIntegration = integrationsToLoad.value.find(
        (integration: any) => integration.id === id
    );
    if (matchingIntegration) {
        integrationPopup.value = { ...matchingIntegration };
    }
}

function filterIntegrations(): any {
    const searchTerm = search.value.toLowerCase();
    integrationsToLoad.value = searchTerm
        ? allIntegrations.filter((integration: any) =>
              integration.name.toLowerCase().includes(searchTerm)
          )
        : [...allIntegrations];
}

onMounted(async () => {
    try {
        await store.dispatch('fetchIntegrations');
        allIntegrations = store.state.integrations;
        integrationsToLoad.value = store.state.integrations;
        loading.value = false;
    } catch (error) {
        console.error('Error fetching integrations:', error);
    }
});
</script>

<template>
    <h1 class="my-2">Integrations</h1>
    <!-- loader -->
    <div v-if="loading" class="text-center my-16 py-16">
        <v-progress-circular
            :size="50"
            color="primary"
            indeterminate
        ></v-progress-circular>
    </div>

    <!-- data -->
    <VCard v-else>
        <!-- Filters -->
        <VCardText>
            <VRow>
                <VCol cols="12" md="4">
                    <AppTextField
                        v-model="search"
                        density="compact"
                        placeholder="Search"
                        append-inner-icon="tabler-search"
                        single-line
                        hide-details
                        dense
                        outlined
                        @input="filterIntegrations()"
                    />
                </VCol>

                <VCol
                    cols="12"
                    offset-md="4"
                    md="4"
                    class="d-flex justify-md-end"
                >
                    <Component class="nav-item-title">
                        <VBtn
                            class="request-integration-btn"
                            prepend-icon="tabler-plus"
                        >
                            Request Integration
                        </VBtn>
                    </Component>
                </VCol>
            </VRow>

            <!-- Integration Cards  -->
            <v-row>
                <v-col
                    cols="12"
                    md="6"
                    lg="4"
                    xl="3"
                    v-for="(item, idx) in integrationsToLoad"
                    :key="idx"
                >
                    <v-card
                        class="mx-auto"
                        :title="item?.name"
                        :subtitle="`${item?.name}.com`"
                    >
                        <!-- avatar -->
                        <template v-slot:prepend>
                            <v-avatar color="blue-darken-2" rounded="0">
                                <v-img
                                    alt="icon"
                                    :src="`/public/images/icons/integrations/${item?.name.toLowerCase()}.svg`"
                                ></v-img>
                            </v-avatar>
                        </template>
                        <!-- content -->
                        <v-card-text>
                            Lorem ipsum dolor sit amet, consectetur adipiscing
                            elit, sed do eiusmod.
                        </v-card-text>
                        <div class="card-bottom pl-5 pb-5">
                            <VBtn
                                color="primary"
                                class="request-integration-btn mt-4"
                                prepend-icon="tabler-circle-plus"
                                @click="
                                    setSelectedIntegration(item?.id),
                                        (isShowingAddPopup = true)
                                "
                            >
                                Connect
                            </VBtn>
                        </div>
                    </v-card>
                </v-col>
            </v-row>
        </VCardText>
    </VCard>
    <!-- add popup -->
    <v-dialog v-model="isShowingAddPopup" width="auto">
        <v-card width="600">
            <v-card-title class="pa-4 popup-header">
                <span class="d-flex justify-space-between">
                    <span class="d-flex align-center">
                        <img
                            :src="`../../public/images/icons/integrations/${integrationPopup.name.toLowerCase()}.svg`"
                            alt="logo"
                            width="30"
                            class="mr-2"
                        />
                        {{ integrationPopup.class_name }}
                    </span>
                    <v-icon
                        class="cursor-pointer"
                        @click="isShowingAddPopup = false"
                    >
                        tabler-letter-x-small
                    </v-icon>
                </span>
            </v-card-title>
            <form>
                <div class="pa-4">
                    <label for="connection-name">Connection name</label>
                    <v-text-field
                        id="connection-name"
                        class="mb-3"
                        placeholder="john@example.com"
                        required
                    />
                    <label for="api-key">API Key</label>
                    <v-text-field
                        id="api-key"
                        class="mb-3"
                        placeholder="john@example.com"
                        required
                    />
                </div>
                <div class="d-flex justify-end pa-4 popup-action">
                    <v-btn color="success" @click="isShowingAddPopup = false">
                        Cancel
                    </v-btn>
                    <v-btn color="warning" class="ml-2">Save</v-btn>
                </div>
            </form>
        </v-card>
    </v-dialog>
</template>

<style>
.request-integration-btn {
    color: #fff !important;
}

.popup-header {
    background-color: #d4f4e2;
}
.popup-action {
    border-top: 1px solid gray;
    padding-top: 10px;
}
.card-bottom {
    background-color: #f6f6f7;
}
</style>
