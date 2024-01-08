// store/index.js
import { createStore } from 'vuex';
import VuexPersist from 'vuex-persist';

// await store.commit('setUser', user.value);
// await store.commit('setAuthDateTimestamp', Date.now());

const vuexPersist = new VuexPersist({
  key: 'neena', // The key to store the state on in the storage provider.
  storage: window.localStorage, // or window.sessionStorage or localForage
  // You can also specify the parts of the state you want to persist.
  reducer: state => ({
    auth: state.auth, // only persist the auth module
    // add other modules that you want to persist here
  })
});

// Create a new store instance.
const store = createStore({
  state() {
    return {
      auth: {
        token: null,
        user: null,
        authDateTimestamp: null
      },
      flowCreation: {
        request: null, // flow request
        drawflowEditor: null, // entire DrawFlow object
        flow: { // flow object
          taskOperations: [],
          dependencies: []
        }
      },
      taskDefinitions: [],
    };
  },
  getters: {
    token: state => state.auth.token,
    user: state => state.auth.user,
    taskDefinitions: state => state.taskDefinitions,
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
    getTaskOperationsThatThisTaskOperationDependsOn: (state) => (taskOperation) => {
      const dependencies = state.flowCreation.flow.dependencies;
      const taskOperations = state.flowCreation.flow.taskOperations;
      const dependencyIds = dependencies.filter(
        (dependency) => dependency.target_node_id === taskOperation.drawflow_node_id
      ).map((dependency) => dependency.source_node_id);
      return taskOperations.filter((operation) => dependencyIds.includes(operation.drawflow_node_id));
    },
    getTaskOperationsThatDependOnThisTaskOperation: (state) => (taskOperation) => {
      const dependencies = state.flowCreation.flow.dependencies;
      const taskOperations = state.flowCreation.flow.taskOperations;
      const dependencyIds = dependencies.filter(
        (dependency) => dependency.source_node_id === taskOperation.drawflow_node_id
      ).map((dependency) => dependency.target_node_id);
      return taskOperations.filter((operation) => dependencyIds.includes(operation.drawflow_node_id));
    },
    getDependencyBySourceAndTargetNodeId: (state) => (sourceNodeId, targetNodeId) => {
      const dependencies = state.flowCreation.flow.dependencies;
      const index = dependencies.findIndex(
        (dependency) => dependency.source_node_id === sourceNodeId && dependency.target_node_id === targetNodeId
      );
      return dependencies[index];
    }
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
        (operation) => operation.drawflow_node_id === taskOperation.drawflow_node_id
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

  },
  actions: {
    fetchTaskDefinitions: async ({ commit, state }) => {
      if (state.taskDefinitions.length === 0) {
        setTimeout(() => {
          const taskDefinitions = [
            { id: 1, output_type: 'Customer', name: 'Ask question', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Ask a question using Chat-GPT integration', source: 'chat-gpt' },
            { id: 2, output_type: 'Customer', name: 'Generate image', human_readable_id: 'generate-image-chat-gpt', yml_output: 'zeker boot ja', description: 'Create images based on specified parameters', source: 'chat-gpt' },
            { id: 3, output_type: 'Customer', name: 'Send Email', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Send an email to a specified list of recipients.', source: 'gmail' },
            { id: 4, output_type: 'Customer', name: 'Create Quote', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Generate a sales quote for a customer', source: 'salesforce' },
            { id: 5, output_type: 'Customer', name: 'Log New Lead', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Log a new sales lead in the CRM', source: 'salesforce' },
            { id: 6, output_type: 'Customer', name: 'Record Interaction', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Record a customer interaction in the system', source: 'salesforce' },
            { id: 7, output_type: 'Customer', name: 'Resolve Case', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Handle and resolve a customer support case', source: 'salesforce' },
            { id: 8, output_type: 'Customer', name: 'Renew Contract', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Initiate the process for contract renewal', source: 'salesforce' },
            { id: 9, output_type: 'Customer', name: 'Upload File', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Upload a file to a cloud storage service', source: 'google-drive' },
            { id: 10, output_type: 'Customer', name: 'Share Document', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Share a document from cloud storage with specified users', source: 'google-drive' },
            { id: 11, output_type: 'Customer', name: 'Create Folder', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Create a new folder in a cloud storage service', source: 'google-drive' },
            { id: 12, output_type: 'Customer', name: 'Delete File', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Delete a file from cloud storage', source: 'google-drive' },
            { id: 13, output_type: 'Customer', name: 'Rename File', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Change the name of a file in cloud storage', source: 'google-drive' },
            { id: 14, output_type: 'Customer', name: 'List Contacts', human_readable_id: 'ask-question-chat-gpt', yml_output: 'zeker boot ja', description: 'Retrieve a list of contacts from an email service', source: 'gmail' },
          ];
          commit('setTaskDefinitions', taskDefinitions);
        }, 100);
      }
    }
  },
  plugins: [vuexPersist.plugin]
});

export default store;