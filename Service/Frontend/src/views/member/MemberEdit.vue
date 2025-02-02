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
  { label: '首次交流時間', type: 'date', depValue: 'f_communication_time' },
  { label: '交流方式', type: 'select', depValue: 'f_communication_way' },
  { label: '首次交易金額', type: 'text', depValue: 'f_communication_amount' },
  { label: '註解', type: 'textarea', depValue: 'description' },
])
const formData = reactive<DataObject>(memberEditFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))

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
    .then((res: any) => {
      memberEditFields.forEach((field: DataObject) => {
        let fieldValue = ''

        if (field.depValue == 'f_communication_time') {
          if (res.data[field.depValue]) {
            fieldValue = res.data[field.depValue].slice(0, 10)
          }
        } else {
          fieldValue = res.data[field.depValue]
        }

        formData[field.depValue] = fieldValue
      })
    })
}

const getCommWayOptions = (): void => {
  callApi('get', '/apis/settings?collection_name=members')
      .then((res: any) => {
        let commWayFieldIndex = memberEditFields.findIndex((field: CustomFormField) => field.depValue == 'f_communication_way')

        memberEditFields[commWayFieldIndex].options = res.data['communication_ways'].map((x: any) => {
          return {
            text: x,
            value: x,
          }
        })
      })
}

const updateMember = () => {
  callApi('patch', `/apis/members/${currentEditId.value}`, formData)
    .then((res: any) => {
      createNotify('success', res.message)
      goPage('/members')
    })
    .catch((err: any) => {
      createNotify('error', err.message)
    })
}

const deleteMember = () => {
  callApi('delete', `/apis/members/${currentEditId.value}`)
    .then((res: any) => {
      createNotify('success', `會員 "${res.data.game_name}" 已刪除 !`)
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
