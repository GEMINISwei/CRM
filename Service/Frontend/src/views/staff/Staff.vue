<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { pageParameters, setPageParams, setStatusFlag } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import CustomInput from '@/components/CustomInput.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import { DataObject, DataTableField, OptionObject, FuncListItem } from '@/type'

const showMode = ref<string>('date')
const dateOrMonth = ref<string>('')
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
    'game_id': selectedGame.value,
    'search_time': dateOrMonth.value,
  }
})
const finalTitle = computed<string>(() => {
  return `${titleText} (${showMode.value == 'date' ? '當日' : '當月'})`
})

const selectedGame = ref<string>('')
const gameOptions = ref<OptionObject[]>([])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '切換模式', icon: 'filter-circle', method: () => changeShowMode() },
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
  setCurrentDate()
  setPageParams('staffs', {
    'gameId': newVal
  })
})

watch(dateOrMonth, (newVal: string) => {
  let month = Number(newVal.split('-')[1])

  if (month >= 1 && month <= 12) {
    setStatusFlag('dataNeedUpdate', true)
  } else {
    createNotify("error", "月份異常 !")
  }
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

const setCurrentDate = () => {
  let now = new Date()
  let year = now.getFullYear()
  let month = String(now.getMonth() + 1).padStart(2, '0')
  let date = String(now.getDate())

  dateOrMonth.value = `${year}-${month}-${date}`
}

const setCurrentMonth = () => {
  let now = new Date()
  let year = now.getFullYear()
  let month = String(now.getMonth() + 1).padStart(2, '0')

  dateOrMonth.value = `${year}-${month}`
}

const changeShowMode = (): void => {
  if (showMode.value == 'date') {
    setCurrentMonth()
    showMode.value = 'month'

  } else if (showMode.value == 'month') {
    setCurrentDate()
    showMode.value = 'date'
  }
}

onMounted(() => {
  getGameList()

  selectedGame.value = pageParameters.members?.gameId
})
</script>

<template>
  <template v-if="selectedGame">
    <CustomInput v-if="showMode == 'date'" type="date" v-model:inputData="dateOrMonth" />
    <CustomInput v-else type="month" v-model:inputData="dateOrMonth" />

    <DataTable :titleText="finalTitle" :fieldInfo :apiUrl :urlQuery :containerSize v-model:tableData="performances">
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
