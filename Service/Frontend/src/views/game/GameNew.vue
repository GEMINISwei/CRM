<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

// const filterSettingOptions: OptionObject[] = [
//   { text: '依照開單時間排序', value: 'created' },
//   { text: '依照完成時間排序', value: 'finished' },
// ]

const gameNewFields = reactive<CustomFormField[]>([
  { label: '遊戲名稱', type: 'text', depValue: 'name', required: true },
  { label: '入金 - 遊戲幣匯率 (台幣 : 遊戲幣 - 1 : XXX)', type: 'float', depValue: 'money_in_exchange', required: true },
  { label: '出金 - 遊戲幣匯率 (台幣 : 遊戲幣 - 1 : XXX)', type: 'float', depValue: 'money_out_exchange', required: true },
  { label: '交易手續費 (台幣)', type: 'number', depValue: 'charge_fee' },
  { label: '遊戲幣手續費', type: 'float', depValue: 'game_coin_fee' },
  { label: '超商滿額設定 (免手續費)', type: 'number', depValue: 'market_free_fee' },
  // { label: '排序設定', type: 'select', depValue: 'filter_setting', options: filterSettingOptions },
])
const formData = reactive<DataObject>(gameNewFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/games') },
  { color: 'primary', text: '新增', method: () => createGame(), needValid: true },
]

const createGame = (): void => {
  callApi('post', '/apis/games', formData)
    .then((resData: any) => {
      createNotify('success', `已建立 "${resData.name}" 遊戲類別`)
      goPage('/games')
    })
    .catch((err: any) => {
      if (err.status == 409) {
        createNotify('info', '遊戲已存在 !')
      } else {
        createNotify('error', '遊戲建立失敗 !')
      }
    })
}

onMounted(() => {
  formData["market_free_fee"] = 0
  formData["filter_setting"] = "created"
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增遊戲類別</h3>
    <CustomForm
      :fields="gameNewFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
