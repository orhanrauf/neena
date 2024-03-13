<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();

const route = useRoute('flow-id');
const id = route.params.id;

const isFetching = ref(true);
const items = ref([{ title: 'Request', to: 'flow' }, { title: 'View' }]);

const response = ref<any>(null);

onMounted(async () => {
    try {
        let res = await store.dispatch('fetchFlowRequestDetail', id);
        response.value = res;
        console.log('response: ', response.value);
        isFetching.value = false;
    } catch (error) {
        console.error('Error fetching FlowRequest Detail:', error);
    }
});
</script>

<template>
    <!-- loader -->
    <div v-if="isFetching" class="text-center my-16 py-16">
        <v-progress-circular
            :size="50"
            color="primary"
            indeterminate
        ></v-progress-circular>
    </div>

    <!-- details -->
    <div v-else>
        <v-breadcrumbs class="text-h3 p-0" :items="items">
            <template v-slot:title="{ item }">
                <span v-if="item.title === 'Request'" class="text-h4">
                    <router-link to="/requests" style="color: #a5a2ad">
                        {{ item.title }}
                    </router-link>
                </span>
                <span v-else class="text-h4">{{ item.title }}</span>
            </template>
        </v-breadcrumbs>
        <section class="mt-4">
            <VRow>
                <VCol cols="12" md="4">
                    <VCard>
                        <VCardText>
                            <div>
                                <h4 class="mb-3 card-subheading">DETAILS</h4>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-user"
                                            color="#4B465C"
                                            size="18"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Created by:
                                    </span>
                                    <span class="card-value-text">
                                        John Doe
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-check"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-2 card-property-text">
                                        Has Flow:
                                    </span>
                                    <span
                                        class="has-flow"
                                        :class="
                                            response?.flow
                                                ? 'has-flow-yes'
                                                : 'has-flow-no'
                                        "
                                    >
                                        {{ response?.flow ? 'Yes' : 'No' }}
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-message-circle"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Source:
                                    </span>
                                    <span class="card-value-text">
                                        User Interface
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-clock-hour-4"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Country:
                                    </span>
                                    <span class="card-value-text">USA</span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-language"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Languages:
                                    </span>
                                    <span class="card-value-text">English</span>
                                </div>
                            </div>
                            <div class="mt-4">
                                <h4 class="mb-3 card-subheading">
                                    PLACEHOLDER DETAILS
                                </h4>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-phone-call"
                                            color="#4B465C"
                                            size="18"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Contact:
                                    </span>
                                    <span class="card-value-text">
                                        (123) 456-7890
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-brand-skype"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Skype:
                                    </span>
                                    <span class="card-value-text">
                                        john.doe
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-mail"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Email:
                                    </span>
                                    <span class="card-value-text">
                                        {{ response?.created_by_email }}
                                    </span>
                                </div>
                            </div>
                            <div class="mt-4">
                                <h4 class="mb-3 card-subheading">
                                    PLACEHOLDERS
                                </h4>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-brand-angular"
                                            color="#EA5455"
                                            size="18"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Backend Developer:
                                    </span>
                                    <span class="card-value-text">
                                        (126 Members)
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-brand-react"
                                            size="18"
                                            color="#00CFE8"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        React Developer:
                                    </span>
                                    <span class="card-value-text">
                                        (98 Members)
                                    </span>
                                </div>
                            </div>
                        </VCardText>
                    </VCard>
                    <VCard class="mt-5">
                        <VCardText>
                            <div>
                                <h4 class="mb-3 card-subheading">FLOW</h4>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-replace"
                                            color="#4B465C"
                                            size="18"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Flow Id:
                                    </span>
                                    <span class="card-value-text flow-id">
                                        {{ response?.id }}
                                    </span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-layout-grid"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Placeholder Compiled:
                                    </span>
                                    <span class="card-value-text">145</span>
                                </div>
                                <div class="d-flex align-center my-1">
                                    <span class="mr-2">
                                        <VIcon
                                            icon="tabler-users"
                                            size="18"
                                            color="#4B465C"
                                        />
                                    </span>
                                    <span class="mr-1 card-property-text">
                                        Placeholders:
                                    </span>
                                    <span class="card-value-text">879</span>
                                </div>
                            </div>
                        </VCardText>
                    </VCard>
                </VCol>
                <VCol cols="12" md="8">
                    <VCard>
                        <VCardTitle class="card-title-bg card-title">
                            <h2 class="pa-2">Request Body</h2>
                        </VCardTitle>
                        <VCardText class="py-5 card-body-height">
                            <p>
                                {{ response.request_instructions }}
                            </p>
                        </VCardText>
                    </VCard>
                    <VCard class="mt-5">
                        <VCardTitle class="card-title-bg card-title">
                            <h2 class="pa-2">Metadata</h2>
                        </VCardTitle>
                        <VCardText class="py-5 card-body-height">
                            <VRow>
                                <VCol cols="12" md="5">
                                    <h4 class="form-subheading mb-1">
                                        Parameter name
                                    </h4>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="email"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="ticketCreationDateTime"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="urgency"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="source"
                                        />
                                    </div>
                                </VCol>
                                <VCol cols="12" md="7">
                                    <h4 class="form-subheading mb-1">
                                        Parameter value
                                    </h4>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="john@example.com"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="23 Aug 2021, 2:00 PM"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="2 - Serious"
                                        />
                                    </div>
                                    <div class="mb-2">
                                        <input
                                            class="form-input"
                                            type="text"
                                            placeholder="WooCommerce"
                                        />
                                    </div>
                                </VCol>
                            </VRow>
                        </VCardText>
                    </VCard>
                </VCol>
            </VRow>
        </section>
    </div>
</template>

<style scoped>
.v-breadcrumbs {
    padding: 0 !important;
}

.flow-id {
    color: rgba(255, 159, 67, 0.85);
}

.badge {
    background-color: rgba(255, 159, 67, 0.2);
    border: 1px solid rgba(75, 70, 92, 0.5);
    border-radius: 4px;
    display: flex;
    width: 36px;
    height: 22px;
    padding: 5px 7px;
    align-items: center;
    color: rgba(255, 159, 67, 1);
}

.red-border {
    border: 2px solid red;
}
.green-border {
    border: 2px solid green;
}

.card-title-bg {
    background-color: rgba(40, 199, 111, 0.2);
}

.form-input {
    width: 100%;
    border: 1px solid rgba(75, 70, 92, 0.6);
    padding: 9px 10px;
    border-radius: 4px;
    color: rgba(75, 70, 92, 0.8);
    font-family: Helvetica;
    font-size: 13px;
    font-weight: 500;
    line-height: 14px;
}
.form-input::placeholder {
    color: rgba(75, 70, 92, 0.6);
}
.form-input:focus,
.form-input:active {
    outline: none !important;
    border: 1px solid rgba(75, 70, 92);
    box-shadow: 0 0 2px rgba(75, 70, 92, 0.8);
}

.card-title {
    /* //styleName: Light/Basic Typography/H5 Heading; */
    font-family: Helvetica;
    font-size: 18px;
    font-weight: 500;
    line-height: 24px;
    letter-spacing: 0px;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.1),
            rgba(255, 255, 255, 0.1)
        );
}

.card-body-height {
    min-height: 342px;
}

.card-subtext {
    /* //styleName: Light/Basic Typography/Paragraph; */
    font-family: Helvetica;
    font-size: 15px;
    font-weight: 400;
    line-height: 22px;
    letter-spacing: 0px;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.2),
            rgba(255, 255, 255, 0.2)
        );
}

.form-subheading {
    font-family: Helvetica;
    font-size: 13px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.2),
            rgba(255, 255, 255, 0.2)
        );
}

.card-subheading {
    /* //styleName: Light/Basic Typography/Paragraph Small; */
    font-family: Helvetica;
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
    letter-spacing: 0px;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.5),
            rgba(255, 255, 255, 0.5)
        );
}

.card-value-text {
    /* //styleName: Light/Basic Typography/Paragraph; */
    font-family: Helvetica;
    font-size: 15px;
    font-weight: 400;
    line-height: 22px;
    letter-spacing: 0px;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.2),
            rgba(255, 255, 255, 0.2)
        );
}

.card-property-text {
    /* //styleName: Light/Basic Typography/Paragraph Semi Bold; */
    font-family: sans-serif;
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
    letter-spacing: 0px;
    color: linear-gradient(0deg, #4b465c, #4b465c),
        linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.2),
            rgba(255, 255, 255, 0.2)
        );
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
