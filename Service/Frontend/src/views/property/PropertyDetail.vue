<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { pageParameters, currentUser, setStatusFlag } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataTableField, DataObject, OptionObject, FuncListItem } from '@/type'

const propertyKind = computed<string>(() => {
  return pageParameters['properties']?.['showKind']
})

const functionList = computed<FuncListItem[]>(() => {
  return [
    { text: '實收清單', icon: 'list-ul', goPath: `/properties/daily_list/${propertyKind.value}` },
  ]
})

const fieldInfo = computed<DataTableField[]>(() => {
  let resultFields: DataTableField[] = []

  switch (propertyKind.value) {
    case 'bank':
      resultFields = [
        { label: '交流時間', depValue: 'time_at', width: '10%' },
        { label: '遊戲暱稱', depValue: 'member_nickname', width: '7%' },
        { label: '種類', depValue: 'base_type', width: '6%' },
        { label: '金額', depValue: 'money', width: '7%' },
        { label: '跨行手續費', depValue: 'diff_bank_fee', width: '8%' },
        { label: '餘額', depValue: 'balance', width: '7%' },
        { label: '遊戲幣', depValue: 'game_coin', width: '7%' },
        { label: '遊戲類別', depValue: 'member_game_name', width: '7%' },
        { label: '編號', depValue: 'custom_no', width: '6%' },
        { label: '末五碼', depValue: 'last_five_code', width: '6%' },
        { label: '時間紀錄', depValue: 'record_time', width: '8%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '7%' },
        { label: '建立者', depValue: 'created_by', width: '6%' },
        { label: '操作', depValue: 'operate', width: '8%' },
      ]
      break

    case 'supermarket':
      resultFields = [
        { label: '交流時間', depValue: 'time_at', width: '10%' },
        { label: '遊戲暱稱', depValue: 'member_nickname', width: '9%' },
        { label: '繳費金額', depValue: 'money', width: '8%' },
        { label: '實收金額', depValue: 'real_in', width: '8%' },
        { label: '遊戲幣', depValue: 'game_coin', width: '9%' },
        { label: '遊戲類別', depValue: 'member_game_name', width: '9%' },
        { label: '編號', depValue: 'custom_no', width: '9%' },
        { label: '繳費代碼', depValue: 'pay_code', width: '9%' },
        { label: '門市', depValue: 'store', width: '6%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '9%' },
        { label: '建立者', depValue: 'created_by', width: '6%' },
        { label: '操作', depValue: 'operate', width: '8%' },
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
        { label: '虛擬帳戶', depValue: 'v_account', width: '7%' },
        { label: '庫存角色', depValue: 'stock_role_name', width: '9%' },
        { label: '建立者', depValue: 'created_by', width: '6%' },
        { label: '操作', depValue: 'operate', width: '6%' },
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

const awardOptions = ref<OptionObject[]>([
  { text: '頭獎', value: 'one' },
  { text: '二獎', value: 'two' },
  { text: '三獎', value: 'three' },
  { text: '未中獎', value: 'no' },
  { text: '隨機中獎', value: 'random' },
])
const lotteryTradeId = ref<string>('')
const lotteryTradeIndex = ref<number>(-1)
const targetAward = ref<string>('')
const currentLotteryUrl = ref<string>('')

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
      resultStr = currentTrade["player"][0]["name"]
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

const fieldClass = (field: string, trade: DataObject) => {
  let classes: string[] = []

  if ((field == 'money' && trade["details"]["money_correction"]) ||
      (field == 'game_coin' && trade["details"]["game_coin_correction"])) {
    classes.push("red-font")
  }

  return classes
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

const showLotteryModal = (index: number) => {
  if (trades.value[index]['lottery'].length == 0) {
    lotteryTradeId.value = trades.value[index]['id']
    lotteryTradeIndex.value = index
    setStatusFlag('modalShow', true)
  } else {
    let currentlotteryId = trades.value[index]['lottery'][0]['id']
    currentLotteryUrl.value = `${window.location.origin}/award?random=${currentlotteryId}`
    setStatusFlag('modalShow2', true)
  }
}

const createLottery = () => {
  let createInfo = {
    trade_id: lotteryTradeId.value,
    target_award: targetAward.value,
  }

  if (createInfo['target_award']) {
    callApi('post', '/apis/lotteries', createInfo)
      .then((resData: any) => {
        // 暫時塞一個空的, 讓畫面可以判斷成功建立抽獎遊戲
        trades.value[lotteryTradeIndex.value]['lottery'].push(resData)

        setStatusFlag('modalShow', false)
        showLotteryModal(lotteryTradeIndex.value)
      })
  }

}

const tradeComplete = (index: number): void => {
  let requestData: DataObject = {
    'completed_by': currentUser['shift'],
    'is_reset_time': true
  }

  callApi('patch', `/apis/trades/${trades.value[index]['id']}/complete`, requestData)
    .then((_) => {
      createNotify('question', `一筆交流紀錄已完成 !`)
      setStatusFlag('dataNeedUpdate', true)
    })
}

const tradeCheck = (index: number): void => {
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
      <div v-if="fieldName == 'money' || fieldName == 'game_coin'" :class="fieldClass(fieldName, trades[dataIndex])">
        {{ textTranstion(fieldName, dataIndex) }}
      </div>
      <div v-else-if="fieldName == 'operate' && hasData">
        <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goTradeEdit(dataIndex)" v-tooltip="'編輯交流'"></i>
        <template v-if="!trades[dataIndex]['completed_by']">
          <i class="bi-check-circle text-success fs-4 mx-2" role="button" @click="tradeComplete(dataIndex)" v-tooltip="'完成訂單'"></i>
        </template>
        <template v-else-if="!trades[dataIndex]['checked_by']">
          <i class="bi-check-circle text-success fs-4 mx-2" role="button" @click="tradeCheck(dataIndex)" v-tooltip="'檢查完成'"></i>
        </template>
        <i class="bi-ban text-danger fs-4 mx-2" role="button" @click="tradeCanel(dataIndex)" v-tooltip="'取消此筆'"></i>
        <i class="bi-controller text-warning fs-4 mx-2" role="button" @click="showLotteryModal(dataIndex)" v-tooltip="'抽獎遊戲'"></i>
      </div>
      <span v-else>{{ textTranstion(fieldName, dataIndex) }}</span>
    </template>
  </DataTable>
  <div class="d-flex justify-content-center">
    <button class="btn btn-secondary" @click="goPage('/properties')">返回列表</button>
  </div>

  <template v-if="propertyKind != 'bank'">
    <FunctionBall :functionList />
  </template>

  <Teleport to="#modal-header">
    <h3>抽獎遊戲設定</h3>
  </Teleport>
  <Teleport to="#modal-body">
    <div class="container">
      <h4 class="text-center my-4">請選擇中獎目標</h4>
      <CustomSelect type="select" :options="awardOptions" v-model:inputData="targetAward" />
      <div class="d-flex justify-content-center my-4">
        <button class="btn btn-primary mx-2" @click="createLottery()">建立抽獎</button>
      </div>
    </div>
  </Teleport>

  <Teleport to="#modal-header-2">
    <h3>抽獎遊戲網址</h3>
  </Teleport>
  <Teleport to="#modal-body-2">
    <div class="container">
      <h4 class="text-center my-4">{{ currentLotteryUrl }}</h4>
    </div>
  </Teleport>
</template>

<style lang="scss" scoped>
.red-font {
  color: red;
}
</style>
