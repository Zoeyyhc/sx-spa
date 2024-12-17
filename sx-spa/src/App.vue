<script setup lang="ts">
import { RouterView } from 'vue-router'
import { darkTheme, NConfigProvider, NGlobalStyle, NMessageProvider } from 'naive-ui'
import MessageContent from './components/MessageContent.vue';
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <n-message-provider>
      <n-global-style />
      <MessageContent />
      <RouterView />
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped></style>