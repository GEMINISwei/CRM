<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap'
import { goPage } from '@/router'
import { updateDate, currentVersion } from '@/version-history'
import { userIdleTime, userIdleMax, currentUser, initUser, isLoginSuccess } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import { callApi } from '@/composables/api';

const htmlElems = reactive<any>({
  sidebar: null
})

const pageInfo = [
  { name: '遊戲管理', path: '/games' },
  { name: '會員管理', path: '/members' },
  { name: '資產管理', path: '/properties' },
  { name: '庫存管理', path: '/stocks' },
  { name: '交流單管理', path: '/trades/new' },
  { name: '媒合紀錄', path: '/matches' },
  { name: '活動管理', path: '/activities' },
  { name: '報表功能', path: '/reports' },
  { name: '系統設定', path: '/settings' },
  { name: '小遊戲', path: '/award' },
]

const shiftText = computed(() => {
  let resultText = ''

  switch (currentUser.shift) {
    case 'admin':
      resultText = '管理者'
      break

    case 'day_class':
      resultText = '早班'
      break

    case 'night_class':
      resultText = '晚班'
      break
  }

  return resultText
})

onMounted(() => {
  let sidebarElem = document.querySelector('#sidebar')

  htmlElems.sidebar = new Offcanvas(sidebarElem)
})

const logout = () => {
  callApi("post", "/apis/users/logout", {
    username: currentUser.username
  })
    .then((_) => {
      htmlElems.sidebar.hide()
      initUser()
      goPage("/")
      createNotify("success", "登出成功 !")
    })
    .catch((_) => {
      createNotify("error", "登出失敗 !")
    })
}
</script>

<template>
  <nav class="navbar navbar-dark bg-body-tertiary flex-nowrap">
    <div id="menu-bar" class="container-fluid">
      <button v-show="isLoginSuccess" class="navbar-toggler" @click="htmlElems.sidebar.show()">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>
    <div v-show="isLoginSuccess" class="container-fluid justify-content-end">
      <span class="navbar-brand">Hi, {{ currentUser.username }} ({{ shiftText }})</span>
      <span class="mx-2">剩餘時間: {{ userIdleMax - userIdleTime }} 秒</span>
      <!-- <button class="btn btn-secondary" @click="chagneShift()">切換身分</button> -->
      <!-- <button class="btn btn-secondary mx-3" @click="test()">測試</button> -->
    </div>
  </nav>

  <div id="sidebar" class="offcanvas offcanvas-start">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title">頁面清單</h5>
      <button class="btn-close" @click="htmlElems.sidebar.hide()"></button>
    </div>
    <div class="offcanvas-body">
      <div class="container">
        <div v-for="page in pageInfo" :key="page.name" class="mx-3 p-2">
          <span role="button" @click="goPage(page.path); htmlElems.sidebar.hide()">
            {{ page.name }}
          </span>
        </div>
        <button id="logout-btn" class="btn btn-secondary mx-3" @click="logout()">登出</button>
        <button id="finish-btn" class="btn btn-success mx-3" @click="() => {}">結帳</button>
        <span id="version-text">Updated: {{ updateDate }} (Ver {{ currentVersion }})</span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#menu-bar {
  min-height: 40px;
}
#logout-btn {
  position: absolute;
  bottom: 20px;
  left: 5px;
}
#finish-btn {
  position: absolute;
  bottom: 20px;
  left: 75px;
}
#version-text {
  position: absolute;
  bottom: 25px;
  right: 10px;
  color: gray;
}
</style>
