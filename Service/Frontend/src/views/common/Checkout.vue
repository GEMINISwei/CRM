<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { currentUser, pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { DataObject } from '@/type'

const checkoutData = ref<DataObject>({})

const propertyData = computed<DataObject[]>(() => {
  return checkoutData.value['property']?.['list_data']
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

onMounted(() => {
  checkoutTrade()
})
</script>

<template>
  <div class="container my-3">
    <div class="my-2">
      <h3>資產餘額</h3>
      <p v-for="property in propertyData">
        {{ property['name'] }}: {{ property['balance'] }}
      </p>
    </div>
    <br>

    <div class="my-2">
      <template v-for="(gameStock, index) in gameStockData">
        <hr>
        <br>
        <h3>{{ gameStock['name'] }} 總庫存</h3>
        <template v-for="stock in gameStockAllData[index]['stock']">
          <p>{{ stock['role_name'] }}: {{ stock['balance'] }}</p>
        </template>
        <p>金幣總數: {{ calcArraySum(gameStockAllData[index]['stock'].map((x: any) => x.balance)) }}</p>
        <br>
        <p>轉入幣總: {{ calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_in)) }}</p>
        <p>轉出現金: {{ calcArraySum(gameStock['stock'].map((x: any) => x.money_out)) }}</p>
        <br>
        <p>轉出幣: {{ calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_out)) }}</p>
        <p>活動幣: {{ calcArraySum(gameStock['stock'].map((x: any) => x.activity_coin)) }}</p>
        <p>官方手續費: {{ calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_fee_out)) }}</p>
        <p>合計:  {{ calcArraySum(gameStock['stock'].map((x: any) => x.game_coin_out_total)) }}</p>
        <p>當班營業額:  {{ calcArraySum(gameStock['stock'].map((x: any) => x.money_in)) }}</p>
      </template>
    </div>
  </div>
</template>
