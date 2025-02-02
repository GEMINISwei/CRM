<script lang="ts" setup>
import { reactive, computed, onMounted } from 'vue'
import { goPage } from '@/router'
import { pageParameters } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const memberEditSockPuppetsFields = reactive<CustomFormField[]>([])
const formData = reactive<DataObject>({})

const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/members') },
  { color: 'success', text: '新增', method: () => addSockPuppet() },
  { color: 'primary', text: '更新', method: () => updateMemberSockPuppets(), needValid: true },
]

const currentEditId = computed<string>(() => {
  return pageParameters['members']?.['editId']
})

onMounted(() => {
  if (currentEditId.value) {
    getMemberSockPuppets()
  } else {
    goPage('/members')
  }
})

const getMemberSockPuppets = () => {
  callApi('get', `/apis/members/${currentEditId.value}`)
    .then((res: any) => {
      res.data.sock_puppets.forEach((sockPuppet: string, aIndex: number) => {
        addSockPuppet()
        formData[`sock_puppets[${aIndex}]`] = sockPuppet
      })
    })
}

const addSockPuppet = (): void => {
  let currCount = memberEditSockPuppetsFields.length

  memberEditSockPuppetsFields.push({ label: `遊戲分身 #${currCount + 1}`, type: 'text', depValue: `sock_puppets[${currCount}]` })
}

const updateMemberSockPuppets = () => {
  callApi('patch', `/apis/members/${currentEditId.value}/sock_puppets`, setRequestData())
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
  let fieldsHasData = memberEditSockPuppetsFields.filter((field: CustomFormField) => formData[field.depValue])

  resultObject['sock_puppets'] = fieldsHasData.map((field: CustomFormField) => {
    return formData[field.depValue]
  })

  return resultObject
}

</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">編輯遊戲分身</h3>
    <CustomForm :fields="memberEditSockPuppetsFields" :buttons="formBtns" v-model:formData="formData" />
  </div>
</template>
