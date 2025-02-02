<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const memberEditPhonesFields = reactive<CustomFormField[]>([])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/members') },
  { color: 'success', text: '新增', method: () => addPhoneField() },
  { color: 'primary', text: '更新', method: () => updateMemberPhones(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['members']?.['editId']
})

onMounted(() => {
  if (currentEditId.value) {
    getMemberAccounts()
  } else {
    goPage('/members')
  }
})

const getMemberAccounts = () => {
  callApi('get', `/apis/members/${currentEditId.value}`)
    .then((res: any) => {
      res.data.phones.forEach((phone: string, aIndex: number) => {
        addPhoneField()
        formData[`phones[${aIndex}]`] = phone
      })
    })
}

const addPhoneField = (): void => {
  let currCount = memberEditPhonesFields.length

  memberEditPhonesFields.push({ label: `電話/手機號碼 #${currCount + 1}`, type: 'text', depValue: `phones[${currCount}]` })
}

const updateMemberPhones = () => {
  callApi('patch', `/apis/members/${currentEditId.value}/phones`, setRequestData())
    .then((res: any) => {
      createNotify('success', res.message)
      goPage('/members')
    })
    .catch((err: any) => {
      createNotify('error', err.message)
    })
}

const setRequestData = (): DataObject => {
  let resultObject: DataObject = {}
  let fieldsHasData = memberEditPhonesFields.filter((field: CustomFormField) => formData[field.depValue])

  resultObject['phones'] = fieldsHasData.map((field: CustomFormField) => {
    return formData[field.depValue]
  })

  return resultObject
}

</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯電話 / 手機號碼</h3>
    <CustomForm :fields="memberEditPhonesFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
