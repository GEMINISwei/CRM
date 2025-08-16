<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { CustomFormField, DataObject, CustomFormButton } from '@/type'

const maxCount = 12
const minCount = 0

const formFields = reactive<CustomFormField[]>([
  { label: '頭獎', type: 'number', depValue: 'one_award', required: true, max: maxCount, min: minCount },
  { label: '二獎', type: 'number', depValue: 'two_award', required: true, max: maxCount, min: minCount },
  { label: '三獎', type: 'number', depValue: 'three_award', required: true, max: maxCount, min: minCount },
  { label: '未中獎', type: 'number', depValue: 'no_award', required: true, max: maxCount, min: minCount },
])
const nameFormFields = reactive<CustomFormField[]>([
  { label: '頭獎名稱', type: 'text', depValue: 'one_award_name' },
  { label: '二獎名稱', type: 'text', depValue: 'two_award_name' },
  { label: '三獎名稱', type: 'text', depValue: 'three_award_name' },
])

const formData = reactive<DataObject>(formFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: 0
  }
}, {}))
const formData2 = reactive<DataObject>({})
const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '設定', method: () => updateAwardSetting(), needValid: true },
  { color: 'secondary', text: '返回', method: () => goPage('/settings') },
]

const awardTotalCount = computed(() => {
  let resultCount = 0

  for (let fIdx = 0; fIdx < formFields.length; fIdx++) {
    let depValue = formFields[fIdx].depValue

    if (formData[depValue]) {
      resultCount += formData[depValue]
    }
  }

  return resultCount
})

const getAwardInfo = () => {
  callApi('get', '/apis/settings/award/block')
    .then((resData: any) => {
      formData['one_award'] = resData['value']['one_award']
      formData['two_award'] = resData['value']['two_award']
      formData['three_award'] = resData['value']['three_award']
      formData['no_award'] = resData['value']['no_award']

      formData2['one_award_name'] = resData['value']['one_award_name']
      formData2['two_award_name'] = resData['value']['two_award_name']
      formData2['three_award_name'] = resData['value']['three_award_name']
    })
}
const updateAwardSetting = () => {
  if (awardTotalCount.value == maxCount) {
    let finalFormData = Object.assign(formData, formData2)

    let updateFormData = {
      collection_name: 'award',
      field: 'block',
      value: finalFormData
    }

    callApi('patch', '/apis/set_settings', updateFormData)
      .then((_: any) => {
        getAwardInfo()
        createNotify('success', '更新設定成功')
      })
  } else {
    createNotify('error', `尚未設定 ${maxCount} 個區塊, 請確認 !!`)
  }
}

onMounted(() =>{
  getAwardInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">遊戲設定</h3>
    <span class="text-center">自定義獎項名稱</span>
    <CustomForm
      class="m-2"
      :fields="nameFormFields"
      :colSize="8"
      :colOffset="2"
      v-model:formData="formData2"
    />
    <span class="text-center">*** 獎項總數需設定 12 個區塊 ***</span>
    <CustomForm
      class="m-2"
      :fields="formFields"
      :colSize="8"
      :colOffset="2"
      :buttons="formBtns"
      v-model:formData="formData"
    />

  </div>
</template>
