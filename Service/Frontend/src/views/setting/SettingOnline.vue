<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { goPage } from '@/router'
import { onlineUsers } from '@/composables/websocket'
import { setStatusFlag } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import CustomInput from '@/components/CustomInput.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import { DataObject, DataTableField, FuncListItem } from '@/type'

const selectDate = ref<string>("")
const loginRecords = ref<DataObject[]>([])
const titleText = "線上監控"
const apiUrl = '/apis/login_records'
const containerSize: string = 'fluid'
const fieldInfo: DataTableField[] = [
  { label: '使用者', depValue: 'nickname', width: '40%' },
  { label: '登入時間', depValue: 'login_time', width: '60%' },
]
const urlQuery = computed<DataObject>(() => {
  return {
    'search_time': selectDate.value,
  }
})
const functionList: FuncListItem[] = [
  { text: '返回設定', icon: 'arrow-return-left', method: () => goToSetting() },
]

const setCurrentDate = () => {
  let now = new Date()
  let year = now.getFullYear()
  let month = String(now.getMonth() + 1).padStart(2, '0')
  let date = String(now.getDate()).padStart(2, '0')

  selectDate.value = `${year}-${month}-${date}`
}

const goToSetting = (): void => {
  goPage('/settings')
}

watch(selectDate, () => {
  setStatusFlag('dataNeedUpdate', true)
})

onMounted(() => {
  setCurrentDate()
})
</script>

<template>
  <div class="container">
    <div class="border rounded p-3 my-4">
      <h2 class="text-center">在線使用者</h2>
      <span class="text-center" v-for="username in onlineUsers">{{ username }}</span>
    </div>

    <template v-if="selectDate">
      <CustomInput type="date" v-model:inputData="selectDate" />
      <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize v-model:tableData="loginRecords">
        <template #tableCell="{ fieldName, dataIndex }">
          <div v-if="fieldName == 'login_time'">
            {{ loginRecords[dataIndex]['login_time'].slice(11, 19) }}
          </div>
        </template>
      </DataTable>
    </template>
  </div>

  <FunctionBall :functionList />
</template>
