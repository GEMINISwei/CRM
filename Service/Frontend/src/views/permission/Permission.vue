<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { callApi } from '@/composables/api';

const onlineUsers = ref([])

onMounted(() => {
  callApi("get", "/apis/users/online")
    .then((resData: any) => {
      onlineUsers.value = resData.users
    })
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">權限管理</h3>
    <!-- <p class="m-4 text-center">待更新...</p> -->
     <h2 class="m-4 text-center">在線使用者</h2>
     <li class="text-center" v-for="username in onlineUsers">{{ username }}</li>
  </div>
</template>
