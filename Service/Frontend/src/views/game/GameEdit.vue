<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { pageParameters } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton, OptionObject } from '@/type'

const filterSettingOptions: OptionObject[] = [
  { text: '依照開單時間排序', value: 'by_created_time' },
  { text: '依照完成時間排序', value: 'by_finished_time' },
]

const gameEditFields = reactive<CustomFormField[]>([
  { label: '遊戲名稱', type: 'text', depValue: 'name', required: true, disabled: true },
  { label: '入金 - 遊戲幣匯率 (台幣 : 遊戲幣 - 1 : XXX)', type: 'float', depValue: 'money_in_exchange', required: true },
  { label: '出金 - 遊戲幣匯率 (台幣 : 遊戲幣 - 1 : XXX)', type: 'float', depValue: 'money_out_exchange', required: true },
  { label: '交易手續費 (台幣)', type: 'number', depValue: 'charge_fee' },
  { label: '遊戲幣手續費', type: 'float', depValue: 'game_coin_fee' },
  { label: '超商滿額設定 (免手續費)', type: 'number', depValue: 'market_free_fee' },
  { label: '排序設定', type: 'select', depValue: 'filter_setting', options: filterSettingOptions },
])
const formData = reactive<DataObject>(gameEditFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/games') },
  { color: 'primary', text: '更新', method: () => updateGame(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['games']?.['editId']
})

onMounted(() => {
  if (currentEditId.value) {
    getGameData()
  } else {
    goPage('/games')
  }
})

const getGameData = () => {
  callApi('get', `/apis/games/${currentEditId.value}`)
    .then((resData: any) => {
      gameEditFields.forEach((field: DataObject) => {
        formData[field.depValue] = resData[field.depValue]
      })
    })
}

const updateGame = () => {
  callApi('patch', `/apis/games/${currentEditId.value}`, formData)
    .then((res: any) => {
      createNotify('success', `遊戲類別 "${res.name}" 資料更新成功 !`)
      goPage('/games')
    })
    .catch((err: any) => {
      if (err.status == 405) {
        createNotify('info', `內容無變更, 請確認更新資訊 !`)
      }
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯遊戲類別</h3>
    <CustomForm
      :fields="gameEditFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
