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
const formData = reactive<DataObject>(formFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: 0
  }
}, {}))
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
      for (let fieldIdx = 0; fieldIdx < formFields.length; fieldIdx++) {
        let depValue = formFields[fieldIdx].depValue

        formData[depValue] = resData['value'][depValue]
      }
    })
}
const updateAwardSetting = () => {
  if (awardTotalCount.value == maxCount) {
    let updateFormData = {
      collection_name: 'award',
      field: 'block',
      value: formData
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
    <span class="text-center">*** 需設定 12 個區塊 ***</span>
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
