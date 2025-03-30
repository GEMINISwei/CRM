<script setup lang="ts">
import { reactive } from 'vue'
import { callApi } from '@/composables/api'
import type { DataObject } from '@/type'

const SampleBtns = reactive<DataObject[]>([
  { color: "success", text: "報表範例", method: () => downloadExcel("download-excel", "基本報表") },
  // { color: "success", text: "媒合範例", method: () => downloadExcel("download-excel", "媒合報表") },
])

const downloadExcel = (reportName: string, downloadName: string) => {
  callApi('get', `/apis/reports/${reportName}`, {}, true)
    .then((resBlob: any) => {
      const url = window.URL.createObjectURL(resBlob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${downloadName}.xlsx`); // 自訂下載檔案名稱
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url); // 清除 URL 資源
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">報表功能</h3>
    <div class="border rounded p-3">
      <h4 class="text-center">範例下載</h4>
      <hr>
      <button
        v-for="(btn, btnIndex) in SampleBtns"
        :key="btnIndex"
        :class="`btn btn-${btn.color} mx-4`"
        type="button"
        @click="btn.method()"
      >
        {{ btn.text }}
      </button>
    </div>
    <div class="border rounded mt-3 p-3">
      <h4 class="text-center">XX 報表</h4>
      <hr>
    </div>
    <div class="border rounded mt-3 p-3">
      <h4 class="text-center">OO 報表</h4>
      <hr>
    </div>
  </div>
</template>
