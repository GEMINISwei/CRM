<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const pagePermissionOptions: OptionObject[] = [
  { text: '可操作', value: 'Y' },
  { text: '不可操作', value: 'N' },
]

const permissionNewFields = reactive<CustomFormField[]>([
  { label: '群組名稱', type: 'text', depValue: 'level_group', required: true },
  { label: '遊戲管理', type: 'select', depValue: 'game_page', options: pagePermissionOptions, required: true },
  { label: '會員管理', type: 'select', depValue: 'member_page', options: pagePermissionOptions, required: true },
  { label: '資產管理', type: 'select', depValue: 'property_page', options: pagePermissionOptions, required: true },
  { label: '庫存管理', type: 'select', depValue: 'stock_page', options: pagePermissionOptions, required: true },
  { label: '交流單管理', type: 'select', depValue: 'trade_page', options: pagePermissionOptions, required: true },
  { label: '活動管理', type: 'select', depValue: 'activity_page', options: pagePermissionOptions, required: true },
  { label: '員工管理', type: 'select', depValue: 'staff_page', options: pagePermissionOptions, required: true },
])
const formData = reactive<DataObject>(permissionNewFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/settings/permission') },
  { color: 'primary', text: '新增', method: () => createPermission(), needValid: true },
]

const createPermission = (): void => {
  let level_group = formData['level_group']

  delete formData.level_group

  let setFormData = {
    collection_name: 'permission',
    field: level_group,
    value: formData
  }

  callApi('patch', '/apis/set_settings', setFormData)
    .then(() => {
      createNotify('success', '新增設定成功')
      goPage('/settings/permission')
    })
}

onMounted(() => {
  Object.keys(formData).forEach((fieldName: string) => {
    if (fieldName != 'level_group') {
      formData[fieldName] = 'N'
    }
  })
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增權限群組</h3>
    <CustomForm
      :fields="permissionNewFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
