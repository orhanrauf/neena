<script setup lang="ts">
import { defineEmits, ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import {TaskDefinition} from '@/types';

const store = useStore();

// Reactive state variables
const searchQuery = ref('');

const taskDefinitions = computed(() => store.getters.taskDefinitions);

// Computed property for filtering tasks based on search query
const filteredTaskDefinitions = computed(() => {
    return taskDefinitions.value.filter((taskDefinition: TaskDefinition) =>
    taskDefinition.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

// Fetch tasks when the component is mounted
onMounted(() => {
    store.dispatch('fetchTaskDefinitions');
});

const emit = defineEmits<{
    (e: 'close-card'): void;
    (e: 'add-task', task: TaskDefinition): void;
}>();

const addTask = (taskDefinition: TaskDefinition) => {

    const cloneTaskDefinition = Object.assign({}, taskDefinition);
    emit("add-task", cloneTaskDefinition);
};

// Methods
function emitCloseCard() {
    emit('close-card');
}

function getIconUrl(integration: string): string {
  return `${import.meta.env.VITE_APP_BASE_URL}images/icons/integrations/${integration}.svg`;
}

</script>

<template>
    <div class="main-container">
        <div class="header-container">
            <h1 class="header">Tasks</h1>
            <VIcon class="task-search-close-btn" icon="tabler-x" size="22" @click="emitCloseCard" />
        </div>
        <div class="search-container">
            <input type="text" class="search-input" v-model="searchQuery" placeholder="Search tasks">
        </div>
        <ul class="task-list">
            <li v-for="task in filteredTaskDefinitions" :key="task.id" class="task-item">
                <!-- Assuming you have icons as components or elements -->
                <img :src="getIconUrl(task.source)" alt="" class="icon">
                <span class="task-name" @click="addTask(task)">{{ task.name }}</span>
            </li>
        </ul>
    </div>
</template>


  
<style scoped>
.main-container {
    background: #fff;
    border-radius: 6px;
    border: 1px solid #b3b3b3;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 0.75rem;
    padding-top: 0.6rem;
    width: 300px;
    /* Adjust the width as necessary */
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.header {
    margin-top: -10px;
    font-size: 1.3rem;
    font-weight: 500;
    color: #606060;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

.search-container {
    margin-bottom: 20px;
    padding-right: 1rem;
}

.search-input {
    width: 90%;
    padding: 6px;
    border: 1.2px solid #acacac;
    border-radius: 4px;
    font-size: 0.95rem;
}

.task-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    max-height: 500px;
    /* Set a maximum height */
    overflow-y: scroll;
    /* Enable vertical scrolling */
}

.task-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.task-item:hover {
    cursor: pointer;
}

.icon {
    width: 20px;
    /* Adjust as necessary */
    height: 20px;
    /* Adjust as necessary */
    margin-right: 10px;
}

.task-name {
    font-weight: 500;
    color: #7c7c7c;
}


.task-name:hover {
    color: #636363 !important;
}
</style>
  