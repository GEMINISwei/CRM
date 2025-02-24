<script setup lang="ts">
import { reactive } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

const couponNewFields = reactive<CustomFormField[]>([
  { label: '活動名稱', type: 'text', depValue: 'name', required: true },
  { label: '開始日期', type: 'date', depValue: 'start_time', required: true },
  { label: '結束日期', type: 'date', depValue: 'end_time', required: true },
  { label: '滿額條件', type: 'number', depValue: 'money_floor', required: true },
  { label: '贈送遊戲幣', type: 'float', depValue: 'coin_free', required: true },
])
const formData = reactive<DataObject>(couponNewFields.reduce((accu, curr) => {
  return {
    ...accu,
    [curr.depValue]: ''
  }
}, {}))
const formBtns: CustomFormButton[] = [
  { color: 'secondary', text: '返回', method: () => goPage('/coupons') },
  { color: 'primary', text: '新增', method: () => createCoupon(), needValid: true },
]

const createCoupon = (): void => {
  callApi('post', '/apis/coupons', formData)
    .then((resData: any) => {
      createNotify('success', `已建立 ${resData.name} 活動`)
      goPage('/coupons')
    })
    .catch((_: any) => {
      // if (err.status) {
      //   createNotify('error', '遊戲類別已存在 !')
      // }
    })
}
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">新增活動</h3>
    <CustomForm
      :fields="couponNewFields"
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>
