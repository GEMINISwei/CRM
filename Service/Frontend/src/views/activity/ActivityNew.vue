<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const activityNewFields = reactive<CustomFormField[]>([
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true },
  { label: '活動名稱', type: 'text', depValue: 'name', required: true },
  { label: '出入金類型', type: 'select', depValue: 'base_type', required: true },
  { label: '開始日期', type: 'date', depValue: 'start_time', required: true },
  { label: '結束日期', type: 'date', depValue: 'end_time', required: true },
  { label: '滿額條件', type: 'number', depValue: 'money_floor', required: true },
  { label: '贈送遊戲幣', type: 'float', depValue: 'coin_free', required: true },
])
const formBtns = reactive<CustomFormButton[]>([
  { color: 'secondary', text: '返回', method: () => goPage('/activities') },
  { color: 'primary', text: '新增', method: () => createActivity(), needValid: true },
])
const formData = reactive<DataObject>({})

const getFormField = (field: string): CustomFormField | undefined => {
  return activityNewFields.find(x => x.depValue == field)
}

const createActivity = (): void => {
  callApi('post', '/apis/activities', formData)
    .then((resData: any) => {
      createNotify('success', `已建立 ${resData.name} 活動`)
      goPage('/activities')
    })
    .catch(() => {
      createNotify('error', '建立活動失敗 !')
    })
}

const getGameOptions = (): void => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      let gameField = getFormField('game_id')

      if (gameField) {
        gameField.options = resData.list_data.map((x: any) => {
          return {
            text: x['name'],
            value: x['id'],
          }
        })
      }
    })
}

const setBaseTypeOptions = (): void => {
  let baseTypeField = getFormField('base_type')

  if (baseTypeField) {
    baseTypeField.options = [
      { text: '入金', value: 'money_in' },
      { text: '出金', value: 'money_out' },
    ]
  }
}

onMounted(() => {
  getGameOptions()
  setBaseTypeOptions()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增活動</h3>
    <CustomForm
      :fields="activityNewFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
