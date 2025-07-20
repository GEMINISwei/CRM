<script setup lang="ts">
import { ref } from 'vue'
import { pageParameters } from '@/composables/globalUse'
import { goPage } from '@/router'
import DataTable from '@/components/DataTable.vue'
import type { DataTableField, DataObject } from '@/type'

const fieldInfo: DataTableField[] = [
  { label: '日期', depValue: '_id', width: '30%' },
  { label: '實收金額', depValue: 'daily_amount', width: '40%' },
  { label: '筆數', depValue: 'count', width: '30%' },
]

const titleText: string = `${pageParameters['properties']?.['showTitle']} - 每日實收清單`
const apiUrl: string = '/apis/properties/v_account_daily'
const urlQuery: DataObject = {
  'property_id': pageParameters['properties']?.['showId']
}
const containerSize: string = 'fluid'
const dailyList = ref<DataObject[]>([])

</script>

<template>
  <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize v-model:tableData="dailyList"></DataTable>

  <div class="d-flex justify-content-center">
    <button class="btn btn-secondary" @click="goPage('/properties')">返回列表</button>
  </div>
</template>
