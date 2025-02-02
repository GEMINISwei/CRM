<script setup lang="ts">
import { statusFlag } from '@/composables/globalUse'
</script>

<template>
  <div v-show="statusFlag.loading" id="loading">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#loading {
  position: absolute;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  background-color: rgba($color: #000000, $alpha: 0.4);
}

.spinner-border {
  width: 4rem;
  height: 4rem;
}
</style>
