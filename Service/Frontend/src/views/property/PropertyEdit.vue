<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api.ts'
import { setStatusFlag, pageParameters } from '@/composables/globalUse.ts'
import { createNotify } from '@/composables/notify.ts'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const propertyEditfields = reactive<CustomFormField[]>([
  { label: '名稱', type: 'text', depValue: 'name', required: true },
  { label: '初始金額', type: 'text', depValue: 'init_amount', required: true },
])
const formData = reactive<DataObject>({})
const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/properties/details') },
  { color: 'primary', text: '更新', method: () => updateProperty(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['properties']?.['propertyId']
})

const getPropertyData = () => {
  callApi('get', `/apis/properties/${currentEditId.value}`)
    .then((resData: any) => {
      formData['name'] = resData['name']
      formData['kind'] = resData['kind']
      formData['init_amount'] = resData['init_amount']
    })
}

const updateProperty = (): void => {
  setStatusFlag('loading', true)

  callApi('patch', `/apis/properties/${currentEditId.value}`, formData)
    .then((res: any) => {
      createNotify('success', `銀行 "${res.name}" 編輯成功`)
      setStatusFlag('loading', false)
      goPage('/properties')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}

onMounted(() => {
  getPropertyData()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯資產</h3>
    <CustomForm :fields="propertyEditfields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
