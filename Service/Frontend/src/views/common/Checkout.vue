<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { currentUser, pageParameters } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { DataObject, DataTableField } from '@/type'

const checkoutData = ref<DataObject>({})
const containerSize: string = 'fluid'

const fieldInfo: DataTableField[] = [
  { label: '資產名稱', depValue: 'name', width: '40%' },
  { label: '資產餘額', depValue: 'balance', width: '60%' },
]

const propertyData = computed<DataObject[]>(() => {
  return checkoutData.value['property'] ? checkoutData.value['property']['list_data'] : []
})
const gameStockAllData = computed<DataObject[]>(() => {
  return checkoutData.value['game_stock_all']?.['list_data']
})
const gameStockData = computed<DataObject[]>(() => {
  return checkoutData.value['game_stock']?.['list_data']
})

const showMode = computed<string>(() => {
  return pageParameters['checkout']?.mode
})

const calcFinalData = computed<any[]>(() => {
  return gameStockData.value.map((x: any) => {
    return [
      Object.entries({
        'game_coin_in': calcArraySum(x['stock'].map((x: any) => x.game_coin_in)),
        'money_out': calcArraySum(x['stock'].map((x: any) => x.money_out)),
        'game_coin_out': calcArraySum(x['stock'].map((x: any) => x.game_coin_out)),
        'activity_coin': calcArraySum(x['stock'].map((x: any) => x.activity_coin)),
        'game_coin_fee_out': calcArraySum(x['stock'].map((x: any) => x.game_coin_fee_out)),
        'game_coin_out_total': calcArraySum(x['stock'].map((x: any) => x.game_coin_out_total)),
        'money_in': calcArraySum(x['stock'].map((x: any) => x.money_in)),
      }).map((x: any) => {
        return {
          "title": x[0],
          "value": x[1],
        }
      }),
      // Object.entries({
      //   'game_coin_out': calcArraySum(x['stock'].map((x: any) => x.game_coin_out)),
      //   'activity_coin': calcArraySum(x['stock'].map((x: any) => x.activity_coin)),
      //   'game_coin_fee_out': calcArraySum(x['stock'].map((x: any) => x.game_coin_fee_out)),
      //   'game_coin_out_total': calcArraySum(x['stock'].map((x: any) => x.game_coin_out_total)),
      // }).map((x: any) => {
      //   return {
      //     "title": x[0],
      //     "value": x[1],
      //   }
      // }),
      // Object.entries({
      //   'money_in': calcArraySum(x['stock'].map((x: any) => x.money_in)),
      // }).map((x: any) => {
      //   return {
      //     "title": x[0],
      //     "value": x[1],
      //   }
      // })
    ]
  })
})

const titleTransform = (oriStr: string): string => {
  let resultStr = ''

  switch (oriStr) {
    case 'game_coin_in':
      resultStr = '轉入幣總'
      break

    case 'money_out':
      resultStr = '轉出現金'
      break

    case 'game_coin_out':
      resultStr = '轉出幣總'
      break

    case 'activity_coin':
      resultStr = '活動幣'
      break

    case 'game_coin_fee_out':
      resultStr = '官方手續費'
      break

    case 'game_coin_out_total':
      resultStr = '轉出幣合計'
      break

    case 'money_in':
      resultStr = '※ 當班營業額'
      break
  }

  return resultStr
}

const allGameStockfieldInfo: DataTableField[] = [
  { label: '庫存名稱', depValue: 'role_name', width: '40%' },
  { label: '幣總數', depValue: 'balance', width: '60%' },
]
const calcFinalfieldInfo: DataTableField[] = [
  { label: '敘述', depValue: 'title', width: '40%' },
  { label: '數值', depValue: 'value', width: '60%' },
]

const checkoutTrade = (): void => {
  let queryUrl = `username=${currentUser.username}&mode=${showMode.value}`

  callApi("get", `/apis/users/trade_checkout?${queryUrl}`)
    .then((resData: any) => {
      checkoutData.value = resData
    })
}

const calcArraySum = (arrayData: number[]): number => {
  return arrayData.reduce((accu: number, curr: number) => accu + curr, 0)
}

const copyCheckoutResult = () => {
  let resultTextArray: string[] = []
  let nowTime = new Date()
  let showDate = `${nowTime.getMonth() + 1}/${nowTime.getDate()}`
  let showTime = ""

  if (currentUser.shift == 'day_class') {
    showTime = '7-19'
  } else if (currentUser.shift == 'night_class') {
    if (showMode.value == 'night-1') {
      showTime = '19-24'
    } else if (showMode.value == 'night-2') {
      showTime = '0-7'
    }
  }

  resultTextArray.push(
    "日期  時間",
    `${showDate} ${currentUser.nickname} ${showTime}`,
  )

  // 複製資產明細
  let propertyInfo = propertyData.value.map((x: any) => {
    return `${x.name}餘額: ${x.balance}`
  })
  let propertyTotalBalance = propertyData.value.map((x: any) => x.balance).reduce((accu, curr) => accu + curr, 0)
  resultTextArray.push(
    "■■■■■ 資產明細 ■■■■■ ",
    ...propertyInfo,
    `🍔 銀行總額: ${propertyTotalBalance}`,
    ""
  )

  // 複製庫存資訊
  gameStockData.value.forEach((gameStock: any, index: number) => {
    resultTextArray.push(`●●● ${gameStock.name}總庫存 ●●●`)

    let gameStocks = gameStockAllData.value[index]['stock']
    gameStocks.forEach((stock: any) => {
      resultTextArray.push(`${stock.role_name}庫存: ${stock.balance}`)
    })

    resultTextArray.push(
      `金幣總數: ${calcArraySum(gameStocks.map((x: any) => x.balance))}`,
      "---------------------------------",
      `轉入幣總: ${calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_in))}`,
      `轉出現金: ${calcArraySum(gameStock['stock'].map((x: any) => x.money_out))}`,
      "",
      `轉出幣總: ${calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_out))}`,
      `活動幣: ${calcArraySum(gameStock['stock'].map((x: any) => x.activity_coin))}`,
      `官方手續費: ${calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_fee_out))}`,
      `合計 = ${calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_out_total))}`,
      "",
      `※ 當班營業額【${calcArraySum(gameStock['stock'].map((x: any) => x.money_in))}】`,
    )

    if (index < gameStockData.value.length - 1) {
      resultTextArray.push("", "")
    }
  })

  navigator.clipboard.writeText(resultTextArray.join("\n"))
    .then(() => {
      createNotify("info", "已將結帳結果複製至剪貼簿")
    })
}

onMounted(() => {
  checkoutTrade()
})
</script>

<template>
  <div class="container my-3">
    <div class="d-flex" style="flex-direction: column-reverse;">
      <button class="btn btn-success mx-2 justify-end" @click="() => copyCheckoutResult()">複製結果</button>
    </div>
    <DataTable titleText="資產明細" :fieldInfo :containerSize v-model:tableData="propertyData" />

    <div class="my-2">
      <template v-for="(gameStock, index) in gameStockData">
        <hr>
        <DataTable
          :titleText="`${gameStock['name']} 總庫存`"
          :fieldInfo="allGameStockfieldInfo"
          :containerSize
          v-model:tableData="gameStockAllData[index]['stock']"
        />
        <p class="text-center">金幣總數: {{ calcArraySum(gameStockAllData[index]['stock'].map((x: any) => x.balance)) }}</p>

        <!-- <template v-for="i in 3"> -->
        <template v-for="i in 1">
          <DataTable
            :fieldInfo="calcFinalfieldInfo"
            :containerSize
            v-model:tableData="calcFinalData[index][i - 1]"
          >
            <template #tableCell="{ fieldName, dataIndex }">
              <span v-if="fieldName == 'title'">
                {{ titleTransform(calcFinalData[index][i - 1][dataIndex]['title']) }}
              </span>
            </template>
          </DataTable>
        </template>
      </template>
    </div>
  </div>
</template>
