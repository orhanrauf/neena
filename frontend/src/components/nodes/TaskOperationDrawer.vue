<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElDrawer } from 'element-plus';
import { useRoute, useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { useStore } from 'vuex';

import YamlCodeBlock from '../tasks/YamlCodeBlock.vue';

const router = useRouter();
const route = useRoute();
const store = useStore();

const props = defineProps<{
  nodeId: string;
  modelValue: boolean;
}>();

const taskOp = ref(null);
const taskDefinition = ref(null);
const incomingDependencyTuples = ref([]);
const outgoingDependencyTuples = ref([]);

const yamlData = `customer: 12345
name: John Doe
email: johndoe@example.com
phone: 555-1234
address:
  street: 123 Elm Street
  city: Anytown
  state: Anystate
  zipCode: 12345
isActive: true
preferences:
  contactMethod: email
  newsletterSubscription: true
interests:
  - technology
  - sports
  - travel
`;

const emit = defineEmits(['update:modelValue', 'update']);

const show = computed({
  get() {
    // Your existing logic to get sidebar data
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});

const loadDependencies = () => {
    // For incoming dependencies
    const incomingDependencies = store.getters.getDependenciesByTargetNodeId(taskOp.value.drawflow_node_id);
    incomingDependencyTuples.value = incomingDependencies.map(dep => {
      const sourceTaskOp = store.getters.getTaskOperationByNodeId(dep.source_node_id);
      return { dependency: dep, taskOperation: sourceTaskOp };
    });

    // For outgoing dependencies
    const outgoingDependencies = store.getters.getDependenciesBySourceNodeId(taskOp.value.drawflow_node_id);
    outgoingDependencyTuples.value = outgoingDependencies.map(dep => {
      const targetTaskOp = store.getters.getTaskOperationByNodeId(dep.target_node_id);
      return { dependency: dep, taskOperation: targetTaskOp };
    });
  }

  const disableScroll = () => {
    const scrollY = window.scrollY; // Remember the scroll position
    document.documentElement.style.position = 'fixed'; // Keep the document in place
    document.documentElement.style.top = `-${scrollY}px`; // Adjust the top position based on scroll position
    document.documentElement.style.width = '100%'; // Ensure the width doesn't change
  };

  const enableScroll = () => {
    const scrollY = document.documentElement.style.top;
    document.documentElement.style.position = '';
    document.documentElement.style.top = '';
    document.documentElement.style.width = '';
    window.scrollTo(0, parseInt(scrollY || '0') * -1); // Scroll to the original position
  };

  const onDependencyClick = (dependency) => {
    // Handle dependency click event
    console.log('Dependency clicked:', dependency);
  };

  const onTaskOperationClick = (taskOperation) => {
    // Handle task operation click event
    console.log('Task Operation clicked:', taskOperation);
  };

  const getIconUrl = (source: string) => {
    return `/images/icons/integrations/${source}.svg`;
  }

  watch(show, (newValue) => {
    if (newValue) {
      disableScroll();
      loadDependencies();
    } else {
      enableScroll();
    }
  });

  watch(route, (to, from) => {
    // Check if the drawer is open, and if so, close it
    if (show.value) {
      show.value = false;
    }
  });

  onMounted(() => {
    taskOp.value = store.getters.getTaskOperationByNodeId(parseInt(props.nodeId));
    taskDefinition.value = store.getters.getTaskDefinitionById(taskOp.value.task_definition);
  });


  const save = () => {
    // Your existing save logic
    emit('update');
    show.value = false;
  };
</script>

<template>
  <teleport to="body">
    <el-drawer v-model="show" direction="rtl" class="full-screen-drawer" title="Task">
      <input class="task-operation-name-input" v-model="taskOp.name" />
      <div class="task-definition">
        <img :src="getIconUrl(store.getters.getTaskDefinitionById(taskOp.task_definition).source)" class="task-definition-img" />
        <div class="task-definition-text">{{ store.getters.getTaskDefinitionById(taskOp.task_definition).name }}</div>
      </div>
      <div class="divider"></div>
      <div class="instruction-box-header">
        <div class="instruction-box-header-instructions">Instructions</div>
        <div class="instructions-box-header-optional">optional</div>
      </div>
      <textarea class="instructions-box-input"
        placeholder="We need to get the user profile before we can process this person’s request. Use the customer’s email from the metadata to look up their account."></textarea>

      <div class="dependencies-header-text">Dependencies</div>

      <div class="dependencies-sub-text">incoming</div>
      <div v-if="incomingDependencyTuples.length">
        <div v-for="(tuple, index) in incomingDependencyTuples" :key="'incoming-' + index" class="incoming-dependency">
          <div class="incoming-dependency-logo-and-task" @click="onTaskOperationClick(tuple.taskOperation)">
            <!-- Replace with dynamic content -->
            <img :src="getIconUrl(store.getters.getTaskDefinitionById(tuple.taskOperation.task_definition).source)"
              class="dependency-logo" />
            <div class="dependency-task-name">{{ tuple.taskOperation.name }}</div>
          </div>
          <div :id="'arrow-' + tuple.dependency.id" class="dependency-arrow" @click="onDependencyClick(tuple.dependency)">
            <svg class="arrow-svg" width="144" height="31" viewBox="0 0 131 31" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path d="M131 15.5L121 9.7265V21.2735L131 15.5ZM0 16.5H122V14.5H0V16.5Z" fill="#4B465C" />
            </svg>
          </div>
        </div>
      </div>
      <div v-else class="no-dependencies">None</div>
      <div class="dependencies-box">
        <div class="dependencies-sub-text">outgoing</div>
        <div v-if="outgoingDependencyTuples.length">
          <div v-for="(tuple, index) in outgoingDependencyTuples" :key="'outgoing-' + index" class="outgoing-dependency">
            <div :id="'arrow-' + tuple.dependency.id" class="dependency-arrow"
              @click="onDependencyClick(tuple.dependency)">
              <svg class="arrow-svg" width="144" height="31" viewBox="0 0 131 31" fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <path d="M131 15.5L121 9.7265V21.2735L131 15.5ZM0 16.5H122V14.5H0V16.5Z" fill="#4B465C" />
              </svg>
            </div>
            <div class="outgoing-dependency-logo-and-task" @click="onTaskOperationClick(tuple.taskOperation)">
              <!-- Replace with dynamic content -->
              <img :src="getIconUrl(store.getters.getTaskDefinitionById(tuple.taskOperation.task_definition).source)"
                class="dependency-logo" />
              <div class="dependency-task-name">{{ tuple.taskOperation.name }}</div>
            </div>
          </div>
        </div>
        <div v-else class="no-dependencies">None</div>
      </div>
      <div class="code-block-header">
        <div class="code-block-header-output">Output</div>
        <div class="instructions-box-header-optional">example</div>
      </div>
      <div class="output-example-yaml">
        <YamlCodeBlock :code="yamlData"> </YamlCodeBlock>
      </div>
    </el-drawer>
  </teleport>
</template>

<style scoped>
.full-screen-drawer {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 200px;
  /* Ensure the drawer takes full width */
}

.task-operation-name-input {
  color: var(--Light-Typography-Color-Body-Text, #5d5a58);
  font-feature-settings: "clig" off, "liga" off;
  white-space: nowrap;
  border-radius: 4px;
  border: 1.6px solid var(--light-solid-color-gray-gray-600-hover, #8b8b8a);
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  justify-content: center;
  padding: 10px 10px;
  font: 500 17px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
  margin-top: -50px !important;
  width: 100%;
}

.task-operation-name-input:focus {
  outline: none;
  /* Removes the default blue outline */
  border-color: #6a6675;
  /* Custom focus color */
}

.task-definition {
  display: flex;
  justify-content: flex-end !important;
  margin-top: 6px;
  gap: 8px;
  align-self: right;
  width: 100%;
  font-size: 1.8rem;
}

.task-definition:hover {
  .task-definition-text {
    color: var(--light-solid-color-warning-warning-700-active, #ca7d35);
    cursor: pointer;
  }
}

.task-definition-img {
  aspect-ratio: 1;
  object-fit: contain;
  width: 24px;
  overflow: hidden;
  max-width: 100%;
}

.task-definition-text {
  color: var(--light-solid-color-warning-warning-700-active, #ff9f43);
  font-feature-settings: "clig" off, "liga" off;
  white-space: nowrap;
  margin: auto 0;
  font: 500 15px/140% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.divider {
  background-color: #dbdade;
  margin-top: 23px;
  height: 1px;
}

.instruction-box-header {
  justify-content: space-between;
  display: flex;
  margin-top: 24px;
  gap: 4px;
}

.instruction-box-header-instructions {
  color: var(--Light-Typography-Color-Heading-Text, #5d5a58);
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  white-space: nowrap;
  font: 500 18px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.instructions-box-header-optional {
  color: #b7b5be;
  text-align: right;
  font-feature-settings: "clig" off, "liga" off;
  align-self: start;
  margin-top: 10px;
  white-space: nowrap;
  font: 400 11px/127% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.instructions-box-input {
  border-radius: 4px;
  border: 1.4px solid var(--light-solid-color-gray-gray-600-hover, #787779);
  background-color: var(--Light-Solid-Color-Extra-Card-Background, #fff);
  display: flex;
  margin-top: 4px;
  flex-direction: column;
  padding: 7px 0 1px 10px;
  resize: both;
  color: #454443;
  /* Allows resizing on both width and height */
  overflow: auto;
  /* Necessary for 'resize' to work */
  height: 400;
  /* Starting fixed height */
  min-height: 300px;
  /* Minimum height */
  max-height: 1000px;
  /* Optional: Constrain the max size */
  min-width: 100%;
  max-width: 100%;

}

.instructions-box-input:focus {
  outline: none;
  /* Removes the default blue outline */
  border: solid 1.6px;
  border-color: #787779;
}

.dependencies-box {
  margin-left: 0.2rem;
  margin-right: 1rem;
}

.no-dependencies {
  color: #666;
  font-style: italic;
  padding: 10px;
}

.dependencies-header-text {
  color: var(--Light-Typography-Color-Heading-Text, #5d5a58);
  font-feature-settings: "clig" off, "liga" off;
  margin-top: 24px;
  white-space: nowrap;
  font: 500 18px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
  margin-top: 1.75rem;
  margin-bottom: 0.8rem;
}

.dependencies-sub-text {
  color: #b7b5be;
  font-feature-settings: "clig" off, "liga" off;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 8px;
  font: 400 13px Helvetica Neue, sans-serif;
}

.outgoing-dependency {
  display: flex;
  align-items: center;
  margin-top: 4px;
  justify-content: space-between;
  gap: 6px;
}

.incoming-dependency {
  display: flex;
  align-items: center;
  margin-top: 4px;
  margin-right: 12px;
  justify-content: space-between;
  gap: 6px;
  margin-top: 0.5rem;
}

.dependency-arrow {
  width: 131px;
  height: 31px;
  margin-top: 4px;
  margin-bottom: 4px;
}

.arrow-svg {
  cursor: pointer;
  transition: fill 0.3s ease, stroke-width 0.3s ease;
  transform: scale(1.1, 1.1);
}

.arrow-svg:hover path {
  fill: #ca7d35;
  /* Change to the color you want on hover */
  stroke-width: 10;
  /* Change to desired stroke width on hover */
}

.outgoing-dependency-logo-and-task {
  color: #6f6b7d;
  gap: 10px;
  font-feature-settings: "clig" off, "liga" off;
  align-self: left;
  display: flex;
  white-space: nowrap;
  margin: auto 0;
  font: 500 15px/108% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.incoming-dependency-logo-and-task {
  color: #6f6b7d;
  gap: 10px;
  font-feature-settings: "clig" off, "liga" off;
  align-self: left;
  display: flex;
  white-space: nowrap;
  margin: auto 0;
  font: 500 15px/108% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.dependency-logo {
  aspect-ratio: 1;
  object-fit: contain;
  object-position: center;
  width: 20px;
  overflow: hidden;
  max-width: 100%;
}

.dependency-task-name {
  color: #5f5f5f;
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  white-space: nowrap;
  font: 500 18px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.dependency-task-name:hover {
  color: #ca7d35;
  cursor: pointer;
}

.code-block-header {
  justify-content: space-between;
  display: flex;
  margin-top: 24px;
  margin-bottom: 12px;
  gap: 4px;
}

.code-block-header-output {
  color: var(--Light-Typography-Color-Heading-Text, #4b465c);
  font-feature-settings: "clig" off, "liga" off;
  flex-grow: 1;
  white-space: nowrap;
  font: 500 18px/133% Helvetica Neue, -apple-system, Roboto, Helvetica,
    sans-serif;
}

.output-example-yaml {
  margin-top: 8px;
  border: 1px solid #aaaaaa;
  border-radius: 4px;
}
</style>