<template>
  <header class="main-container">
    <textarea class="title input-field" v-model="textareaInput" :placeholder="dynamicPlaceholder"></textarea>
    <div class="horizontal-line"></div>
    <div class="button-group">
      <button class="advanced-btn">Advanced</button>
      <div class="right-buttons">
        <VBtn
            variant="outlined"
            class="start-blank-btn"
            @click="submitRequestBlank"
          >
            Start Blank
          </VBtn>
          <VBtn
            class="generate-flow-btn"
            @click="submitRequestGenerate"
          >
          Generate Flow
          </VBtn>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';


const dynamicPlaceholder = ref("Type here what request you would like to train your agent for");
const textareaInput = ref(""); // Reactive variable for the textarea input
const dotCount = ref(0);
const isIncreasing = ref(true);

const router = useRouter();
const store = useStore();

const startDotAnimation = () => {
  setInterval(() => {
    if (dotCount.value === 3) {
      isIncreasing.value = false;
    } else if (dotCount.value === 0) {
      isIncreasing.value = true;
    }
    
    dotCount.value += isIncreasing.value ? 1 : -1;
    dynamicPlaceholder.value = `Type here what request you would like to train your agent for${'.'.repeat(dotCount.value)}`;
  }, 700);
};

const submitRequest = async () => {
  if (!textareaInput.value.trim()) {
    alert("Please enter a request before proceeding.");
    return;
  }

  var flowRequest = {
    request_instructions: textareaInput.value
  };

  const response = await http.post('flow_requests/', flowRequest);

  flowRequest = response.data;

  store.commit('setRequest', flowRequest);
  return flowRequest;
};

const submitRequestGenerate = async () => {
  const flowRequest = await submitRequest();
  store.dispatch('generateFlow', flowRequest.id);
  router.push('/create-flow');
};

const submitRequestBlank = async () => {
  await submitRequest();
  store.commit('setFlow', {name:'', task_operations: [], dependencies: [],});
  router.push('/create-flow');
};


onMounted(startDotAnimation);
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 862px;
  padding: 21px;
  border-radius: 6px;
  border: 2px solid rgb(var(--v-theme-secondary));
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  box-shadow: 2.5px 2.5px 0px 0px rgb(var(--v-theme-secondary));
  position: relative; 
}
.title {
  color: var(--light-solid-color-gray-gray-600-hover, #4B465C);
  font: 500 22px/30px Roboto, -apple-system, Roboto, Helvetica, sans-serif;
  width: 100%;
  max-width: 800px;
  margin-left: -0.1rem;
  margin-top: -0.6rem;
}

.horizontal-line {
  background-color: #dbdade;
  width: calc(100% + 42px); 
  min-height: 1.5px;
  margin-top: 250px;
  margin-left: -21px; /* Offset the left padding of .main-container */
  margin-right: -21px; 
}

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 20px;
}

.advanced-btn {
  color: var(--Light-Solid-Color-Primary-Primary---800, #67b6f0);
  font: 500 15px/120% Roboto, -apple-system, Roboto, Helvetica, sans-serif;
  letter-spacing: 0.43px;
  align-items: left;
  white-space: nowrap;
}

.button-group {
  display: flex;
  width: 100%; /* Ensure it takes the full width */
  padding: 20px 20px 0; /* Adjust padding as needed */
}

.right-buttons {
  margin-left: auto; /* This should push the buttons to the right */
  display: flex;
  gap: 20px;
}

.input-field {
  width: 100%; /* Full width */
  height: 100%; /* Full height of container */
  border: none; /* No border */
  outline: none; /* Remove focus outline */
  font-size: 18px; /* Example font size */
  color: #4B465C; /* Darker gray text color */
  text-align: left;
  vertical-align: top;
  padding: 0; /* Adjust or remove padding as needed */
}

.input-field::placeholder {
  color: #a0a0a0; /* Lighter gray placeholder text */
}

.start-blank-btn {
  margin-left: auto; /* Pushes this button and the following siblings to the right */
  color: var(--Light-Solid-Color-Secondary-Secondary---900, #9a9b9d) !important;
  border: 1px solid var(--Light-Solid-Color-Secondary-Secondary---900, #9a9b9d);
}
.generate-flow-btn {
  font: 500 15px/120% Roboto, -apple-system, Roboto, Helvetica, sans-serif;
  color: var(--Light-Solid-Color-Extra-Dark, #4b4b4b) !important;
  border: 1px solid var(--Light-Solid-Color-Gray-Gray---900, #4b465c);
  background-color: var(--light-solid-color-warning-warning-500-base, #ff9f43) !important;
  align-self: stretch;
  box-shadow: none !important;
}
</style>