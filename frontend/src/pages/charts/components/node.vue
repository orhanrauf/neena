<template>
    <div class="command-card">
      <div class="header">
        <img class="icon" :src="iconSrc" alt="Integration Icon" />
        <h3 class="title">{{ title }}</h3>
      </div>
      <p class="description">{{ description }}</p>
      <div class="footer">
        <span class="output">{{ output }}</span>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  const props = defineProps({
    title: String,
    description: String,
    iconSrc: String,
    output: String
  });
  
  // Example usage, you would set these props based on the parent component
  const title = ref('Get customer by email');
  const description = ref('Looks up customer profile in Salesforce by email.');
  const iconSrc = ref('path-to-salesforce-icon.png'); // Replace with the path to your Salesforce icon
  const output = ref('Customer');
  </script>
  
  <style scoped>
  .command-card {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .header {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .icon {
    width: 24px;
    height: 24px;
    margin-right: 8px;
  }
  
  .title {
    margin: 0;
    color: #333;
    font-size: 1.2em;
  }
  
  .description {
    margin: 0;
    color: #666;
    font-size: 1em;
  }
  
  .footer {
    border-top: 1px solid #eee;
    padding-top: 8px;
    margin-top: 8px;
  }
  
  .output {
    display: inline-block;
    background-color: #f4f4f4;
    padding: 4px 8px;
    border-radius: 4px;
    color: #333;
    font-size: 0.9em;
  }
  </style>
  