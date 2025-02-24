<script lang="ts" setup>
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api.ts'
import { setStatusFlag } from '@/composables/globalUse.ts'
import { createNotify } from '@/composables/notify.ts'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const stockNewfields = reactive<CustomFormField[]>([
  { label: '名稱', type: 'text', depValue: 'role_name', required: true },
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true },
  { label: '角色數量', type: 'text', depValue: 'init_amount' },
])
const formData = reactive<DataObject>({})
const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/stocks') },
  { color: 'primary', text: '新增', method: () => createStockRole(), needValid: true },
]

onMounted(() => {
  getGameList()
})

const getGameList = (): void => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      let gameIdFieldIndex = stockNewfields.findIndex((field: CustomFormField) => field.depValue == 'game_id')

      stockNewfields[gameIdFieldIndex].options = resData.list_data.map((x: any) => {
        return {
          text: x['name'],
          value: x['id'],
        }
      })
    })
}

const createStockRole = (): void => {
  setStatusFlag('loading', true)

  callApi('post', '/apis/stocks', formData)
    .then((resData: any) => {
      createNotify('success', `庫存角色 "${resData.role_name}" 新增成功`)
      setStatusFlag('loading', false)
      goPage('/stocks')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增庫存角色</h3>
    <CustomForm :fields="stockNewfields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
