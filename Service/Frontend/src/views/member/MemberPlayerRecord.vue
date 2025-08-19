<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { goPage } from '@/router'
import { pageParameters, setStatusFlag } from '@/composables/globalUse'
import CustomInput from '@/components/CustomInput.vue'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataTableField, DataObject, FuncListItem } from '@/type'

const showYear = ref<string>('')

const fieldInfo: DataTableField[] = [
  { label: '年月', depValue: '_id', width: '20%' },
  { label: '入金額度', depValue: 'daily_in', width: '40%' },
  { label: '出金額度', depValue: 'daily_out', width: '40%' },
]
const apiUrl: string = '/apis/trades/member_records'
const urlQuery = computed<DataObject>(() => {
  return {
    'member_id': pageParameters.members.memberId,
    'search_time': showYear.value
  }
})
const containerSize: string = 'fluid'
const records = ref([] as DataObject[])

const titleText = computed<string>(() => {
  return `${pageParameters.members.memberName} (出入金列表)`
})
// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '返回', icon: 'arrow-return-left', method: () => goBackPage() },
]

const goBackPage = (): void => {
  goPage('/members')
}

const setCurrentMonth = () => {
  let now = new Date()
  let year = now.getFullYear()

  showYear.value = `${year}`
}

onBeforeMount(() => {
  setCurrentMonth()
})

watch(showYear, (newVal: string) => {
  if (newVal.length == 4) {
    setStatusFlag('dataNeedUpdate', true)
  }
})
</script>

<template>
  <CustomInput type="text" v-model:inputData="showYear" />
  <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize :dataCount="9" v-model:tableData="records" />
  <FunctionBall :functionList />
</template>
