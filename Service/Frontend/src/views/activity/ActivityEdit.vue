<script lang="ts" setup>
import { reactive, computed, watch, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const activityEditFields = reactive<CustomFormField[]>([
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true, disabled: true },
  { label: '活動名稱', type: 'text', depValue: 'name', required: true },
  { label: '出入金類型', type: 'text', depValue: 'base_type', required: true, disabled: true },
  { label: '開始日期', type: 'date', depValue: 'start_time', required: true },
  { label: '結束日期', type: 'date', depValue: 'end_time', required: true },
  { label: '滿額條件', type: 'number', depValue: 'match_condition', required: true },
  { label: '贈送遊戲幣', type: 'number', depValue: 'coin_free', required: true, hidden: true },
  { label: '贈送台幣', type: 'number', depValue: 'money_free', required: true, hidden: true },
])
const formBtns = reactive<CustomFormButton[]>([
  { color: 'success', text: '返回', method: () => goPage('/activities') },
  { color: 'primary', text: '更新', method: () => updateActivity(), needValid: true },
  { color: 'danger', text: '刪除', method: () => deleteActivity() },
])
const formData = reactive<DataObject>({})

const currentEditId = computed<string>(() => {
  return pageParameters['activities']?.['editId']
})

const getFormField = (field: string): CustomFormField | undefined => {
  return activityEditFields.find(x => x.depValue == field)
}

const getActivityData = (): void => {
  callApi('get', `/apis/activities/${currentEditId.value}`)
    .then((resData: any) => {
      activityEditFields.forEach((field: DataObject) => {
        let fieldValue = ''

        if (field.depValue == 'start_time' || field.depValue == 'end_time') {
          if (resData[field.depValue]) {
            fieldValue = resData[field.depValue].slice(0, 10)
          }
        } else if (field.depValue == 'base_type') {
          if (resData[field.depValue] == 'money_in') {
            fieldValue = '入金'
          } else if (resData[field.depValue] == 'money_out') {
            fieldValue = '出金'
          }
        } else {
          fieldValue = resData[field.depValue]
        }

        formData[field.depValue] = fieldValue
      })
    })
}

const updateActivity = (): void => {
  callApi('patch', `/apis/activities/${currentEditId.value}`, formData)
    .then((resData: any) => {
      createNotify('success', `活動 "${resData.name}" 已更新 !`)
      goPage('/activities')
    })
    .catch((err: any) => {
      if (err.status == 405) {
        createNotify('info', `內容無變更, 請確認更新資訊 !`)
      } else {
        createNotify('error', "活動更新失敗 !")
      }
    })
}

const deleteActivity = (): void => {
  callApi('delete', `/apis/activities/${currentEditId.value}`)
    .then((resData: any) => {
      createNotify('success', `活動 "${resData.name}" 已刪除 !`)
      goPage('/activities')
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

watch(() => formData['base_type'], (newVal) => {
  let coinFreeField = getFormField("coin_free")
  let moneyFreeField = getFormField("money_free")

  if (!coinFreeField || !moneyFreeField) return

  if (newVal == '入金') {
    coinFreeField.hidden = false
  } else if (newVal == '出金') {
    moneyFreeField.hidden = false
  }
})

onMounted(() => {
  if (currentEditId.value) {
    getActivityData()
    getGameOptions()
  } else {
    goPage('/activities')
  }
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯活動</h3>
    <CustomForm :fields="activityEditFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
