// store/index.js
import { createStore } from 'vuex';
import VuexPersist from 'vuex-persist';

// await store.commit('setUser', user.value);
// await store.commit('setAuthDateTimestamp', Date.now());

const vuexPersist = new VuexPersist({
    key: 'neena', // The key to store the state on in the storage provider.
    storage: window.localStorage, // or window.sessionStorage or localForage
    // You can also specify the parts of the state you want to persist.
    reducer: (state) => ({
        auth: state.auth, // only persist the auth module
        // add other modules that you want to persist here
    }),
});

// Create a new store instance.
const store = createStore({
    state() {
        return {
            auth: {
                token: null,
                user: null,
                authDateTimestamp: null,
            },
            flowCreation: {
                flowRequest: {}, // flow request
                drawflowEditor: null, // entire DrawFlow object
                flow: {
                    name: '',
                    task_operations: [],
                    dependencies: [],
                },
                isGenerating: false,
                error: null,
                isSaveWorkflowPopupVisible: false,
            },
            flowExecution: {
                flow: {},
                flowRun: {},
                latestUpdate: null,
            },
            taskDefinitions: [],
            integrations: [],
            flowRequests: [],
            flows: [],
            flowRun: {},
        };
    },
    getters: {
        token: (state) => state.auth.token,
        user: (state) => state.auth.user,
        taskDefinitions: (state) => state.taskDefinitions,
        // Getter to find a task operation by drawflow_node_id
        getTaskOperationByNodeId: (state) => (nodeId) => {
            // Assuming taskOperations is an array in state.flowCreation.flow
            const task_operations = state.flowCreation.flow.task_operations;

            // Find the task operation with the matching drawflow_node_id
            const taskOperation = task_operations.find(
                (operation) => operation.drawflow_node_id === nodeId
            );

            return taskOperation || null; // Return the found operation or null if not found
        },
        getTaskOperationByIndex: (state) => (index) => {
            const task_operations = state.flowCreation.flow.task_operations;
            const taskOperation = task_operations.find(
                (operation) => operation.index === index
            );
            return taskOperation || null;
        },
        // Getter for finding a task definition by id
        getTaskDefinitionById: (state) => (id) => {
            // Assuming taskDefinitions is an array in state
            const taskDefinitions = state.taskDefinitions;

            // Find the task definition with the matching id
            const taskDefinition = taskDefinitions.find(
                (definition) => definition.id === id
            );

            return taskDefinition || null; // Return the found definition or null if not found
        },
        // Getter for finding an integration by id
        getIntegrationById: (state) => (id) => {
            // Assuming integrations is an array in state
            const integrations = state.integrations;

            // Find the integration with the matching id
            const integration = integrations.find(
                (integration) => integration.id === id
            );

            return integration || null; // Return the found integration or null if not found
        },
        getDependenciesBySourceNodeId: (state) => (sourceNodeId) => {
            const dependencies = state.flowCreation.flow.dependencies;
            return dependencies.filter(
                (dependency) => dependency.source_drawflow_node_id === sourceNodeId
            );
        },
        getDependenciesByTargetNodeId: (state) => (targetNodeId) => {
            const dependencies = state.flowCreation.flow.dependencies;
            return dependencies.filter(
                (dependency) => dependency.target_drawflow_node_id === targetNodeId
            );
        },
        getTaskOperationsThatThisTaskOperationDependsOn: (state) => (taskOperation) => {
            const dependencies = state.flowCreation.flow.dependencies;
            const task_operations = state.flowCreation.flow.task_operations;
            const dependencyIds = dependencies
                .filter(
                    (dependency) =>
                        dependency.target_drawflow_node_id ===
                        taskOperation.drawflow_node_id
                )
                .map((dependency) => dependency.source_drawflow_node_id);
            return task_operations.filter((operation) =>
                dependencyIds.includes(operation.drawflow_node_id)
            );
        },
        getTaskOperationsThatDependOnThisTaskOperation: (state) => (taskOperation) => {
            const dependencies = state.flowCreation.flow.dependencies;
            const task_operations = state.flowCreation.flow.task_operations;
            const dependencyIds = dependencies
                .filter(
                    (dependency) =>
                        dependency.source_drawflow_node_id ===
                        taskOperation.drawflow_node_id
                )
                .map((dependency) => dependency.target_drawflow_node_id);
            return task_operations.filter((operation) =>
                dependencyIds.includes(operation.drawflow_node_id)
            );
        },
        getDependencyBySourceAndTargetNodeId: (state) => (sourceNodeId, targetNodeId) => {
            const dependencies = state.flowCreation.flow.dependencies;
            const index = dependencies.findIndex(
                (dependency) =>
                    dependency.source_drawflow_node_id === sourceNodeId &&
                    dependency.target_drawflow_node_id === targetNodeId
            );
            return dependencies[index];
        },
        getDrawFlowNodeXandY: (state) => (drawflowNodeId) => {
            const editor = state.flowCreation.drawflowEditor;
            const exportData = editor.export();
            const nodes = exportData.drawflow.Home.data;
            const node = nodes[drawflowNodeId];
            return { x: node.pos_x, y: node.pos_y };
        }
    },
    mutations: {
        setFlows(state, flows) {
            state.flows = flows;
        },
        startFlowGeneration(state) {
            state.flowCreation.isGenerating = true;
            state.flowCreation.flow = null;
            state.flowCreation.error = null;
        },
        flowGenerationSuccess(state, flow) {
            state.flowCreation.isGenerating = false;
            state.flowCreation.flow = flow;
        },
        flowGenerationFailure(state, error) {
            state.flowCreation.isGenerating = false;
            state.flowCreation.error = error;
        },
        saveToken(state, token) {
            state.auth.token = token;
        },
        setUser(state, user) {
            state.auth.user = user;
        },
        setAuthDateTimestamp(state, timestamp) {
            state.auth.authDateTimestamp = timestamp;
        },
        logOut(state, user) {
            state.auth.token = null;
            state.auth.user = null;
            state.auth.authDateTimestamp = null;

            // Clear only the auth data under 'neena.auth' in local storage
            const neenaData = JSON.parse(localStorage.getItem('neena') || '{}');
            delete neenaData.auth;
            localStorage.setItem('neena', JSON.stringify(neenaData));
        },
        setRequest(state, flowRequest) {
            state.flowCreation.flowRequest = flowRequest;
        },
        setDrawflowEditor(state, drawflowEditor) {
            state.flowCreation.drawflowEditor = drawflowEditor;
        },
        setTaskDefinitions(state, taskDefinitions) {
            state.taskDefinitions = taskDefinitions;
        },
        setFlowRun(state, flowRun) {
            state.flowExecution.flowRun = flowRun;
            state.flowExecution.latestUpdate = Date.now();

        },
        // Task operation mutations
        addTaskOperation(state, taskOperation) {
            taskOperation.index = getNewTaskOpIndex(state);
            state.flowCreation.flow.task_operations.push(taskOperation);
        },
        addDrawFlowNodeIdToTaskOperation(state, { taskOperationId, drawflowNodeId }) {
            const task_operations = state.flowCreation.flow.task_operations;
            const index = task_operations.findIndex(
                (operation) => operation.id === taskOperationId
            );
            task_operations[index].drawflow_node_id = drawflowNodeId;
        },
        editTaskOperation(state, taskOperation) {
            const task_operations = state.flowCreation.flow.task_operations;
            const index = task_operations.findIndex(
                (operation) =>
                    operation.drawflow_node_id ===
                    taskOperation.drawflow_node_id
            );
            state.flowCreation.flow.taskOperations[index] = taskOperation;
        },
        deleteTaskOperation(state, drawflowNodeId) {
            const task_operations = state.flowCreation.flow.task_operations;
            const index = task_operations.findIndex(
                (operation) => operation.drawflow_node_id === drawflowNodeId
            );
            state.flowCreation.flow.task_operations.splice(index, 1);
        },
        // Dependency mutations
        addDependency(state, dependency) {
            console.log('Adding dependency', dependency);
            state.flowCreation.flow.dependencies.push(dependency);
        },
        addDependencyIfNotExists: (state, payload) => {
            const dependencies = state.flowCreation.flow.dependencies;
            const { sourceDrawflowNodeId, targetDrawflowNodeId, sourceTaskOperation, targetTaskOperation } = payload;
            if (!checkIfDependencyExists(state, sourceDrawflowNodeId, targetDrawflowNodeId)) {
                const dependency = {
                    source_drawflow_node_id: sourceDrawflowNodeId,
                    target_drawflow_node_id: targetDrawflowNodeId,
                    source_task_operation: sourceTaskOperation.index,
                    target_task_operation: targetTaskOperation.index,
                };
                dependencies.push(dependency);
            }
        },
        deleteDependencyByTargetNodeId(state, targetNodeId) {
            const dependencies = state.flowCreation.flow.dependencies;
            const index = dependencies.findIndex(
                (dependency) => dependency.target_drawflow_node_id === targetNodeId
            );
            state.flowCreation.flow.dependencies.splice(index, 1);
        },
        deleteDependencyBySourceNodeId(state, sourceNodeId) {
            const dependencies = state.flowCreation.flow.dependencies;
            const index = dependencies.findIndex(
                (dependency) => dependency.source_drawflow_node_id === sourceNodeId
            );
            state.flowCreation.flow.dependencies.splice(index, 1);
        },
        setIntegrations(state, integrations) {
            state.integrations = integrations;
        },
        setFlowRequests(state, flowRequests) {
            state.flowRequests = flowRequests;
        },
        setFlow(state, flow) {
            state.flowCreation.flow = flow;
        },
        setFlowForFlowExecution(state, flow) {
            state.flowExecution.flow = flow;
        }
    },
    actions: {
        buildDrawFlowFromApi: ({ state, commit, getters }, flow) => {
            const editor = state.flowCreation.drawflowEditor;
            const { task_operations, dependencies } = flow;

            // Clear existing nodes and connections
            editor.clear();

            var xPlus = 200;
            var yPlus = 100;

            const coordinatesAreSet = task_operations.every((taskOperation) => taskOperation.x && taskOperation.y);

            task_operations.sort((a, b) => a.sorted_index - b.sorted_index);

            task_operations.forEach((taskOperation) => {
                // Manually manage nextNodeId to ensure consistency
                const nextNodeId = editor.nodeId;

                commit('addDrawFlowNodeIdToTaskOperation', {
                    taskOperationId: taskOperation.id,
                    drawflowNodeId: nextNodeId
                });

                editor.addNode(
                    taskOperation.name,
                    1, // inputs
                    1, // outputs
                    taskOperation.x || (coordinatesAreSet ? taskOperation.x : Math.floor(Math.random() * 100) + xPlus),
                    taskOperation.y || (coordinatesAreSet ? taskOperation.y : Math.floor(Math.random() * 100) + yPlus),
                    "node",
                    {},
                    "Node",
                    "vue"
                );

                xPlus += 600;
                yPlus += 150;
            });

            setTimeout(() => {
                // Add dependencies using the drawflow node IDs
                dependencies.forEach((dependency) => {
                    const sourceNodeId = getters.getTaskOperationByIndex(dependency.source_task_operation).drawflow_node_id;
                    const targetNodeId = getters.getTaskOperationByIndex(dependency.target_task_operation).drawflow_node_id;
                    
                    dependency.source_drawflow_node_id = sourceNodeId;
                    dependency.target_drawflow_node_id = targetNodeId;
                    editor.addConnection(
                        sourceNodeId.toString(),
                        targetNodeId.toString(),
                        "output_1", // output index
                        "input_1", // input index
                    );
                });
              }, 200);
        },
        async generateFlow({ commit }, flowRequestId) {
            commit('startFlowGeneration');
            try {
              const response = await http.get(`flows/generate?flow_request_id=${flowRequestId}`);
              commit('flowGenerationSuccess', response.data);
            } catch (error) {
              commit('flowGenerationFailure', error);
            }
          },
        fetchTaskDefinitions: async ({ commit, state }) => {
            if (state.taskDefinitions.length === 0) {
                const response = await http.get('/task_definitions/all');
                const taskDefinitions = response.data;
                commit('setTaskDefinitions', taskDefinitions);
            }
        },
        fetchFlows: async ({ commit, state }, id) => {
            const response = await http.get(`/flows/all?limit=20`);
            const flows = response.data;
            commit('setFlows', flows);
            return flows;
        },
        fetchFlowById: async ({ commit, state }, id) => {
            const response = await http.get(`/flows/?id=${id}`);
            state.flowCreation.flow = response.data;
            return response.data;
        },
        fetchFlowRequests: async ({ commit, state }) => {
            const response = await http.get('/flow_requests/all');
            const flowRequests = response.data;
            commit('setFlowRequests', flowRequests);
        },
        deleteFlowRequests: async ({ commit, state }, id) => {
            const response = await http.delete(`/flow_requests/?id=${id}`);

            if (response.status === 200) {
                state.flowRequests = state.flowRequests.filter(
                    (fr) => fr.id !== id
                );
            }
            return response.status;
        },
        fetchFlowRequestDetail: async ({ commit, state }, id) => {
            const response = await http.get(`/flow_requests/?id=${id}`);
            const flowRequestDetail = response.data;
            return flowRequestDetail;
        },
        fetchIntegrations: async ({ commit, state }) => {
            if (state.integrations.length === 0) {
                const response = await http.get('/integrations/all');
                const integrations = response.data; 
                console.log('Integrations', integrations);
                commit('setIntegrations', integrations);
            }
        },
        addBlankTaskOp: ({ state, rootGetters, commit }, taskDefinition) => {
            const editor = state.flowCreation.drawflowEditor;
            const taskOpName = getNewTaskOpName(state, taskDefinition);
            const nextNodeId = editor.nodeId;
            const taskOp = {
                drawflow_node_id: nextNodeId,
                name: taskOpName,
                task_definition: taskDefinition.id,
                instructions: '',
                x: 400,
                y: 150
            };

            commit('addTaskOperation', taskOp);

            editor.addNode(
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
        },
        saveFlowRequest: async ({ state, commit }) => {
            const flow = state.flowCreation.flow;
            const response = await http.post('/flow_requests/', flow);
            return response;
        },
        saveFlow: async ({ state, commit, getters }) => {
            const flow = state.flowCreation.flow;
            const taskOperations = flow.task_operations;
            // Update x and y directly within the taskOperations array
            taskOperations.forEach(taskOperation => {
                const { x, y } = getters.getDrawFlowNodeXandY(taskOperation.drawflow_node_id);
                taskOperation.x = x;
                taskOperation.y = y;
            });

            let response;
            if (flow.id) {
                response = await http.put(`/flows/`, flow);
            } else {
                response = await http.post('/flows/', flow);
            }
            // Update the flow in your state to reflect any changes from the server
            state.flowCreation.flow = response.data;
            
            return response;
        },
        updateFlowRequestWithFlowId: async ({ state, commit }, flow) => {;
            var flowRequest = state.flowCreation.flowRequest;
            flowRequest.flow = flow.id;
            const response = await http.put('/flow_requests/', flowRequest);
            return response;
        },
        executeFlow: async ({ state, commit }, {flowId, flowRequestId}) => {
            const response = await http.post(`/flows/execute?flow_id=${flowId}&flow_request_id=${flowRequestId}`);
            state.flowExecution.flowRun = response.data;
            return response;
        },
        getFlowRun: async ({ commit }, flowRunId) => {
            try {
              const response = await http.get(`/flow_runs?id=${flowRunId}`);
              commit('setFlowRun', response.data);
            } catch (error) {
              console.error(error);
            }
          },
    },
    plugins: [vuexPersist.plugin]
});

function getNewTaskOpIndex(state) {
    if (!state.flowCreation.flow.task_operations) {
        return 0;
    }
    const task_operations = state.flowCreation.flow.task_operations;
    return task_operations.length > 0
        ? Math.max(...task_operations.map((op) => op.index)) + 1
        : 0;
}

function checkIfDependencyExists(state, sourceDrawflowNodeId, targeDrawFlowtNodeId) {
    const dependencies = state.flowCreation.flow.dependencies;
    return dependencies.some(
        (dependency) =>
            dependency.source_drawflow_node_id === sourceDrawflowNodeId &&
            dependency.target_drawflow_node_id === targeDrawFlowtNodeId
    );
}

function getNewTaskOpName(state, taskDefinition) {
    const editor = state.flowCreation.drawflowEditor;
    const exportData = editor.export();
    const nodes = exportData.drawflow.Home.data;
    let maxNumber = 0;
    let baseNameExists = false;
    
    Object.keys(nodes).forEach((key) => {
      const node = nodes[key];
      if (node.name === taskDefinition.task_name) {
        baseNameExists = true;
      }
      if (node.name.startsWith(taskDefinition.task_name)) {
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
      return maxNumber > 0 ? `${taskDefinition.task_name}_${maxNumber + 1}` : `${taskDefinition.task_name}_2`;
    } else {
      return taskDefinition.task_name;
    }
  }

  export default store;
