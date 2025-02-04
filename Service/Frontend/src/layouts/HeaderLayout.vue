<script setup lang="ts">
import { reactive, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap'
import { goPage } from '@/router'
import { currentUser, setShift, isLoginSuccess } from '@/composables/globalUse'

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
  { name: '活動管理', path: '/coupons' },
  { name: '報表功能', path: '/reports' },
  { name: '權限管理', path: '/permissions' },
  { name: '系統設定', path: '/settings' },
  { name: '小遊戲 Demo', path: '/test' },
]

onMounted(() => {
  let sidebarElem = document.querySelector('#sidebar')

  htmlElems.sidebar = new Offcanvas(sidebarElem)
})

const chagneShift = (): void => {
  if (currentUser.shift == '管理者') {
    setShift('早班')
  } else if (currentUser.shift == '早班') {
    setShift('晚班')
  } else if (currentUser.shift == '晚班') {
    setShift('管理者')
  }
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
      <span class="navbar-brand">Hi, {{ currentUser.name }} ({{ currentUser.shift }})</span>
      <button class="btn btn-secondary" @click="chagneShift()">切換身分</button>
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
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#menu-bar {
  min-height: 40px;
}
</style>
