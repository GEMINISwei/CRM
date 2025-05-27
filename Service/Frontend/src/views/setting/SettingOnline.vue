<script setup lang="ts">
import { onlineUsers } from '@/composables/websocket'
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">線上監控</h3>
    <div class="border rounded p-3">
      <h2 class="text-center">在線使用者</h2>
      <li class="text-center" v-for="username in onlineUsers">{{ username }}</li>
    </div>
  </div>
</template>
