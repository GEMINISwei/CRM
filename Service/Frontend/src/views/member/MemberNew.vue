<script lang="ts" setup>
import { reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { setStatusFlag } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton, FuncListItem } from '@/type'

const sexOptions: OptionObject[] = [
  { text: '男', value: '男' },
  { text: '女', value: '女' },
]
const memberNewFields = reactive<CustomFormField[]>([
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true },
  { label: '遊戲暱稱', type: 'text', depValue: 'nickname', required: true },
  { label: '性別', type: 'select', depValue: 'sex', options: sexOptions },
  { label: '首次交流時間', type: 'date', depValue: 'f_communication_time' },
  { label: '首次交流方式', type: 'select', depValue: 'f_communication_way' },
  { label: '首次交易金額', type: 'text', depValue: 'f_communication_amount' },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'success', text: '返回', method: () => goPage('/members') },
  { color: 'primary', text: '新增', method: () => createUser(), needValid: true },
]

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增交流方式', icon: 'plus-square', method: () => setStatusFlag('modalShow', true) },
]

const CommunicationWayNewFields = reactive<CustomFormField[]>([
  { label: '交流方式', type: 'text', depValue: 'communication_ways', required: true },
])
const commWayformData = reactive<DataObject>(CommunicationWayNewFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const commWayformBtns: CustomFormButton[] = [
  { color: 'primary', text: '新增', method: () => addCommWay(), needValid: true },
]

const addCommWay = () => {
  let requestData = {
    collection_name: 'members',
    update_type: 'push',
    field_name: 'communication_ways',
    field_value: commWayformData['communication_ways'],
  }


  console.log(requestData)
  callApi('patch', '/apis/settings', requestData)
    .then(() => {
      getCommWayOptions()
      setStatusFlag('modalShow', false)
    })
}

onMounted(() => {
  getGameOptions()
  getCommWayOptions()
})

const getGameOptions = (): void => {
  callApi('get', '/apis/games')
    .then((res: any) => {
      let gameFieldIndex = memberNewFields.findIndex((field: CustomFormField) => field.depValue == 'game_id')

      memberNewFields[gameFieldIndex].options = res.data.map((x: any) => {
        return {
          text: x['name'],
          value: x['id'],
        }
      })
    })
}
const getCommWayOptions = (): void => {
  callApi('get', '/apis/settings?collection_name=members')
      .then((res: any) => {
        let commWayFieldIndex = memberNewFields.findIndex((field: CustomFormField) => field.depValue == 'f_communication_way')

        memberNewFields[commWayFieldIndex].options = res.data['communication_ways'].map((x: any) => {
          return {
            text: x,
            value: x,
          }
        })
      })
}

const createUser = (): void => {
  setStatusFlag('loading', true)

  callApi('post', '/apis/members', requestDataSpecialRule())
    .then((res: any) => {
      createNotify('success', `會員 "${res.data.nickname}" 新增成功`)
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

  console.log(dataResult)

  return dataResult
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增會員</h3>
    <CustomForm :fields="memberNewFields" :buttons="formBtns" v-model:formData="formData" />

    <FunctionBall :functionList />
  </div>

  <Teleport to="#modal-header">
    <h2>新增交流方式</h2>
  </Teleport>
  <Teleport to="#modal-body">
    <CustomForm
      :fields="CommunicationWayNewFields"
      :colSize="12"
      :colOffset="0"
      :buttons="commWayformBtns"
      v-model:formData="commWayformData"
    />
  </Teleport>
</template>
