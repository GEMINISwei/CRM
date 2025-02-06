<script setup lang="ts">
import { reactive, watch } from 'vue'
import { currentUser, setUser, isLoginSuccess, setStatusFlag } from '@/composables/globalUse'
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

const versionHistory = reactive({
  "2025/02/05": [
    "新增側邊欄連結畫面 (待更新也顯示)"
  ],
  "2025/02/06": [
    "側邊欄底部新增版號及最後更新日期",
    "登入完成後跳出近期更新項目"
  ]
})

watch(isLoginSuccess, (newVal) => {
  if (newVal == true) {
    setStatusFlag("modalShow", true)
  }
})

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

  <Teleport to="#modal-header">
    <h3>Version History</h3>
  </Teleport>
  <Teleport to="#modal-body">
    <div v-for="updateItems, modifyDate in versionHistory" :key="modifyDate" class="update-block">
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
