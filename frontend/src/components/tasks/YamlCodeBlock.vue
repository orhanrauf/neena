<script setup lang="ts">
import { computed } from "vue";
import hljs from "highlight.js/lib/core";
import yaml from "highlight.js/lib/languages/yaml";
import "highlight.js/styles/stackoverflow-light.css";

hljs.registerLanguage("yaml", yaml);

const props = defineProps<{
  code: string;
}>();

const highlightedCode = computed((): string => {
  const result = hljs.highlight(props.code, {
    language: "yaml",
    ignoreIllegals: false,
  });
  return result.value;
});
</script>

<template>
  <pre><code v-html="highlightedCode" :tabindex="0" class="hljs yaml"></code></pre>
</template>