<script setup lang="ts">
import { reactive } from 'vue'
import { currentUser, setUser, isLoginSuccess } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormButton } from '@/type'

const loginFields = [
  { label: '帳號', type: 'text', depValue: 'username', required: true },
  { label: '密碼', type: 'password', depValue: 'password', required: true },
]
const formData = reactive<DataObject>({})
  const formBtns: CustomFormButton[] = [
  { color: 'primary', text: '登入', method: () => userLogin(), needValid: true },
]

const userLogin = (): void => {
  // 登入功能尚未設計, 先預設一個超級使用者
  if (formData.username == 'admin' && formData.password == 'admin123456') {
    setUser({
      id: 'Test_00000000',
      name: 'admin',
      level: 0,
    })

    createNotify('success', `使用者 "${currentUser.name}" 已登入`)
  } else {
    createNotify('error', `登入資訊有誤, 請重新輸入`)
  }
}
</script>

<template>
  <div id="home-page-body" class="container">
    <h2>Welcome to CRM system</h2>
    <div v-show="!isLoginSuccess" class="col-12 mt-4">
      <CustomForm :fields="loginFields" :buttons="formBtns" v-model:formData="formData" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#home-page-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
</style>
