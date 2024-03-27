<template>
    <div class="root"></div>
</template>

<script setup>
import { onMounted} from 'vue';
import jsonview from "../../plugins/json-view/json-view.js";
const props = defineProps({
    jsonData: {
        type: Object,
        required: true
    }
});

onMounted(() => {
    const dataStr = JSON.stringify(props.jsonData);

    // Create the JSON tree object
    const tree = jsonview.create(dataStr);

    // Render the tree into the DOM element
    jsonview.render(tree, document.querySelector('.root'));

    // Optionally, expand the tree
    jsonview.expand(tree);
});
</script>

<style>
.json-container {
  font-family: monospace;
  line-height: 1.5;
  font-size: 14px;
  color: #2b6d91;
}

.line {
  padding: 2px 5px;
  &:hover {
    background-color: #f5f5f5;
  }
}

.json-key {
  color: #a52a2a;
}

.json-value {
  color: #2a8b2a;
}

.json-separator {
  margin: 0 5px;
  color: #333; 
}

.caret-icon i {
  cursor: pointer;
  color: #333;
  &:hover {
    color: #000;
  }
}
</style>