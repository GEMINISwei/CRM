<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { pageParameters, currentUser, setStatusFlag } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import type { DataTableField, DataObject } from '@/type'

const fieldInfo = computed<DataTableField[]>(() => {
  let resultFields: DataTableField[] = []

  switch (pageParameters['properties']?.['showKind']) {
    case 'bank':
      resultFields = [
        { label: '交流時間', depValue: 'time_at', width: '10%' },
        { label: '遊戲暱稱', depValue: 'member_nickname', width: '7%' },
        { label: '種類', depValue: 'base_type', width: '6%' },
        { label: '金額', depValue: 'money', width: '7%' },
        { label: '跨行手續費', depValue: 'diff_bank_fee', width: '10%' },
        { label: '餘額', depValue: 'balance', width: '7%' },
        { label: '遊戲幣', depValue: 'game_coin', width: '7%' },
        { label: '遊戲類別', depValue: 'member_game_name', width: '7%' },
        { label: '編號', depValue: 'custom_no', width: '6%' },
        { label: '末五碼', depValue: 'last_five_code', width: '6%' },
        { label: '時間紀錄', depValue: 'record_time', width: '10%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '7%' },
        { label: '操作', depValue: 'operate', width: '10%' },
      ]
      break

    case 'supermarket':
      resultFields = [
        { label: '交流時間', depValue: 'time_at', width: '10%' },
        { label: '遊戲暱稱', depValue: 'member_nickname', width: '9%' },
        { label: '繳費金額', depValue: 'money', width: '9%' },
        { label: '實收金額', depValue: 'real_in', width: '9%' },
        { label: '遊戲幣', depValue: 'game_coin', width: '9%' },
        { label: '遊戲類別', depValue: 'member_game_name', width: '9%' },
        { label: '編號', depValue: 'custom_no', width: '9%' },
        { label: '繳費代碼', depValue: 'pay_code', width: '9%' },
        { label: '門市', depValue: 'store', width: '8%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '9%' },
        { label: '操作', depValue: 'operate', width: '10%' },
      ]
      break

    case 'v_account':
      resultFields = [
        { label: '交流時間', depValue: 'time_at', width: '9%' },
        { label: '遊戲暱稱', depValue: 'member_nickname', width: '9%' },
        { label: '繳費金額', depValue: 'money', width: '9%' },
        { label: '實收金額', depValue: 'real_in', width: '9%' },
        { label: '遊戲幣', depValue: 'game_coin', width: '9%' },
        { label: '遊戲類別', depValue: 'member_game_name', width: '9%' },
        { label: '編號', depValue: 'custom_no', width: '9%' },
        { label: '末五碼', depValue: 'last_five_code', width: '9%' },
        { label: '虛擬帳戶', depValue: 'v_account', width: '9%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '9%' },
        { label: '操作', depValue: 'operate', width: '10%' },
      ]
      break
  }

  return resultFields
})


const apiUrl: string = '/apis/trades'
const titleText: string = `${pageParameters['properties']?.['showTitle']} - 交流紀錄`
const urlQuery: DataObject = {
  'property_id': pageParameters['properties']?.['showId']
}
const containerSize: string = 'fluid'
const trades = ref<DataObject[]>([])
const colorInfo = reactive<DataObject>({
  'admin': '#ffffff',
  'day_class': '#ffffff',
  'night_class': '#ffffff',
})

const textTranstion = (field: string, index: number): string => {
  let currentTrade = trades.value[index]
  let resultStr = ""

  switch (field)
  {
    case "time_at":
      resultStr = currentTrade[field].slice(0, 10)
      break

    case 'base_type':
      if (currentTrade[field] == 'money_in') {
        resultStr = "入金"
      } else if (currentTrade[field] == 'money_out') {
        resultStr = "出金"
      }
      break

    case "member_nickname":
      resultStr = currentTrade["member"][0]["nickname"]
      break

    case "stock_role_name":
      resultStr = currentTrade["stock"][0]["role_name"]
      break

    case "member_game_name":
      resultStr = currentTrade["member"][0]["game"][0]["name"]
      break

    case "custom_no":
      resultStr = currentTrade["details"][field]
      break

    case "last_five_code":
      resultStr = currentTrade["details"][field]
      break

    case "record_time":
      resultStr = currentTrade["details"][field]
      break

    case "pay_code":
      resultStr = currentTrade["details"][field]
      break

    case "store":
      resultStr = currentTrade["details"][field]
      break

    case "diff_bank_fee":
      resultStr = currentTrade["details"][field]
      break

    default:
      resultStr = currentTrade[field]
  }

  return resultStr ? resultStr : "-"
}

const goTradeEdit = (index: number) => {
  goPage('/trades/edit', {
    editId: trades.value[index]['id'],
    showKind: pageParameters['properties']?.['showKind'],
    propertyName: pageParameters['properties']?.['showTitle'],
    propertyId: pageParameters['properties']?.['showId'],
    basyType: trades.value[index]['base_type'],
  })
}

const tradeCanel = (index: number) => {
  callApi('delete', `/apis/trades/${trades.value[index]['id']}`)
    .then((_) => {
      createNotify('question', `一筆交流紀錄已取消 !`)
      setStatusFlag('dataNeedUpdate', true)
    })
}

const tradeCheckFinish = (index: number): void => {
  let requestData: DataObject = {
    'checked_by': currentUser['shift']
  }

  callApi('patch', `/apis/trades/${trades.value[index]['id']}/check`, requestData)
    .then((_) => {
      createNotify('question', `一筆交流紀錄已檢查 !`)
      setStatusFlag('dataNeedUpdate', true)
    })
}

const getColorInfo = () => {
  callApi('get', '/apis/settings/trade/color')
    .then((resData: any) => {
      Object.keys(colorInfo).forEach((key: string) => {
        colorInfo[key] = resData['value'][key]
      })
    })
}

watch(trades, (newVal) => {
  newVal.forEach((trade: DataObject) => {
    trade.customStyle = `background: ${colorInfo[trade['checked_by']]};`
  })
})

onMounted(() => {
  if (pageParameters['properties'] === undefined) {
    goPage('/properties')
  }

  getColorInfo()
})
</script>

<template>
  <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize v-model:tableData="trades">
    <template #tableCell="{ fieldName, dataIndex, hasData }">
      <div v-if="fieldName == 'operate' && hasData">
        <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goTradeEdit(dataIndex)" v-tooltip="'編輯交流'"></i>
        <template v-if="!trades[dataIndex]['checked_by']">
          <i class="bi-check-circle text-success fs-4 mx-2" role="button" @click="tradeCheckFinish(dataIndex)" v-tooltip="'檢查完成'"></i>
        </template>
        <i class="bi-ban text-danger fs-4 mx-2" role="button" @click="tradeCanel(dataIndex)" v-tooltip="'取消此筆'"></i>
      </div>
      <span v-else>{{ textTranstion(fieldName, dataIndex) }}</span>
    </template>
  </DataTable>
  <div class="d-flex justify-content-center">
    <button class="btn btn-secondary" @click="goPage('/properties')">返回列表</button>
  </div>
</template>
