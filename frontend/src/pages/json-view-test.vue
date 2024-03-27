<template>
    <JSONViewCard :jsonData="myJsonData" />
  </template>
  
  <script setup>
  
  const myJsonData = {
    example: "This is some JSON data",
    number: 42,
    nested: { hello: "world" }
  };
  </script>