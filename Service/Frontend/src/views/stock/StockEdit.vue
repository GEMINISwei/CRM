<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api.ts'
import { setStatusFlag, pageParameters } from '@/composables/globalUse.ts'
import { createNotify } from '@/composables/notify.ts'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const stockEditfields = reactive<CustomFormField[]>([
  { label: '名稱', type: 'text', depValue: 'role_name', required: true },
  { label: '初始金額', type: 'text', depValue: 'init_amount', required: true },
])
const formData = reactive<DataObject>({})
const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/stocks') },
  { color: 'primary', text: '更新', method: () => updateStock(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['stocks']?.['stockId']
})

const getStockData = () => {
  callApi('get', `/apis/stocks/${currentEditId.value}`)
    .then((resData: any) => {
      formData['role_name'] = resData['role_name']
      formData['init_amount'] = resData['init_amount']
    })
}

const updateStock = (): void => {
  setStatusFlag('loading', true)

  callApi('patch', `/apis/stocks/${currentEditId.value}`, formData)
    .then((res: any) => {
      createNotify('success', `銀行 "${res.name}" 編輯成功`)
      setStatusFlag('loading', false)
      goPage('/stocks')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}

onMounted(() => {
  getStockData()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯庫存</h3>
    <CustomForm :fields="stockEditfields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
