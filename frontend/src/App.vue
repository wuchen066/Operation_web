<template>
  <Suspense>
    <template #default>
      <Layout />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>

<script setup>
import Layout from './components/Layout.vue';
</script>