<script lang="ts" setup>
import { reactive } from 'vue'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const settingFields = reactive<CustomFormField[]>([
  // Trade Create
  { label: '代收平台 - 手續費', type: 'number', depValue: 'supermarket_stage_fee', required: true },
  { label: '虛擬帳號 - 手續費', type: 'number', depValue: 'v_account_stage_fee', required: true },
  // Property Detail
  { label: '管理者 - 代表顏色', type: 'color', depValue: 'admin_color', required: true },
  { label: '早班 - 代表顏色', type: 'color', depValue: 'day_class_color', required: true },
  { label: '晚班 - 代表顏色', type: 'color', depValue: 'night_class_color', required: true },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '更新', method: () => updateSettings(), needValid: true },
]

const updateSettings = (): void => {
  console.log(formData)
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">系統設定</h3>
    <CustomForm
      :fields="settingFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
