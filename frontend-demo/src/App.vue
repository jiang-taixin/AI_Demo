<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>

  <a-config-provider
      :theme="{
      token: {
        colorPrimary: '#2c3e50',
        borderRadius: 5
      },
    }"
  >
    <RouterView />
  </a-config-provider>
</template>

<style scoped>

</style>
