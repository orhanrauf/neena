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
                request: null, // flow request
                drawflowEditor: null, // entire DrawFlow object
                flow: {
                    // flow object
                    taskOperations: [],
                    dependencies: [],
                },
            },
            taskDefinitions: [],
            integrations: [],
            flowRequests: [],
            integrations: [],
        };
    },
    getters: {
        token: (state) => state.auth.token,
        user: (state) => state.auth.user,
        taskDefinitions: (state) => state.taskDefinitions,
        // Getter to find a task operation by drawflow_node_id
        getTaskOperationByNodeId: (state) => (nodeId) => {
            // Assuming taskOperations is an array in state.flowCreation.flow
            const taskOperations = state.flowCreation.flow.taskOperations;

            // Find the task operation with the matching drawflow_node_id
            const taskOperation = taskOperations.find(
                (operation) => operation.drawflow_node_id === nodeId
            );

            return taskOperation || null; // Return the found operation or null if not found
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
                (dependency) => dependency.source_node_id === sourceNodeId
            );
        },
        getDependenciesByTargetNodeId: (state) => (targetNodeId) => {
            const dependencies = state.flowCreation.flow.dependencies;
            return dependencies.filter(
                (dependency) => dependency.target_node_id === targetNodeId
            );
        },
        getTaskOperationsThatThisTaskOperationDependsOn:
            (state) => (taskOperation) => {
                const dependencies = state.flowCreation.flow.dependencies;
                const taskOperations = state.flowCreation.flow.taskOperations;
                const dependencyIds = dependencies
                    .filter(
                        (dependency) =>
                            dependency.target_node_id ===
                            taskOperation.drawflow_node_id
                    )
                    .map((dependency) => dependency.source_node_id);
                return taskOperations.filter((operation) =>
                    dependencyIds.includes(operation.drawflow_node_id)
                );
            },
        getTaskOperationsThatDependOnThisTaskOperation:
            (state) => (taskOperation) => {
                const dependencies = state.flowCreation.flow.dependencies;
                const taskOperations = state.flowCreation.flow.taskOperations;
                const dependencyIds = dependencies
                    .filter(
                        (dependency) =>
                            dependency.source_node_id ===
                            taskOperation.drawflow_node_id
                    )
                    .map((dependency) => dependency.target_node_id);
                return taskOperations.filter((operation) =>
                    dependencyIds.includes(operation.drawflow_node_id)
                );
            },
        getDependencyBySourceAndTargetNodeId:
            (state) => (sourceNodeId, targetNodeId) => {
                const dependencies = state.flowCreation.flow.dependencies;
                const index = dependencies.findIndex(
                    (dependency) =>
                        dependency.source_node_id === sourceNodeId &&
                        dependency.target_node_id === targetNodeId
                );
                return dependencies[index];
            },
    },
    mutations: {
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
        setRequest(state, request) {
            state.flowCreation.request = request;
        },
        setDrawflowEditor(state, drawflowEditor) {
            state.flowCreation.drawflowEditor = drawflowEditor;
        },
        setTaskDefinitions(state, taskDefinitions) {
            state.taskDefinitions = taskDefinitions;
        },
        // Task operation mutations
        addTaskOperation(state, taskOperation) {
            state.flowCreation.flow.taskOperations.push(taskOperation);
        },
        editTaskOperation(state, taskOperation) {
            const taskOperations = state.flowCreation.flow.taskOperations;
            const index = taskOperations.findIndex(
                (operation) =>
                    operation.drawflow_node_id ===
                    taskOperation.drawflow_node_id
            );
            state.flowCreation.flow.taskOperations[index] = taskOperation;
        },
        deleteTaskOperation(state, drawflowNodeId) {
            const taskOperations = state.flowCreation.flow.taskOperations;
            const index = taskOperations.findIndex(
                (operation) => operation.drawflow_node_id === drawflowNodeId
            );
            state.flowCreation.flow.taskOperations.splice(index, 1);
        },
        // Dependency mutations
        addDependency(state, dependency) {
            console.log('Adding dependency', dependency);
            state.flowCreation.flow.dependencies.push(dependency);
        },
        deleteDependencyByTargetNodeId(state, targetNodeId) {
            const dependencies = state.flowCreation.flow.dependencies;
            const index = dependencies.findIndex(
                (dependency) => dependency.target_node_id === targetNodeId
            );
            state.flowCreation.flow.dependencies.splice(index, 1);
        },
        deleteDependencyBySourceNodeId(state, sourceNodeId) {
            const dependencies = state.flowCreation.flow.dependencies;
            const index = dependencies.findIndex(
                (dependency) => dependency.source_node_id === sourceNodeId
            );
            state.flowCreation.flow.dependencies.splice(index, 1);
        },
        setIntegrations(state, integrations) {
            state.integrations = integrations;
        },

        setFlowRequests(state, flowRequests) {
            state.flowRequests = flowRequests;
        },

    },
    actions: {
        fetchTaskDefinitions: async ({ commit, state }) => {
            if (state.taskDefinitions.length === 0) {
                const response = await http.get('/task_definitions/all');
                const taskDefinitions = response.data;
                commit('setTaskDefinitions', taskDefinitions);
            }
        },
        fetchIntegrations: async ({ commit, state }) => {
            if (state.integrations.length === 0) {
                const response = await http.get('/integrations/all');
                const integrations = response.data;
                console.log('Integrations', integrations);
                commit('setIntegrations', integrations);
            }
        },

        fetchFlowRequests: async ({ commit, state }) => {
            if (state.flowRequests.length === 0) {
                const response = await http.get('/flow_requests/all');
                const flowRequests = response.data;
                commit('setFlowRequests', flowRequests);
            }
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

    },
    plugins: [vuexPersist.plugin],
});

export default store;
