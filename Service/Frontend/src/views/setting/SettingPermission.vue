<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { callApi } from '@/composables/api'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataObject, FuncListItem } from '@/type'
import { goPage } from '@/router'

const allPermissions = ref<DataObject>({})

const functionList: FuncListItem[] = [
  { text: '新增權限群組', icon: 'plus-square', goPath: '/settings/permission/new' },
  { text: '新增使用者', icon: 'plus-square', goPath: '/settings/user/new' },
]

const getPermissionInfo = () => {
  callApi('get', '/apis/settings/permission/all')
    .then((resData: any) => {
      allPermissions.value = resData['value']
    })
}

const editPermission = (levelGroup: any) => {
  goPage('/settings/permission/edit', {
    levelGroup: levelGroup
  })
}

onMounted(() => {
  getPermissionInfo()
})
</script>

<template>
  <div class="container">
    <h3 class="m-4 text-center">使用權限設定</h3>

    <div
      v-for="(_, levelGroup) in allPermissions"
      :key="levelGroup"
      class="border rounded my-3 p-3 d-flex flex-row justify-content-center"
    >
      <div class="w-50 px-5 d-flex">
        <span class="align-self-center">{{ levelGroup }}</span>
      </div>
      <div class="w-50 mx-3 d-flex flex-row justify-content-end">
        <button class="btn btn-primary" @click="editPermission(levelGroup)">編輯群組</button>
      </div>
    </div>
  </div>

  <FunctionBall :functionList />
</template>
