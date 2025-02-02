<script setup lang="ts">
import { ref } from 'vue'
import DataCard from '@/components/DataCard.vue'
import type { DataCardField, DataObject } from '@/type'

// Member List Table Props Setting
const titleText: string = '媒合紀錄'
const fieldInfo: DataCardField[] = [
  { label: '媒合單號', depValue: 'order_number' },
  { label: '媒合金額', depValue: 'money' },
  { label: '交流單號 (出金)', depValue: 'buy_trade_id' },
  { label: '交流單號 (入金)', depValue: 'sell_trade_ids' },
]
const apiUrl: string = '/apis/matches'
const matches = ref([] as DataObject[])

const moneyFormat = (money: number): string => {
  let resultStr: string = ''

  resultStr = new Intl.NumberFormat('en-US').format(money)

  return resultStr
}
</script>

<template>
  <div>
    <DataCard :titleText :fieldInfo :apiUrl v-model:tableData="matches">
      <template #tableCell="{ fieldName, dataIndex }">
        <span v-if="fieldName == 'money'">
          {{ moneyFormat(matches[dataIndex]?.["money"]) }} / {{ moneyFormat(matches[dataIndex]?.["total_money"]) }}
        </span>
      </template>
    </DataCard>
  </div>
</template>
