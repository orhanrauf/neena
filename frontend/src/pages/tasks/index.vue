<script setup lang="ts">
const data = [
  {
    id: 1,
    name: "lookup acc number_by_email",
    parameters:
      "<span>acc_number:</span> <span class='text-success'>string</span>",
    description: "Looks up a customers account number basde on taire email",
  },
  {
    id: 2,
    name: "lookup acc number_by - email",
    parameters: "int: acc number <br/>str: details",
    description: "Looks up a customers account number basde on taire email",
  },
  {
    id: 3,
    name: "",
    parameters: "",
    description: "",
  },
];
</script>

<template>
  <VTable class="bg-transparent">
    <thead>
      <tr class="text-left font-weight-black">
        <th>NAME</th>
        <th>PARAMETERS</th>
        <th>DESCRIPTION</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in data" :key="item.id">
        <td class="py-8" v-html="item.name"></td>
        <td class="py-8" v-html="item.parameters"></td>
        <td class="py-8" v-html="item.description"></td>
      </tr>
    </tbody>
  </VTable>
</template>

<style scoped>
.v-table .v-table__wrapper > table > thead > tr > th:not(:last-child) {
  border-right: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.v-table .v-table__wrapper > table > tbody > tr > td:not(:last-child),
.v-table .v-table__wrapper > table > tbody > tr > th:not(:last-child) {
  border-right: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
