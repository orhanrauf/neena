<template>
  <div class="template-card">
    <div class="icons-container">
      <div class="icon-background">
        <!-- Use image1 prop for the first image source -->
        <img class="icon" :src="image1" alt="Icon 1" />
      </div>
      <div class="icon-background">
        <!-- Use image2 prop for the second image source -->
        <img class="icon" :src="image2" alt="Icon 2" />
      </div>
    </div>

    <!-- Use title prop for the card text -->
    <p class="card-text">{{ title }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  image1: String,
  image2: String,
  title: String,
  // Add more image props as needed
});

</script>

<style scoped>
.template-card {
  border: 1.6px solid #a9a9a9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: left;
  background-color: #fff;
  width: 300px; /* Adjust width as needed */
  transition: border 0.3s, background-color 0.3s; /* Smooth transition for hover and active */
}

.template-card:hover {
  background-color: #e0e0e0; /* Light gray background on hover */
  border: 1.5px solid #606060; /* Thicker border on hover */
  cursor: pointer;
}

.template-card:active {
  background-color: #e0e0e0; /* Slightly darker background when clicked */
  border: 1.5px solid #818080; /* Even thicker border when clicked */
}

.icon {
  width: 30px;
  height: 30px;
}

.icons-container {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  margin-bottom: 14px;
}

.icon-background {
  background: rgba(40, 199, 111, 0.08);
  display: flex;
  justify-content: center;
  height: 45px;
  width: 45px;
  align-items: center;
  border-radius: 6px;
}

.card-text {
  text-align: left;
  color: #706e6e;
  font-size: 16px;
  font-weight: 500;
  align-items: left;
  /* Add other font styling as necessary */
}
</style>
