<script setup lang="ts">
import { computed } from "vue";
import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
import "highlight.js/styles/stackoverflow-light.css";

hljs.registerLanguage("python", python);

const props = defineProps<{
  code: string;
}>();

const highlightedCode = computed((): string => {
  const result = hljs.highlight(props.code, {
    language: "python",
    ignoreIllegals: false,
  });
  return result.value;
});
</script>

<template>
  <pre><code v-html="highlightedCode" :tabindex="0" class="hljs python"></code></pre>
</template>
