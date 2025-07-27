<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton, OptionObject } from '@/type'

const isMainOptions: OptionObject[] = [
  { text: '是', value: true },
  { text: '否', value: false },
]
const memberAddPlayerFields = reactive<CustomFormField[]>([
  { label: '遊戲名稱', type: 'text', depValue: 'name' },
  { label: '是否為主帳號', type: 'select', depValue: 'is_main', options: isMainOptions, disabled: true },
])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/members') },
  { color: 'success', text: '新增', method: () => addPlayer() },
]

const currentEditId = computed<string>(() => {
  return pageParameters['members']?.['editId']
})

onMounted(() => {
  if (currentEditId.value) {
    // getMemberSockPuppets()
  } else {
    goPage('/members')
  }
})

const addPlayer = () => {
  formData['member_id'] = currentEditId.value
  formData['is_main'] = false

  callApi('post', '/apis/players', formData)
    .then((_: any) => {
      createNotify('success',  '已新增遊戲帳號 !')
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
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯遊戲分身</h3>
    <CustomForm :fields="memberAddPlayerFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
