<script lang="ts" setup>
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { setStatusFlag } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const sexOptions: OptionObject[] = [
  { text: '男', value: '男' },
  { text: '女', value: '女' },
]
const memberNewFields = reactive<CustomFormField[]>([
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true },
  { label: '遊戲暱稱', type: 'text', depValue: 'nickname', required: true },
  { label: '性別', type: 'select', depValue: 'sex', options: sexOptions },
  { label: '首次交流時間', type: 'date', depValue: 'first_communication_time' },
  { label: '首次交流方式', type: 'select', depValue: 'first_communication_way' },
  { label: '首次交易金額', type: 'text', depValue: 'first_communication_amount' },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/members') },
  { color: 'primary', text: '新增', method: () => createUser(), needValid: true },
]

onMounted(() => {
  getGameOptions()
  getCommWayOptions()
})

const getGameOptions = (): void => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      let gameFieldIndex = memberNewFields.findIndex((field: CustomFormField) => field.depValue == 'game_id')

      memberNewFields[gameFieldIndex].options = resData.list_data.map((x: any) => {
        return {
          text: x['name'],
          value: x['id'],
        }
      })
    })
}
const getCommWayOptions = (): void => {
  callApi('get', '/apis/settings/member/communication_way')
      .then((resData: any) => {
        let commWayFieldIndex = memberNewFields.findIndex((field: CustomFormField) => {
          return field.depValue == 'first_communication_way'
        })

        let communicationWays = resData['value'].map((x: any) => {
          return {
            text: x,
            value: x
          }
        })

        memberNewFields[commWayFieldIndex].options = communicationWays
      })
}

const createUser = (): void => {
  setStatusFlag('loading', true)

  callApi('post', '/apis/members', requestDataSpecialRule())
    .then((resData: any) => {
      createNotify('success', `會員 "${resData.nickname}" 新增成功`)
      setStatusFlag('loading', false)
      goPage('/members')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}

const requestDataSpecialRule = (): DataObject => {
  let dataResult: DataObject = {}

  Object.keys(formData).forEach((fieldName: string) => {
    if (formData[fieldName] != '') {
      dataResult[fieldName] = formData[fieldName]
    }

    // Special Rule
    if (fieldName == 'sock_puppets') {
      dataResult[fieldName] = formData[fieldName].split(',').map((str: string) => str.trim())
    }
  })

  return dataResult
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增會員</h3>
    <CustomForm :fields="memberNewFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
