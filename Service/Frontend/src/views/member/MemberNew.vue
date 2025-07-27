<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { setStatusFlag } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'

const part = ref(1)

const sexOptions: OptionObject[] = [
  { text: '男', value: '男' },
  { text: '女', value: '女' },
]
const memberNewFields = reactive<CustomFormField[]>([
  { label: '遊戲類別', type: 'select', depValue: 'game_id', required: true },
  // { label: '遊戲暱稱', type: 'text', depValue: 'nickname', required: true },
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

const isMainOptions: OptionObject[] = [
  { text: '是', value: true },
  { text: '否', value: false },
]
const playerNewFields = reactive<CustomFormField[]>([
  { label: '暱稱', type: 'text', depValue: 'name', required: true },
  { label: '是否為主帳號', type: 'select', depValue: 'is_main', options: isMainOptions },
])
const formData2 = reactive<DataObject>({})
const formBtns2: CustomFormButton[] = [
  { color: 'primary', text: '新增', method: () => createPlayer(), needValid: true },
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

  callApi('post', '/apis/members', formData)
    .then((resData: any) => {
      createNotify('success', '會員新增成功')
      setStatusFlag('loading', false)

      formData2['member_id'] = resData.id
      formData2['is_main'] = true
      part.value = 2
      // goPage('/members')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}

const createPlayer = (): void => {
  setStatusFlag('loading', true)

  callApi('post', '/apis/players', formData2)
    .then((resData: any) => {
      createNotify('success', `遊戲帳號 "${resData.name}" 新增成功`)
      setStatusFlag('loading', false)
      goPage('/members')
    })
    .catch(() => {
      setStatusFlag('loading', false)
    })
}
</script>

<template>
  <div class="container">
    <template v-if="part == 1">
      <h3 class="m-4 text-center">新增會員</h3>
      <CustomForm :fields="memberNewFields" :buttons="formBtns" v-model:formData="formData" />
    </template>
    <template v-else-if="part == 2">
      <h3 class="m-4 text-center">新增遊戲帳號</h3>
      <CustomForm :fields="playerNewFields" :buttons="formBtns2" v-model:formData="formData2" />
    </template>
  </div>
</template>
