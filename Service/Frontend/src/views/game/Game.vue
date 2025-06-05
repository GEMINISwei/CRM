<script setup lang="ts">
import { ref } from 'vue'
import { goPage } from '@/router'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataObject, DataTableField, FuncListItem } from '@/type'

const titleText: string = '遊戲列表'
const fieldInfo: DataTableField[] = [
  { label: '遊戲名稱', depValue: 'name', width: '15%' },
  { label: '入金 - 遊戲幣匯率', depValue: 'money_in_exchange', width: '20%' },
  { label: '出金 - 遊戲幣匯率', depValue: 'money_out_exchange', width: '20%' },
  { label: '超商手續費', depValue: 'charge_fee', width: '10%' },
  { label: '遊戲幣手續費', depValue: 'game_coin_fee', width: '20%' },
  { label: '操作', depValue: 'operate', width: '15%' },
]
const apiUrl: string = '/apis/games'
const games = ref<DataObject[]>([])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增遊戲類別', icon: 'plus-square', goPath: '/games/new' },
]

const goGameEdit = (index: number) => {
  goPage('/games/edit', {
    editId: games.value[index]['id']
  })
}
</script>

<template>
  <div class="container">
    <DataTable :titleText :fieldInfo :apiUrl v-model:tableData="games">
      <template #tableCell="{ fieldName, hasData, dataIndex }">
        <div v-if="fieldName == 'operate' && hasData">
          <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goGameEdit(dataIndex)" v-tooltip="'編輯會員'"></i>
        </div>
      </template>
    </DataTable>
    <FunctionBall :functionList />
  </div>
</template>
