<template>
    <div class="main-container">
        <header class="header">
            <span class="header-title">Request</span>
            <div class="close-button">
                <v-icon size=24px color="#7a7a7a" @click="$emit('close')">tabler-x</v-icon>
            </div>
        </header>
        <div class="content-container">
            <div class="description">{{ requestContent }}</div>
            <div class="divider"></div>
            <footer class="footer">Details</footer>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

// Assuming the state variable is stored under the key 'request' in Vuex
const requestContent = computed(() => store.state.flowCreation.request.content);
</script>

<style scoped>
.main-container {
    border: 3px solid #6a6675;
    background-color: #fff;
    max-width: 862px;
    width: 700px;
    height: 400px;
    display: flex;
    flex-direction: column;
    border-radius: 6px; /* border-radius is applied here */
    overflow: hidden; /* This will clip the children to the main-container's border */
}

.header {
    background-color: #d4ede0;
    color: #5f5d5d;
    padding: 10px;
    font-size: 24px;
    font-weight: 500;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0; /* Removes any default margin */
}

.close-button {
    cursor: pointer;
}

.content-container {
    padding: 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column; /* Ensures footer is at the bottom */
}

.description {
    font-size: 17px;
    flex-grow: 1; /* Allows description to fill the space above the divider */
    font-weight: 500;
    color: #828282;
}

.divider {
    border-bottom: 1px solid #c1c1c1;
    margin-top: 16px; /* Adds margin on top of the divider */
    margin-bottom: 16px; /* Adds margin below the divider */
    margin-left: -16px;
    width: 110%;
}

.footer {
    font-size: 12px;
    color: #67a3ce;
}
</style>
