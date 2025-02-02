<script lang="ts" setup>
import { goPage } from '@/router'
</script>

<template>
  <div id="not-found-page-body">
    <h2>找不到此頁面</h2>
    <button class="btn btn-secondary" @click="goPage('/')">返回首頁</button>
  </div>
</template>

<style lang="scss" scoped>
#not-found-page-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
</style>
