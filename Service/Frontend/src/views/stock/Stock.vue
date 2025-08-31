<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import DataCard from '@/components/DataCard.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataCardField, DataObject, OptionObject, FuncListItem } from '@/type'

// Member List Table Props Setting
const titleText: string = '庫存列表'
const fieldInfo: DataCardField[] = [
  { label: '角色名稱', depValue: 'role_name' },
  { label: '角色數量', depValue: 'balance' },
]
const apiUrl: string = '/apis/stocks'
const urlQuery = computed<DataObject>(() => {
  return {
    'game_id': selectedGame.value
  }
})
const stocks = ref([] as DataObject[])
const selectedGame = ref<string>('')
const gameOptions = ref<OptionObject[]>([])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增庫存角色', icon: 'plus-square', goPath: '/stocks/new' },
  { text: '選擇遊戲', icon: 'arrow-return-left', method: () => goSelectGame() },
]

onMounted(() => {
  getGameList()
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

const moneyFormat = (money: number): string => {
  let resultStr: string = ''

  resultStr = new Intl.NumberFormat('en-US').format(money)

  return resultStr
}

const goStockEdit = (index: number) => {
  goPage(`/stocks/edit`, {
    stockId: stocks.value[index]['id'],
  })
}
</script>

<template>
  <template v-if="selectedGame">
    <DataCard :titleText :fieldInfo :apiUrl :urlQuery v-model:tableData="stocks" :cardClick="goStockEdit">
      <template #tableCell="{ fieldName, dataIndex }">
        <span v-if="fieldName == 'balance'">
          {{ moneyFormat(stocks[dataIndex]?.[fieldName]) }}
        </span>
      </template>
    </DataCard>
  </template>
  <div v-else id="stock-page-select-body" class="container">
    <h3>庫存列表</h3>
    <h3>請選擇遊戲類別</h3>
    <div class="col-6 mt-2">
      <CustomSelect type="select" :options="gameOptions" v-model:inputData="selectedGame" />
    </div>
  </div>

  <FunctionBall :functionList />
</template>


<style lang="scss" scoped>
#stock-page-select-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
</style>
