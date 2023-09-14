<script setup lang="ts">
import axios from "@axios"
import Drawflow from "drawflow"
import { onMounted, shallowRef, h, getCurrentInstance, render, ref, ComponentInternalInstance, ShallowRef } from "vue"
import { useToast } from "vue-toastification"
import Node from "./nodes/Node.vue";

const props = defineProps<{
  flowRequestId: string,
}>();

const toast = useToast();

const editor: ShallowRef = shallowRef({});
const dialogVisible = ref(false);
const dialogData = ref({});
const Vue = { version: 3, h, render };

const internalInstance = getCurrentInstance() as ComponentInternalInstance;
internalInstance.appContext.app._context.config.globalProperties.$df = editor;

onMounted(() => {
  const id = document.getElementById("drawflow");
  editor.value = new Drawflow(
    id,
    Vue,
    internalInstance.appContext.app._context
  );
  editor.value.start();

  editor.value.registerNode("Node", Node, {}, {});

  editor.value.on("connectionCreated", function (connection: any) {
    connectionCreated(connection);
  });

  editor.value.on("connectionRemoved", function (connection: any) {
    connectionRemoved(connection);
  });
});

const getNewTaskName = (taskDefinition: any): string => {
  const exportData = editor.value.export();
  const nodes = exportData.drawflow.Home.data;
  let existingTaskName: string | null = null;

  Object.keys(nodes).forEach((key) => {
    const node = nodes[key];

    if (node.data.task_definition.task_name.startsWith(taskDefinition.task_name)) {
      existingTaskName = node.data.task_definition.task_name;
    }
  });

  if (existingTaskName) {
    const matches = existingTaskName.match(/_(\d+)$/);
    if (matches && matches.length > 0) {
      const number = parseInt(matches[1]) + 1;

      return taskDefinition.task_name + '_' + number;
    }
  }

  return taskDefinition.task_name + '_1';
}

const addTask = (taskDefinition: any) => {
  const inputCount = taskDefinition.parameters.length;
  const newName = getNewTaskName(taskDefinition);

  taskDefinition.task_name = newName;

  editor.value.addNode(
    newName /* name */,
    inputCount /* inputs */,
    1 /* outputs */,
    100 /* pos_x */,
    100 /* pos_y */,
    "node" /* class */,
    {
      task_definition: taskDefinition,
    } /* data */,
    "Node" /* html */,
    "vue" /* typenode */
  );
};

const connectionCreated = (connection: any) => {
  const inputNode = editor.value.getNodeFromId(connection.input_id);
  const outputNode = editor.value.getNodeFromId(connection.output_id);

  const inputClassSplit = connection.input_class.split("_");
  const inputIndex = parseInt(inputClassSplit[1]) - 1;

  const parameters = inputNode.data.task_definition.parameters;
  parameters[inputIndex].source = "@tasks()";
  parameters[
    inputIndex
  ].value = `${outputNode.data.task_definition.task_name}.output`;

  editor.value.updateNodeDataFromId(connection.input_id, {
    ...inputNode.data,
    parameters: parameters,
  });
};

const connectionRemoved = (connection: any) => {
  const inputNode = editor.value.getNodeFromId(connection.input_id);

  const inputClassSplit = connection.input_class.split("_");
  const inputIndex = parseInt(inputClassSplit[1]) - 1;

  const parameters = inputNode.data.task_definition.parameters;
  parameters[inputIndex].source = null;
  parameters[inputIndex].value = "";

  editor.value.updateNodeDataFromId(connection.input_id, {
    ...inputNode.data,
    parameters: parameters,
  });
};

const saveWorkflow = () => {
  // Get all the nodes from the workflow
  const exportData = editor.value.export();
  const nodes = exportData.drawflow.Home.data;
  const nodeKeys = Object.keys(nodes);

  const flowRequestId = props.flowRequestId;

  // Create task operations object
  const taskOperations = nodeKeys.map((key) => {
    const node = nodes[key];

    return {
      name: node.data.task_definition.task_name,
      task_definition: node.data.task_definition.id,
      arguments: node.data.task_definition.parameters.map((parameter: any) => {
        return {
          name: parameter.name,
          data_type: parameter.data_type,
          value: parameter.value,
          source: parameter.source,
        }
      }),
      explanation: node.data.task_definition.description,
      x: node.pos_x,
      y: node.pos_y,
      z: 0,
    }
  });

  // Create the flow through the API
  axios
    .post('/v1/flows', {
      flow_request: flowRequestId,
      name: 'No name',
      task_operations: taskOperations,
    })
      .then((response) => {
        toast.success('Flow successfully created!');
        // Clear the drawflow
        editor.value.clear();
      })
      .catch((error) => {
        toast.error('Something went wrong during the API call');
        console.error(error);
      });
}
</script>

<template>
  <div>
    <el-container>
      <el-header class="header">
        <VRow class="d-flex gap-4 justify-space-between">
          <!-- Add task button -->
          <AddTaskModal @addTask="addTask" />

          <!-- Action buttons -->
          <div class="d-flex gap-4">
            <VBtn prepend-icon="tabler:adjustments-code" color="success">
              Run Flow
            </VBtn>
            <VBtn
              prepend-icon="tabler:device-floppy"
              color="secondary"
              @click="saveWorkflow"
            >
              Save Flow
            </VBtn>
          </div>
        </VRow>
      </el-header>

      <!-- Actual Drawflow container -->
      <el-container class="container">
        <el-main>
          <div
            id="drawflow"
          ></div>
        </el-main>
      </el-container>
    </el-container>

    <!-- Export dialog -->
    <el-dialog v-model="dialogVisible" title="Export" width="50%">
      <span>Data:</span>
      <pre><code>{{ dialogData }}</code></pre>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="dialogVisible = false">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-block-end: 1px solid #494949;
}

.container {
  min-block-size: calc(100vh - 250px);
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
  background-image: radial-gradient(transparent 1px, #f8f7fa 1px);
  background-size: 20px 20px;
  block-size: 100%;
  inline-size: 100%;
  text-align: initial;
}

.drawflow .connection .main-path {
  stroke-width: 2px !important;
  stroke: #4b465c !important;
}

.drawflow .connection .main-path.selected {
  stroke: #5b4d80 !important;
}
</style>
<style src="drawflow/dist/drawflow.min.css"></style>
