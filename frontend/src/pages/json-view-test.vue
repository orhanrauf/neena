<template>
    <JSONViewCard :jsonData="myJsonData" :objectName="myObject"/>
  </template>
  
  <script setup>
  
  const myJsonData = {
    example: "This is some JSON data",
    number: 42,
    nested: { hello: "world" }
  };

  const myObject = 'MyObject';
  </script>