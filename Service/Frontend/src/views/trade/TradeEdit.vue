<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { pageParameters } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const tradeEditFields = reactive<CustomFormField[]>([
  { label: '編號', type: 'text', depValue: 'custom_no' },
  { label: '末五碼', type: 'text', depValue: 'last_five_code', hidden: true },
  { label: '時間紀錄', type: 'time', depValue: 'record_time', hidden: true },
  { label: '繳費代碼', type: 'text', depValue: 'pay_code', hidden: true },
  { label: '門市', type: 'text', depValue: 'store', hidden: true },
  { label: '虛擬帳號', type: 'text', depValue: 'v_account', hidden: true },
  { label: '金額修正 (多給的)', type: 'number', depValue: 'money_correction', hidden: true },
  { label: '遊戲幣修正 (多給的)', type: 'number', depValue: 'game_coin_correction', hidden: true },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => backToProperyDetails(), needValid: true },
  { color: 'primary', text: '更新', method: () => updateTrade(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['trades']?.['editId']
})
const currentKind = computed<string>(() => {
  return pageParameters['trades']?.['showKind']
})
const currentType = computed<string>(() => {
  return pageParameters['trades']?.['basyType']
})

onMounted(() => {
  getTradeInfo()
  showKindFields()
})

const getTradeInfo = () => {
  callApi('get', `/apis/trades/${currentEditId.value}`)
    .then((res: any) => {
      tradeEditFields.forEach((field: DataObject) => {
        formData[field.depValue] = res.data['details'][field.depValue]
      })

      formData['money_correction'] = res.data['money_correction']
      formData['game_coin_correction'] = res.data['game_coin_correction']
    })
}

const showKindFields = () => {
  let lastFiveCodeFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'last_five_code')
  let recordTimeFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'record_time')
  let payCodeFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'pay_code')
  let storeFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'store')
  let vAccountFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'v_account')
  let moneyCorrectionFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'money_correction')
  let gameCoinCorrectionFieldIndex = tradeEditFields.findIndex(x => x.depValue == 'game_coin_correction')

  switch (currentKind.value) {
    case 'bank':
      tradeEditFields[lastFiveCodeFieldIndex].hidden = false
      tradeEditFields[recordTimeFieldIndex].hidden = false
      break

    case 'supermarket':
      tradeEditFields[payCodeFieldIndex].hidden = false
      tradeEditFields[storeFieldIndex].hidden = false
      break

    case 'v_account':
      tradeEditFields[lastFiveCodeFieldIndex].hidden = false
      tradeEditFields[vAccountFieldIndex].hidden = false
      break
  }

  if (currentType.value == 'money_in') {
    tradeEditFields[gameCoinCorrectionFieldIndex].hidden = false
  } else if (currentType.value == 'money_out') {
    tradeEditFields[moneyCorrectionFieldIndex].hidden = false
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
  let requestData = {
    details: formData,
    money_correction: formData['money_correction'],
    game_coin_correction: formData['game_coin_correction'],
  }

  callApi('patch', `/apis/trades/${currentEditId.value}`, requestData)
    .then((_) => {
      createNotify('question', `一筆交流紀錄已更新 !`)
      backToProperyDetails()
    })
}

</script>

<template>
  <div class="container">
    <div class="m-4">
      <h3 class="text-center">編輯交流單</h3>
    </div>
    <CustomForm
      :fields="tradeEditFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
