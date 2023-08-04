<script setup>
import Drawflow from "drawflow";
import { onMounted, shallowRef, h, getCurrentInstance, render, ref } from "vue";
import Node from "./nodes/Node.vue";

const editor = shallowRef({});
const dialogVisible = ref(false);
const dialogData = ref({});
const Vue = { version: 3, h, render };
const internalInstance = getCurrentInstance();
internalInstance.appContext.app._context.config.globalProperties.$df = editor;

function exportEditor() {
  dialogData.value = editor.value.export();
  dialogVisible.value = true;
}
const drag = (ev) => {
  if (ev.type === "touchstart") {
    mobile_item_selec = ev.target
      .closest(".drag-drawflow")
      .getAttribute("data-node");
  } else {
    ev.dataTransfer.setData("node", ev.target.getAttribute("data-node"));
  }
};
const drop = (ev) => {
  if (ev.type === "touchend") {
    var parentdrawflow = document
      .elementFromPoint(
        mobile_last_move.touches[0].clientX,
        mobile_last_move.touches[0].clientY
      )
      .closest("#drawflow");
    if (parentdrawflow != null) {
      addNodeToDrawFlow(
        mobile_item_selec,
        mobile_last_move.touches[0].clientX,
        mobile_last_move.touches[0].clientY
      );
    }
    mobile_item_selec = "";
  } else {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("node");
    addNodeToDrawFlow(data, ev.clientX, ev.clientY);
  }
};
const allowDrop = (ev) => {
  ev.preventDefault();
};
let mobile_item_selec = "";
let mobile_last_move = null;
function positionMobile(ev) {
  mobile_last_move = ev;
}
function addNodeToDrawFlow(name, pos_x, pos_y) {
  pos_x =
    pos_x *
      (editor.value.precanvas.clientWidth /
        (editor.value.precanvas.clientWidth * editor.value.zoom)) -
    editor.value.precanvas.getBoundingClientRect().x *
      (editor.value.precanvas.clientWidth /
        (editor.value.precanvas.clientWidth * editor.value.zoom));
  pos_y =
    pos_y *
      (editor.value.precanvas.clientHeight /
        (editor.value.precanvas.clientHeight * editor.value.zoom)) -
    editor.value.precanvas.getBoundingClientRect().y *
      (editor.value.precanvas.clientHeight /
        (editor.value.precanvas.clientHeight * editor.value.zoom));
}

onMounted(() => {
  const elements = document.getElementsByClassName("drag-drawflow");
  for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener("touchend", drop, false);
    elements[i].addEventListener("touchmove", positionMobile, false);
    elements[i].addEventListener("touchstart", drag, false);
  }

  const id = document.getElementById("drawflow");
  editor.value = new Drawflow(
    id,
    Vue,
    internalInstance.appContext.app._context
  );
  editor.value.start();

  editor.value.registerNode("Node", Node, {}, {});
});

const addTask = (taskDefinition) => {
  editor.value.addNode(
    "Node" /* name */,
    1 /* inputs */,
    1 /* outputs */,
    100 /* pos_x */,
    100 /* pos_y */,
    "node" /* class */,
    { ...taskDefinition } /* data */,
    "Node" /* html */,
    "vue" /* typenode */
  );
};
</script>

<template>
  <div>
    <el-container>
      <el-header class="header">
        <VRow class="d-flex gap-4 justify-space-between">
          <!-- Add task button -->
          <AddTaskModal @addTask="addTask" />

          <!-- Action butotns -->
          <div class="d-flex gap-4">
            <VBtn prepend-icon="tabler:adjustments-code" color="success">
              Run Flow
            </VBtn>
            <VBtn
              prepend-icon="tabler:device-floppy"
              color="secondary"
              @click="exportEditor"
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
            @drop="drop($event)"
            @dragover="allowDrop($event)"
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
          <el-button type="primary" @click="dialogVisible = false"
            >Confirm</el-button
          >
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
