<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { callApi } from '@/composables/api'
import { pageParameters, setPageParams } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import { DataObject, DataTableField, OptionObject, FuncListItem } from '@/type'

const performances = ref<DataObject[]>([])
const titleText = "員工業績列表"
const apiUrl = '/apis/users/trade_performance'
const containerSize: string = 'fluid'
const fieldInfo: DataTableField[] = [
  { label: '日期', depValue: 'date', width: '10%' },
  { label: '員工', depValue: 'staff', width: '10%' },
  { label: '入金', depValue: 'daily_in_money', width: '10%' },
  { label: '出金', depValue: 'daily_out_money', width: '10%' },
  { label: '總入幣', depValue: 'daily_in_coin', width: '10%' },
  { label: '總出幣', depValue: 'daily_out_coin', width: '10%' },
  { label: '手續幣', depValue: 'money_fee', width: '10%' },
  { label: '免手續幣 (總額)', depValue: 'no_charge_coin', width: '15%' },
  { label: '活動幣 (總量)', depValue: 'activity_coin', width: '15%' },
]
const urlQuery = computed<DataObject>(() => {
  return {
    'game_id': selectedGame.value
  }
})

const selectedGame = ref<string>('')
const gameOptions = ref<OptionObject[]>([])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '選擇遊戲', icon: 'arrow-return-left', method: () => goSelectGame() },
]

const textTranstion = (field: string, index: number): string => {
  let resultStr = ''
  let currentData = performances.value[index]

  if (field == 'staff') {
    resultStr = currentData['_id'].split('_x_')[0]
  } else if (field == 'date') {
    resultStr = currentData['_id'].split('_x_')[1]
  }

  return resultStr
}

watch(selectedGame, (newVal: string) => {
  setPageParams('staffs', {
    'gameId': newVal
  })
})

const getGameList = (): void => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      gameOptions.value = resData.list_data.map((x: any) => {
        return {
          text: x['name'],
          value: x['id'],
        }
      })
    })
}

const goSelectGame = (): void => {
  selectedGame.value = ''
}

onMounted(() => {
  getGameList()

  selectedGame.value = pageParameters.members?.gameId
})


</script>

<template>
  <template v-if="selectedGame">
    <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize v-model:tableData="performances">
      <template #tableCell="{ fieldName, dataIndex }">
        <div v-if="fieldName == 'date' || fieldName == 'staff'">
          {{ textTranstion(fieldName, dataIndex) }}
        </div>
      </template>
    </DataTable>
    <FunctionBall :functionList />
  </template>
  <div v-else id="staff-page-select-body" class="container">
    <h3>{{ titleText }}</h3>
    <h3>請選擇遊戲類別</h3>
    <div class="col-6 mt-2">
      <CustomSelect type="select" :options="gameOptions" v-model:inputData="selectedGame" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#staff-page-select-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
</style>
