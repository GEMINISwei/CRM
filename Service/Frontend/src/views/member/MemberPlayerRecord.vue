<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataTableField, DataObject, FuncListItem } from '@/type'

const fieldInfo: DataTableField[] = [
  { label: '日期', depValue: '_id', width: '20%' },
  { label: '入金額度', depValue: 'daily_in', width: '40%' },
  { label: '出金額度', depValue: 'daily_out', width: '40%' },
]
const apiUrl: string = '/apis/trades/player_records'
const urlQuery = computed<DataObject>(() => {
  return {
    'player_id': pageParameters.members.playerId
  }
})
const containerSize: string = 'fluid'
const records = ref([] as DataObject[])

const titleText = computed<string>(() => {
  return `${pageParameters.members.playerName} (出入金列表)`
})
// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '返回', icon: 'arrow-return-left', method: () => goBackPage() },
]

onMounted(() => {
  if (pageParameters.members.playerId) {
    //
  } else {
    goPage('/members')
  }
})

const goBackPage = (): void => {
  goPage('/members')
}
</script>

<template>
  <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize :dataCount="9" v-model:tableData="records" />
  <FunctionBall :functionList />
</template>
