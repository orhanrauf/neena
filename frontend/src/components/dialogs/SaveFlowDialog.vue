<template>
    <div class="main-container">
        <header class="header">
            <span class="header-title">Save Flow</span>
            <div class="close-button">
                <v-icon size="24px" color="#7a7a7a" @click="$emit('close')">tabler-x</v-icon>
            </div>
        </header>
        <div class="content-container">
            <input class="description-input" type="text" v-model="flowDescription" />
            <footer class="footer">
                <!-- Run Flow button -->
                <VBtn class="save-btn" prepend-icon="tabler-device-floppy" @click="saveFlow">
                    Save
                </VBtn>
            </footer>
        </div>
    </div>
</template>
  

<script setup>
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const requestContent = computed(() => store.state.flowCreation.request.content);
const flowDescription = ref(`Flow for ${requestContent.value}`);

watch(requestContent, (newValue) => {
    flowDescription.value = `Flow for ${newValue}`;
});

const saveFlow = () => {
    // Implement logic to save the flow
    alert(`Flow saved: ${flowDescription.value}`);
};
</script>

<style scoped>
.main-container {
    border: 2.5px solid #6a6675;
    background-color: #fff;
    max-width: 862px;
    width: 700px;
    height: 230px;
    display: flex;
    flex-direction: column;
    border-radius: 6px;
    /* border-radius is applied here */
    overflow: hidden;
    /* This will clip the children to the main-container's border */
}

.header {
    background-color: #f5dfbe;
    color: #5f5d5d;
    padding: 10px;
    font-size: 24px;
    font-weight: 500;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0;
    /* Removes any default margin */
}

.close-button {
    cursor: pointer;
}

.content-container {
    padding: 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    /* Ensures footer is at the bottom */
}


.divider {
    border-bottom: 1px solid #c1c1c1;
    margin-top: 16px;
    /* Adds margin on top of the divider */
    margin-bottom: 16px;
    /* Adds margin below the divider */
    margin-left: -16px;
    width: 110%;
}


.description-input {
    font-size: 17px;
    color: #828282;
    border: 1.5px solid #a8a8a8; /* Slightly bolder and darker border */
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 16px;
    margin-top: 8px;
    width: 100%;
    font-weight: 500; /* Bolder font weight */
    background-color: #f9f9f9; /* Slightly darker background */
}

.description-input:focus {
    outline: none; /* Removes the default blue outline */
    border-color: #6a6675; /* Custom focus color */
}

.footer {
    display: flex;
    justify-content: flex-end;
}

.save-btn {
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 8px;
    margin-bottom: 8px;
    background-color: #FF9F43 !important;
    color: #494949 !important;
    border: 1px solid #494949 !important; /* Removes the border */
}
</style>