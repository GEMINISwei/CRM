<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { pageParameters } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import BaseForm from '@/components/BaseForm.vue'
import type { BaseFormFields, BaseFormButton, DataObject } from '@/type'


const formFields = reactive<BaseFormFields>({
  'custom_no': { label: '編號', type: 'text' },
  'last_five_code': { label: '末五碼', type: 'text' },
  'record_time': { label: '時間紀錄', type: 'time' },
  'pay_code': { label: '繳費代碼', type: 'text' },
  'store': { label: '門市', type: 'text' },
  'v_account': { label: '虛擬帳號', type: 'text' },
  'diff_bank_fee': { label: '跨行手續費', type: 'number' },
  'money_correction': { label: '金額修正 (多給的)', type: 'number' },
  'game_coin_correction': { label: '遊戲幣修正 (多給的)', type: 'number' },
})
const formBtns: BaseFormButton[] = [
  { color: 'secondary', text: '返回', method: () => backToProperyDetails() },
  { color: 'primary', text: '更新', method: () => updateTrade(), needValid: true },
]
const formData = reactive<DataObject>({})
const pageParams = computed<DataObject>(() => {
  return pageParameters['trades']
})


const getTradeInfo = () => {
  callApi('get', `/apis/trades/${pageParams.value.editId}`)
    .then((resData: any) => {
      Object.keys(formFields).forEach((depValue: string) => {
        formData[depValue] = resData['details'][depValue]
      })
    })
}

const showKindFields = () => {
  switch (pageParams.value.showKind) {
    case 'bank':
      formFields['pay_code'].hidden = true
      formFields['store'].hidden = true
      formFields['v_account'].hidden = true

      if (pageParams.value.basyType == 'money_in') {
        formFields['diff_bank_fee'].hidden = true
      }
      break

    case 'supermarket':
      formFields['last_five_code'].hidden = true
      formFields['record_time'].hidden = true
      formFields['v_account'].hidden = true
      formFields['diff_bank_fee'].hidden = true
      break

    case 'v_account':
      formFields['record_time'].hidden = true
      formFields['pay_code'].hidden = true
      formFields['store'].hidden = true
      formFields['diff_bank_fee'].hidden = true
      break
  }

  formFields['money_correction'].hidden = pageParams.value.basyType == 'money_in'
  formFields['game_coin_correction'].hidden = pageParams.value.basyType == 'money_out'
}

const backToProperyDetails = () => {
  goPage('/properties/details', {
    showTitle: pageParameters['trades']?.['propertyName'],
    showKind: pageParameters['trades']?.['showKind'],
    showId: pageParameters['trades']?.['propertyId'],
  })
}

const updateTrade = () => {
  let request_data = {
    details: JSON.parse(JSON.stringify(formData))
  }

  callApi('patch', `/apis/trades/${pageParams.value.editId}`, request_data)
    .then((_) => {
      createNotify('question', `一筆交流紀錄已更新 !`)
      backToProperyDetails()
    })
    .catch((err: any) => {
      if (err.status == 405) {
        createNotify('info', `內容無變更, 請確認更新資訊 !`)
      }
    })
}


onMounted(() => {
  getTradeInfo()
  showKindFields()
})
</script>

<template>
  <div class="container">
    <div class="m-4">
      <h3 class="text-center">編輯交流單</h3>
    </div>
    <BaseForm
      v-model:fields="formFields"
      v-model:formData="formData"
      v-model:buttons="formBtns"
    />
  </div>
</template>
