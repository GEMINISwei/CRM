<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { CustomFormField, DataObject, CustomFormButton } from '@/type'


const fomFields = reactive<CustomFormField[]>([
  { label: '交流方式', type: 'text', depValue: 'communication_way', required: true },
])
const formData = reactive<DataObject>(fomFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '新增', method: () => addCommunicateWay(), needValid: true },
  { color: 'danger', text: '刪除', method: () => deleteCommunicateWay(), needValid: true },
  { color: 'secondary', text: '返回', method: () => goPage('/settings') },
]
const communicateWayList = ref<string[]>([])

const getCommunicateWayList = (): void => {
  callApi('get', '/apis/settings/member/communication_way')
    .then((resData: any) => {
      communicateWayList.value = resData['value']
    })
}
const addCommunicateWay = () => {
  let addFormData = {
    collection_name: 'member',
    field: 'communication_way',
    value: formData["communication_way"]
  }

  callApi('patch', '/apis/add_settings', addFormData)
    .then(() => {
      formData["communication_way"] = ""
      getCommunicateWayList()
      createNotify('success', '新增設定成功')
    })
}
const deleteCommunicateWay = () => {
  let deleteFormData = {
    collection_name: 'member',
    field: 'communication_way',
    value: formData["communication_way"]
  }

  callApi('delete', '/apis/delete_settings', deleteFormData)
    .then(() => {
      formData["communication_way"] = ""
      getCommunicateWayList()
      createNotify('success', '刪除設定成功')
    })
}

onMounted(() => {
  getCommunicateWayList()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">交流方式設定</h3>
    <div class="border rounded">
      <CustomForm
        class="m-2"
        :fields="fomFields"
        :colSize="12"
        :colOffset="0"
        :buttons="formBtns"
        v-model:formData="formData"
      />
    </div>
    <div class="container">
      <h3 class="m-4 text-center">交流方式列表</h3>
      <li class="text-center m-2" v-for="commWay in communicateWayList">{{ commWay }}</li>
    </div>
  </div>
</template>
