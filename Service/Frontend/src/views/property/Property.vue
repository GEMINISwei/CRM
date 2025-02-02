<script setup lang="ts">
import { ref } from 'vue'
import { goPage } from '@/router';
import DataCard from '@/components/DataCard.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataCardField, DataObject, FuncListItem } from '@/type'

// Member List Table Props Setting
const titleText: string = '資產列表'
const fieldInfo: DataCardField[] = [
  { label: '銀行名稱', depValue: 'name' },
  { label: '帳號', depValue: 'account' },
  { label: '當日餘額', depValue: 'today_balance' },
  { label: '當日筆數', depValue: 'day_trade_count' },
  { label: '當月筆數', depValue: 'month_trade_count' },
  { label: '總餘額', depValue: 'balance' },
  { label: '總筆數', depValue: 'trade_count' },
]
const apiUrl: string = '/apis/properties'
const assets = ref([] as DataObject[])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增資產', icon: 'plus-square', goPath: '/properties/new' },
]

const goAssetDetail = (index: number) => {
  goPage('/properties/details', {
    showTitle: assets.value[index]['name'],
    showKind: assets.value[index]['kind'],
    showId: assets.value[index]['id']
  })
}

const moneyFormat = (money: number): string => {
  let resultStr: string = ''

  resultStr = new Intl.NumberFormat('en-US').format(money)

  return resultStr
}
</script>

<template>
  <div>
    <DataCard :titleText :fieldInfo :apiUrl v-model:tableData="assets" :cardClick="goAssetDetail">
      <template #tableCell="{ fieldName, dataIndex }">
        <span v-if="fieldName == 'balance'">
          {{ moneyFormat(assets[dataIndex]?.[fieldName]) }}
        </span>
      </template>
    </DataCard>

  </div>

  <FunctionBall :functionList />
</template>
