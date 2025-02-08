<script setup lang="ts">
import { onMounted } from 'vue'
import { pageParameters, setPageParams, currentUser, setUser, setStatusFlag } from './composables/globalUse'
import HeaderLayout from '@/layouts/HeaderLayout.vue'
import ModalLayout from '@/layouts/ModalLayout.vue'
import NotifyLayout from '@/layouts/NotifyLayout.vue'
import LoadingLayout from '@/layouts/LoadingLayout.vue'
import { callApi } from '@/composables/api'

onMounted(() => {
  setStatusFlag('init', false)
  	window.addEventListener('beforeunload', () => {
      callApi("post", "/apis/users/logout", {
        username: currentUser.username
      })
    })

  // 不將資訊暴露到 Url 上的處理
  window.addEventListener('beforeunload', () => {
    // Page Use Parameters
    Object.keys(pageParameters).forEach((key: string) => {
      window.sessionStorage.setItem(key, JSON.stringify(pageParameters[key]))
    })

    // UserInfo Use Parameters
    window.sessionStorage.setItem('userInfo', JSON.stringify(currentUser))
  })
  window.addEventListener('load', () => {
    // Page Use Parameters
    Object.keys(window.sessionStorage).forEach((page: string) => {
      // 只處理 UserInfo 以外的資訊
      if (page != 'userInfo') {
        let sessionValue: string | null = window.sessionStorage.getItem(page)

        if (sessionValue) {
          let params = JSON.parse(sessionValue)

          if (params) {
            setPageParams(page, params)
          }
        }

        window.sessionStorage.removeItem(page)
      }
    })

    // UserInfo Use Parameters
    let sessionValue: string | null = window.sessionStorage.getItem('userInfo')

    if (sessionValue) {
      setUser(JSON.parse(sessionValue))
      window.sessionStorage.removeItem('userInfo')
    }

    setStatusFlag('init', true)
  })

})
</script>

<template>
  <HeaderLayout />
  <RouterView />
  <NotifyLayout />
  <ModalLayout />
  <LoadingLayout />
</template>
