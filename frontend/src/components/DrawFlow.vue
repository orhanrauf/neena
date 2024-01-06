<script setup lang="ts">
import { TaskDefinition, TaskOperation, Dependency } from "@/types";
import DependencyDrawer from "./nodes/DependencyDrawer.vue";
import axios from 'axios';
import RequestDialog from "./dialogs/RequestDialog.vue";
import SaveFlowDialog from "./dialogs/SaveFlowDialog.vue";
import Drawflow from "../plugins/drawflow/drawflow.js";
import { defineEmits, onMounted, shallowRef, h, getCurrentInstance, render, ref, ComponentInternalInstance, ShallowRef } from "vue";
import Node from "./nodes/Node.vue";
import { useStore } from 'vuex';

const store = useStore();
const isRequestPopupVisible = ref(false);
const isSaveWorkflowPopupVisible = ref(false);
const showDrawer = ref(false);
const selectedSourceNodeId = ref(0);
const selectedTargetNodeId = ref(0);
const editor: ShallowRef = shallowRef({});
const cardVisible = ref(false);
const Vue = { version: 3, h, render };
const internalInstance = getCurrentInstance() as ComponentInternalInstance;
internalInstance.appContext.app._context.config.globalProperties.$df = editor;
const emit = defineEmits(['close-card']);


// Method to toggle the visibility of the pop-up
const requestTogglePopup = () => {
  isRequestPopupVisible.value = !isRequestPopupVisible.value;
};

const saveWorkflowTogglePopup = () => {
  isSaveWorkflowPopupVisible.value = !isSaveWorkflowPopupVisible.value;
};

// Function to handle the ESC key press
const closeOnEsc = (event) => {
  if (event.key === 'Escape') {
    isRequestPopupVisible.value = false;
    isSaveWorkflowPopupVisible.value = false;
  }
};

window.addEventListener('keydown', closeOnEsc);

onMounted(() => {
  const id = document.getElementById("drawflow");

  editor.value = new Drawflow(
    id,
    Vue,
    internalInstance.appContext.app._context
  );

  store.commit('setDrawflowEditor', editor.value);

  editor.value.curvature = 1;
  editor.value.line_path = 20;
  editor.value.reroute = true;

  editor.value.start();

  editor.value.registerNode("Node", Node, {}, {});

  editor.value.on("nodeRemoved", (nodeId) => {
    store.commit('deleteTaskOperation', nodeId);
  });

  editor.value.on("connectionRemoved", (connection) => {
    connectionRemoved(connection);
  });

  editor.value.on("connectionCreated", (connection) => {
    // {output_id: '2', input_id: '1', output_class: 'output_1', input_class: 'input_1'}
    const source_node_id = parseInt(connection.output_id);
    const target_node_id = parseInt(connection.input_id);

    var dependency: Dependency = {
      source_node_id: source_node_id,
      target_node_id: target_node_id,
      instructions: ''
    }
    store.commit('addDependency', dependency);
  });

  editor.value.on('connectionDoubleClicked', (connection) => {
    console.log('botot')
    showDrawer.value = true;
    selectedSourceNodeId.value = connection.input_id;
    selectedTargetNodeId.value = connection.output_id;
  });
})

const connectionRemoved = (connection) => {
  store.commit('deleteDependencyByTargetNodeId', connection.input_id);
};

onUnmounted(() => {
  window.removeEventListener('keydown', closeOnEsc);
});

const toggleTaskListCard = () => {
  cardVisible.value = !cardVisible.value;
};

const getNewTaskOpName = (taskDefinition: TaskDefinition): string => {
  const exportData = editor.value.export();
  const nodes = exportData.drawflow.Home.data;
  let maxNumber = 0;
  let baseNameExists = false;

  Object.keys(nodes).forEach((key) => {
    const node = nodes[key];
    if (node.name === taskDefinition.name) {
      baseNameExists = true;
    }
    if (node.name.startsWith(taskDefinition.name)) {
      const matches = node.name.match(/_(\d+)$/);
      if (matches && matches.length > 1) {
        const number = parseInt(matches[1]);
        if (number > maxNumber) {
          maxNumber = number;
        }
      }
    }
  });

  if (baseNameExists) {
    return maxNumber > 0 ? `${taskDefinition.name}_${maxNumber + 1}` : `${taskDefinition.name}_2`;
  } else {
    return taskDefinition.name;
  }
};

const addBlankTaskOp = (taskDefinition: TaskDefinition) => {
  const taskOpName = getNewTaskOpName(taskDefinition);
  var nextNodeId = editor.value.nodeId;
  var taskOp: TaskOperation = {
    drawflow_node_id: nextNodeId,
    name: taskOpName,
    task_definition: taskDefinition.id,
    instructions: '',
    x: 400,
    y: 150
  }

  store.commit('addTaskOperation', taskOp);

  editor.value.addNode(
    taskOpName /* name */,
    1 /* inputs */,
    1 /* outputs */,
    taskOp.x /* pos_x */,
    taskOp.y /* pos_y */,
    "node" /* class */,
    {} /* data, retrieved from vuex state */,
    "Node" /* html */,
    "vue" /* typenode */
  );
};

</script>

<template>
  <div>
    <el-container>
      <el-header class="header">
        <VRow class="d-flex justify-space-between align-center full-width">

          <!-- Left Group -->
          <div class="d-flex align-center gap">
            <!-- Add task button -->
            <VBtn class="add-task-btn" @click="cardVisible = !cardVisible" prepend-icon="tabler-plus">
              Add Task
            </VBtn>

            <!-- Request icon -->
            <el-button @click="requestTogglePopup" class="icon-container request-icon-container">
              <v-icon color="#494949">tabler-message</v-icon>
            </el-button>
          </div>

          <!-- Right Group -->
          <div class="d-flex align-center gap">
            <!-- Save icon -->
            <el-button @click="saveWorkflowTogglePopup" class="icon-container save-icon-container">
              <v-icon color="#494949">tabler-device-floppy</v-icon>
            </el-button>

            <!-- Run Flow button -->
            <VBtn class="run-flow-btn" prepend-icon="tabler-bolt">
              Run Flow
            </VBtn>
          </div>

          <!-- Request pop-up component -->
          <div v-if="isRequestPopupVisible" class="request-popup-overlay" @click.self="requestTogglePopup">
            <RequestDialog class="request-popup-container" @close="requestTogglePopup"></RequestDialog>
          </div>

          <!-- Save workflow pop-up component -->
          <div v-if="isSaveWorkflowPopupVisible" class="request-popup-overlay" @click.self="saveWorkflowTogglePopup">
            <SaveFlowDialog class="request-popup-container" @close="saveWorkflowTogglePopup"></SaveFlowDialog>
          </div>

        </VRow>
      </el-header>
      <!-- Actual Drawflow container -->
      <el-container class="drawflow-container">
        <el-main>

          <TaskListCard v-if="cardVisible" class="task-list-card" @close-card="toggleTaskListCard"
            @add-task="addBlankTaskOp" />

          <div id="drawflow"></div>
        </el-main>
      </el-container>
    </el-container>
    <DependencyDrawer v-if="showDrawer" v-model="showDrawer" :source-node-id="selectedSourceNodeId" :target-node-id="selectedTargetNodeId"/>
  </div>
</template>

<style scoped>
.request-popup-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.15);
  /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(2px);
  z-index: 100;
  /* Make sure it's above all other content */
}

.request-popup-container {
  z-index: 101;
  /* Above the overlay */
}

/* When the pop-up is visible, blur the background content */
body.blurred {
  overflow: hidden;
  filter: blur(5px);
}

.gap {
  gap: 10px;
  /* Adjust the gap size as needed */
}

.add-task-btn {
  color: #fff !important;
}

.icon-container {
  justify-content: center;
  border-radius: 6px;
  border: 1px solid var(--Light-Solid-Color-Gray-Gray---900, #494949);
  display: flex;
  align-items: center;
  background-color: #eefaff;
  display: flex;
  flex-direction: column;
  width: 38px;
  height: 38px;
  padding: 0 8px;
}

.request-icon-container {
  background-color: #f0f9fc;
}

.request-icon-container:hover {
  background-color: #b3cad9;
}

.save-icon-container {
  background-color: #ffbf84;
}

.save-icon-container:hover {
  background-color: #df985e;
}

.run-flow-btn {
  background-color: #FF9F43 !important;
  color: #494949 !important;
  border: 1px solid #494949 !important;
  /* Removes the border */

}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-block-end: 1px solid #494949;
}

.task-list-card {
  position: absolute;
  top: 40px;
  left: 40px;
  z-index: 10;
  /* Ensure it's above the Drawflow container */
}

.drawflow-container {
  min-block-size: calc(100vh - 220px);
  position: relative;
  padding-top: 0.6rem;
}
</style>

<style>
.el-main {
  padding: 0;
}

.drawflow .drawflow-node {
  width: 346px !important;
  padding: 0 !important;
}

.header {
  margin-block: 0 !important;
  margin-inline: 0 !important;
}

.drawflow .drawflow-node.node {
  background: #fff;
  border: 2px solid #4b465c;
}

.drawflow .drawflow-node.node.selected {
  background: #fff;
}

.drawflow .drawflow-node.node .input,
.drawflow .drawflow-node.node .output {
  background: #d9d9d9;
  border: 1px solid #4b465c;
}

#drawflow {
  background: #494949;
  background-image: radial-gradient(transparent 1px, #FAFAF7 1px);
  background-size: 20px 20px;
  block-size: 100%;
  inline-size: 100%;
  text-align: initial;
}

.drawflow .connection .main-path {
  stroke-width: 3px !important;
  stroke: #6e6b78 !important;
}

.drawflow .connection .main-path.selected {
  stroke: #e38c3b !important;
  stroke-width: 3.5px !important;

}
</style>
<style src="../plugins/drawflow/drawflow.css"></style>
x