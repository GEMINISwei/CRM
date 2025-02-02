<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api.ts'
import { setStatusFlag } from '@/composables/globalUse.ts'
import { createNotify } from '@/composables/notify.ts'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const chargeMethodOptions: OptionObject[] = [
  { text: '銀行轉帳', value: 'bank' },
  { text: '超商代收', value: 'supermarket' },
  { text: '虛擬帳號', value: 'v_account' },
]
const propertyNewfields = reactive<CustomFormField[]>([
  { label: '名稱', type: 'text', depValue: 'name', required: true },
  { label: '類型', type: 'select', depValue: 'kind', required: true, options: chargeMethodOptions },
  { label: '帳戶', type: 'text', depValue: 'account' },
  { label: '初始金額', type: 'text', depValue: 'init_amount' },
])
const formData = reactive<DataObject>({})
const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/properties') },
  { color: 'primary', text: '新增', method: () => createBank(), needValid: true },
]

watch(() => formData['kind'], (newVal) => {
  let accountFieldIndex = propertyNewfields.findIndex((field: CustomFormField) => field.depValue == 'account')

  if (newVal == 'supermarket' || newVal == '') {
    propertyNewfields[accountFieldIndex].disabled = true
    formData['account'] = ''
  } else {
    propertyNewfields[accountFieldIndex].disabled = false
  }
})

const createBank = (): void => {
  setStatusFlag('loading', true)

  callApi('post', '/apis/properties', formData)
    .then((res: any) => {
      createNotify('success', `銀行 "${res.name}" 新增成功`)
      setStatusFlag('loading', false)
      goPage('/properties')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增資產</h3>
    <CustomForm :fields="propertyNewfields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
