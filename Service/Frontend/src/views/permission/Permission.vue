<script setup lang="ts">
import { onMounted } from 'vue'
import { onlineUsers } from '@/composables/websocket'

onMounted(() => {
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">權限管理</h3>
     <h2 class="m-4 text-center">在線使用者</h2>
     <li class="text-center" v-for="username in onlineUsers">{{ username }}</li>
  </div>
</template>
