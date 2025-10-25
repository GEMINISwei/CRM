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
  'record_hour': { label: '時間紀錄 (時)', type: 'number', min: 0, max: 23 },
  'record_minute': { label: '時間紀錄 (分)', type: 'number', min: 0, max: 59 },
  'pay_code': { label: '繳費代碼', type: 'text' },
  'store': { label: '門市', type: 'text' },
  'v_account': { label: '虛擬帳號', type: 'text' },
  'diff_bank_fee': { label: '跨行手續費', type: 'number' },
  'money_correction': { label: '金額修正 (錯帳)', type: 'text' },
  'game_coin_correction': { label: '遊戲幣修正 (錯帳)', type: 'text' },
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

        if (depValue == 'money_correction' || depValue == 'game_coin_correction') {
          if (!resData['details'][depValue]) {
            formData[depValue] = 0
          }
        }
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
  if (formFields['game_coin_correction'].hidden == false) {
    formData['game_coin_correction'] = 0
  }
}

const backToProperyDetails = () => {
  goPage('/properties/details', {
    showTitle: pageParameters['trades']?.['propertyName'],
    showKind: pageParameters['trades']?.['showKind'],
    showId: pageParameters['trades']?.['propertyId'],
  })
}

const updateTrade = () => {
  let skipThis = false

  // 金幣、遊戲幣錯帳更新前 text 轉 number
  Object.keys(formData).forEach((depValue: string) => {
    if (depValue == 'money_correction' || depValue == 'game_coin_correction') {
      let newVal = Number(formData[depValue])

      if (isNaN(newVal)) {
        let errorField = depValue == 'money_correction' ? '台幣' : '遊戲幣'

        createNotify('error', `${errorField}輸入值異常 !`)
        skipThis = true
        return // 跳出不處理
      } else {
        formData[depValue] = Number(formData[depValue])
      }
    }

    // 隱藏的欄位全部刪除
    if (formFields[depValue].hidden) {
      delete formData[depValue]
    }
  })

  if (skipThis) return

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
