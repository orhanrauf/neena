<script>
import Drawflow from "drawflow";
import {
  onMounted,
  shallowRef,
  h,
  getCurrentInstance,
  render,
  readonly,
  ref,
} from "vue";
import Node1 from "./nodes/node1.vue";
import Node2 from "./nodes/node2.vue";
import Node3 from "./nodes/node3.vue";

export default {
  name: "drawflow",
  setup() {
    const listNodes = readonly([
      {
        name: "Get/Post",
        color: "#49494970",
        item: "Node1",
        input: 0,
        output: 1,
      },
      {
        name: "Script",
        color: "blue",
        item: "Node2",
        input: 1,
        output: 2,
      },
      {
        name: "console.log",
        color: "#ff9900",
        item: "Node3",
        input: 1,
        output: 0,
      },
    ]);

    const editor = shallowRef({});
    const dialogVisible = ref(false);
    const dialogData = ref({});
    const Vue = { version: 3, h, render };
    const internalInstance = getCurrentInstance();
    internalInstance.appContext.app._context.config.globalProperties.$df =
      editor;

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

      const nodeSelected = listNodes.find((ele) => ele.item == name);
      editor.value.addNode(
        name,
        nodeSelected.input,
        nodeSelected.output,
        pos_x,
        pos_y,
        name,
        {},
        name,
        "vue"
      );
    }
    onMounted(() => {
      var elements = document.getElementsByClassName("drag-drawflow");
      for (var i = 0; i < elements.length; i++) {
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

      editor.value.registerNode("Node1", Node1, {}, {});
      editor.value.registerNode("Node2", Node2, {}, {});
      editor.value.registerNode("Node3", Node3, {}, {});
      editor.value.import({
        drawflow: {
          Home: {
            data: {
              5: {
                id: 5,
                name: "Node2",
                data: { script: "(req,res) => {\n console.log(req);\n}" },
                class: "node",
                html: "Node2",
                typenode: "vue",
                inputs: {
                  input_1: { connections: [{ node: "6", input: "output_1" }] },
                },
                outputs: {
                  output_1: { connections: [] },
                  output_2: { connections: [] },
                },
                pos_x: 1000,
                pos_y: 117,
              },
              6: {
                id: 6,
                name: "Node1",
                data: { url: "localhost/add", method: "post" },
                class: "node",
                html: "Node1",
                typenode: "vue",
                inputs: {},
                outputs: {
                  output_1: { connections: [{ node: "5", output: "input_1" }] },
                },
                pos_x: 137,
                pos_y: 89,
              },
            },
          },
        },
      });
    });
    return {
      exportEditor,
      listNodes,
      drag,
      drop,
      allowDrop,
      dialogVisible,
      dialogData,
    };
  },
};
</script>

<template>
  <div>
    <el-container>
      <el-header class="header">
        <VRow class="d-flex gap-4 justify-space-between">
          <!-- Add task button -->
          <AddTaskModal />

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

      <el-container class="container">
        <!--        <el-aside width="250px" class="column">-->
        <!--          <ul>-->
        <!--            <li-->
        <!--              v-for="n in listNodes"-->
        <!--              :key="n"-->
        <!--              draggable="true"-->
        <!--              :data-node="n.item"-->
        <!--              @dragstart="drag($event)"-->
        <!--              class="drag-drawflow"-->
        <!--            >-->
        <!--              <div class="node" :style="`background: ${n.color}`">-->
        <!--                {{ n.name }}-->
        <!--              </div>-->
        <!--            </li>-->
        <!--          </ul>-->
        <!--        </el-aside>-->
        <el-main>
          <div
            id="drawflow"
            @drop="drop($event)"
            @dragover="allowDrop($event)"
          ></div>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog v-model="dialogVisible" title="Export" width="50%">
      <span>Data:</span>
      <pre><code>{{dialogData}}</code></pre>
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

.drawflow .drawflow-node.node {
  background: #fff;
  border: 2px solid #4b465c;
}

.drawflow .drawflow-node.node.selected {
  background: #f1f1f1;
}

.drawflow .drawflow-node.node .header {
  background: rgba(103, 182, 240, 0.4);
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

/*.column {
  border-inline-end: 1px solid #494949;
}

.column ul {
  padding-block: 10px;
  padding-inline: 10px;
  padding-inline-start: 0;
}

.column li {
  background: transparent;
}*/
</style>
<style src="drawflow/dist/drawflow.min.css"></style>
