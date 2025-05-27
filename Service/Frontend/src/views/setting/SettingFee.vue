<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { CustomFormField, DataObject, CustomFormButton } from '@/type'

const formFields = reactive<CustomFormField[]>([
  { label: '超商平台', type: 'number', depValue: 'supermarket_stage', required: true, min: 0 },
  { label: '虛擬帳號', type: 'number', depValue: 'v_account_stage', required: true, min: 0 },
])
const formData = reactive<DataObject>(formFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '設定', method: () => updateFeeSetting(), needValid: true },
  { color: 'secondary', text: '返回', method: () => goPage('/settings') },
]

const getFeeInfo = () => {
  callApi('get', '/apis/settings/trade/fee')
    .then((resData: any) => {
      for (let fieldIdx = 0; fieldIdx < formFields.length; fieldIdx++) {
        let depValue = formFields[fieldIdx].depValue

        formData[depValue] = resData['value'][depValue]
      }
    })
}
const updateFeeSetting = () => {
  let updateFormData = {
    collection_name: 'trade',
    field: 'fee',
    value: formData
  }

  callApi('patch', '/apis/set_settings', updateFormData)
    .then((_: any) => {
      getFeeInfo()
      createNotify('success', '更新設定成功')
    })
}

onMounted(() =>{
  getFeeInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">手續費設定</h3>
    <CustomForm
      class="m-2"
      :fields="formFields"
      :colSize="8"
      :colOffset="2"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
