<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const memberEditAccountsFields = reactive<CustomFormField[]>([])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/members') },
  { color: 'success', text: '新增', method: () => addAccountField() },
  { color: 'primary', text: '更新', method: () => updateMemberAccounts(), needValid: true },
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
      res.data.accounts.forEach((account: string, aIndex: number) => {
        addAccountField()
        formData[`accounts[${aIndex}]`] = account
      })
    })
}

const addAccountField = (): void => {
  let currCount = memberEditAccountsFields.length

  memberEditAccountsFields.push({ label: `銀行帳戶 #${currCount + 1}`, type: 'text', depValue: `accounts[${currCount}]` })
}

const updateMemberAccounts = () => {
  callApi('patch', `/apis/members/${currentEditId.value}/accounts`, setRequestData())
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
  let fieldsHasData = memberEditAccountsFields.filter((field: CustomFormField) => formData[field.depValue])

  resultObject['accounts'] = fieldsHasData.map((field: CustomFormField) => {
    return formData[field.depValue]
  })

  return resultObject
}

</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯銀行帳戶</h3>
    <CustomForm :fields="memberEditAccountsFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
