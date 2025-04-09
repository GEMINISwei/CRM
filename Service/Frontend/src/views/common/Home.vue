<script setup lang="ts">
import { reactive, watch } from 'vue'
import { currentUser, setUser, isLoginSuccess, setStatusFlag } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { history } from '@/version-history'
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

watch(isLoginSuccess, (newVal) => {
  if (newVal == true) {
    setStatusFlag("modalShow", true)
  }
})

const userLogin = (): void => {
  callApi("post", "/apis/users/login", formData)
    .then((resData: any) => {
      setUser({
        username: resData.username,
        token: resData.access_token,
        shift: resData.shift,
        level: 0,
      })

      formData.username = ""
      formData.password = ""

      createNotify('success', `使用者 "${currentUser.username}" 已登入`)
    })
    .catch(() => {
      createNotify('error', `登入資訊有誤, 請重新輸入`)
    })
}
</script>

<template>
  <div id="home-page-body" class="container">
    <h2>Welcome to CRM system</h2>
    <div v-show="!isLoginSuccess" class="col-12 mt-4">
      <CustomForm :fields="loginFields" :buttons="formBtns" v-model:formData="formData" />
    </div>
  </div>

  <Teleport to="#modal-header">
    <h3>Version History</h3>
  </Teleport>
  <Teleport to="#modal-body">
    <div v-for="updateItems, modifyDate in history" :key="modifyDate" class="update-block">
      <li>{{ modifyDate }}</li>
      <template v-for="(item, itemIndex) in updateItems" :key="itemIndex">
        <span>{{ itemIndex + 1 }}. {{ item }}</span>
        <br>
      </template>
    </div>
  </Teleport>
</template>

<style lang="scss" scoped>
#home-page-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
.update-block {
  margin: 0 0 20px 0;
}
</style>
