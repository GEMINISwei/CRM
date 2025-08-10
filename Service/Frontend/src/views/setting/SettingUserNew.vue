<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const userShiftOptions: OptionObject[] = [
  { text: '早班', value: 'day_class' },
  { text: '晚班', value: 'night_class' },
]

const permissionNewFields = reactive<CustomFormField[]>([
  { label: '暱稱', type: 'text', depValue: 'nickname', required: true },
  { label: '帳號', type: 'text', depValue: 'username', required: true },
  { label: '密碼', type: 'password', depValue: 'password', required: true },
  { label: '班別', type: 'select', depValue: 'shift', options: userShiftOptions, required: true },
  { label: '權限群組', type: 'select', depValue: 'level_group', options: [], required: true },
])
const formData = reactive<DataObject>(permissionNewFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/settings/permission') },
  { color: 'primary', text: '新增', method: () => createUser(), needValid: true },
]

const createUser = (): void => {
  callApi('post', '/apis/users', formData)
    .then(() => {
      createNotify('success', '新增使用者成功')
      goPage('/settings/permission')
    })
}

const getPermissionInfo = () => {
  callApi('get', '/apis/settings/permission/all')
    .then((resData: any) => {
      let levelGroupField = permissionNewFields.find(x => x.depValue == 'level_group')

      if (levelGroupField) {
        levelGroupField.options = Object.keys(resData['value']).map(x => {
          return {
            text: x,
            value: x,
          }
        })
      }
    })
}

onMounted(() => {
  getPermissionInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增使用者</h3>
    <CustomForm
      :fields="permissionNewFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
