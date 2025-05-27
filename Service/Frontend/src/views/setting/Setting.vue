<script lang="ts" setup>
import { reactive } from 'vue'
import { goPage } from '@/router'
import type { DataObject } from '@/type'

const systemSettings = reactive<DataObject[]>([
  { title: '交流方式', method: () => goPage('/settings/communicate_way') },
  { title: '手續費', method: () => goPage('/settings/fee') },
  { title: '代表顏色', method: () => goPage('/settings/color') },
  { title: '使用權限', method: () => goPage('/settings/permission') },
  { title: '遊戲設定', method: () => goPage('/settings/award') },
])
const monitorCheck = reactive<DataObject[]>([
  { title: '線上監控', method: () => goPage('/settings/online') },
])

</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">系統設定</h3>
    <div
      v-for="(sVal, sIdx) in systemSettings"
      :key="sIdx"
      class="border rounded my-3 p-3 d-flex flex-row justify-content-center"
    >
      <div class="w-50 px-5 d-flex">
        <span class="align-self-center">{{ sVal.title }}</span>
      </div>
      <div class="w-50 mx-3 d-flex flex-row justify-content-end">
        <button class="btn btn-primary" @click="sVal.method">前往設定</button>
      </div>
    </div>

    <h3 class="m-4 text-center">監控狀態</h3>
    <div
      v-for="(sVal, sIdx) in monitorCheck"
      :key="sIdx"
      class="border rounded my-3 p-3 d-flex flex-row justify-content-center"
    >
      <div class="w-50 px-5 d-flex">
        <span class="align-self-center">{{ sVal.title }}</span>
      </div>
      <div class="w-50 mx-3 d-flex flex-row justify-content-end">
        <button class="btn btn-primary" @click="sVal.method">前往確認</button>
      </div>
    </div>
  </div>
</template>
