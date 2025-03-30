<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { CustomFormField, DataObject, CustomFormButton } from '@/type'

const formFields = reactive<CustomFormField[]>([
  { label: '管理者', type: 'color', depValue: 'admin', required: true },
  { label: '早班', type: 'color', depValue: 'day_class', required: true },
  { label: '晚班', type: 'color', depValue: 'night_class', required: true },
])
const formData = reactive<DataObject>(formFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: '#FFFFFF'
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '設定', method: () => updateColorSetting(), needValid: true },
  { color: 'secondary', text: '返回', method: () => goPage('/settings') },
]

const getColorInfo = () => {
  callApi('get', '/apis/settings/trade/color')
    .then((resData: any) => {
      for (let fieldIdx = 0; fieldIdx < formFields.length; fieldIdx++) {
        let depValue = formFields[fieldIdx].depValue

        formData[depValue] = resData['value'][depValue]
      }
    })
}
const updateColorSetting = () => {
  let updateFormData = {
    collection_name: 'trade',
    field: 'color',
    value: formData
  }

  callApi('patch', '/apis/set_settings', updateFormData)
    .then((_: any) => {
      getColorInfo()
      createNotify('success', '更新設定成功')
    })
}

onMounted(() =>{
  getColorInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">代表顏色設定</h3>
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
