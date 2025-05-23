<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const sexOptions: OptionObject[] = [
  { text: '男', value: '男' },
  { text: '女', value: '女' },
]
const memberEditFields = reactive<CustomFormField[]>([
  { label: '遊戲暱稱', type: 'text', depValue: 'nickname', required: true, disabled: true },
  { label: '性別', type: 'select', depValue: 'sex', options: sexOptions },
  { label: '首次交流時間', type: 'date', depValue: 'first_communication_time' },
  { label: '交流方式', type: 'select', depValue: 'first_communication_way' },
  { label: '首次交易金額', type: 'text', depValue: 'first_communication_amount' },
  { label: '註解', type: 'textarea', depValue: 'description' },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/members') },
  { color: 'primary', text: '更新', method: () => updateMember(), needValid: true },
  { color: 'danger', text: '刪除', method: () => deleteMember() },
]

const currentEditId = computed<string>(() => {
  return pageParameters['members']?.['editId']
})

onMounted(() => {
  if (currentEditId.value) {
    getMemberData()
    getCommWayOptions()
  } else {
    goPage('/members')
  }
})

const getMemberData = () => {
  callApi('get', `/apis/members/${currentEditId.value}`)
    .then((resData: any) => {
      memberEditFields.forEach((field: DataObject) => {
        let fieldValue = ''

        if (field.depValue == 'first_communication_time') {
          if (resData[field.depValue]) {
            fieldValue = resData[field.depValue].slice(0, 10)
          }
        } else {
          fieldValue = resData[field.depValue]
        }

        formData[field.depValue] = fieldValue
      })
    })
}

const getCommWayOptions = (): void => {
  callApi('get', '/apis/settings/member/communication_ways')
      .then((resData: any) => {
        let commWayFieldIndex = memberEditFields.findIndex((field: CustomFormField) => {
          return field.depValue == 'first_communication_way'
        })

        memberEditFields[commWayFieldIndex].options = resData['communication_ways'].map((x: any) => {
          return {
            text: x,
            value: x,
          }
        })
      })
}

const updateMember = () => {
  callApi('patch', `/apis/members/${currentEditId.value}`, formData)
    .then((resData: any) => {
      createNotify('success', `會員 "${resData.nickname}" 已更新 !`)
      goPage('/members')
    })
    .catch((err: any) => {
      if (err.status == 405) {
        createNotify('info', `內容無變更, 請確認更新資訊 !`)
      } else {
        createNotify('error', err.message)
      }
    })
}

const deleteMember = () => {
  callApi('delete', `/apis/members/${currentEditId.value}`)
    .then((resData: any) => {
      createNotify('success', `會員 "${resData.nickname}" 已刪除 !`)
      goPage('/members')
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯會員</h3>
    <CustomForm :fields="memberEditFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
