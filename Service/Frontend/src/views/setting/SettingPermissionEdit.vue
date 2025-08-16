<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { pageParameters } from '@/composables/globalUse'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const pagePermissionOptions: OptionObject[] = [
  { text: '可操作', value: 'Y' },
  { text: '不可操作', value: 'N' },
]

const permissionEditFields = reactive<CustomFormField[]>([
  { label: '群組名稱', type: 'text', depValue: 'level_group', required: true, disabled: true },
  { label: '遊戲管理', type: 'select', depValue: 'game_page', options: pagePermissionOptions, required: true },
  { label: '會員管理', type: 'select', depValue: 'member_page', options: pagePermissionOptions, required: true },
  { label: '資產管理', type: 'select', depValue: 'property_page', options: pagePermissionOptions, required: true },
  { label: '庫存管理', type: 'select', depValue: 'stock_page', options: pagePermissionOptions, required: true },
  { label: '交流單管理', type: 'select', depValue: 'trade_page', options: pagePermissionOptions, required: true },
  { label: '活動管理', type: 'select', depValue: 'activity_page', options: pagePermissionOptions, required: true },
  { label: '員工管理', type: 'select', depValue: 'staff_page', options: pagePermissionOptions, required: true },
])
const formData = reactive<DataObject>(permissionEditFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/settings/permission') },
  { color: 'primary', text: '更新', method: () => updatePermission(), needValid: true },
]

const currentLevelGroup = computed<string>(() => {
  return pageParameters['settings']?.['levelGroup']
})

const updatePermission = (): void => {
  delete formData.level_group

  let setFormData = {
    collection_name: 'permission',
    field: currentLevelGroup.value,
    value: formData
  }

  callApi('patch', '/apis/set_settings', setFormData)
    .then(() => {
      createNotify('success', '更新設定成功')
      goPage('/settings/permission')
    })
}

const getPermissionInfo = () => {
  callApi('get', `/apis/settings/permission/${currentLevelGroup.value}`)
    .then((resData: any) => {
      Object.keys(formData).forEach((field: string) => {
        if (field == 'level_group') {
          formData[field] = resData['field']
        } else {
          formData[field] = resData['value'][field]
        }
      })
    })
}

onMounted(() => {
  getPermissionInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯權限群組</h3>
    <CustomForm
      :fields="permissionEditFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
