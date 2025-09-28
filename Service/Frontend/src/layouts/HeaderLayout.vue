<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap'
import { goPage } from '@/router'
import { updateDate, currentVersion } from '@/version-history'
import { userIdleTime, userIdleMax, currentUser, initUser, isLoginSuccess } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import { callApi } from '@/composables/api';
import { DataObject } from '@/type';

const htmlElems = reactive<any>({
  sidebar: null
})

const pageInfo = ref([
  { name: '遊戲管理', path: '/games', dep_permission: 'game_page' },
  { name: '會員管理', path: '/members', dep_permission: 'member_page' },
  { name: '資產管理', path: '/properties', dep_permission: 'property_page' },
  { name: '拆帳管理', path: '/split_trades', dep_permission: 'property_page' },
  { name: '庫存管理', path: '/stocks', dep_permission: 'stock_page' },
  { name: '交流單管理', path: '/trades/new', dep_permission: 'trade_page' },
  { name: '活動管理', path: '/activities', dep_permission: 'activity_page' },
  { name: '員工管理', path: '/staffs', dep_permission: 'staff_page' },
  { name: '系統設定', path: '/settings', dep_permission: 'setting_page' },
  // { name: '媒合紀錄', path: '/matches' },
  { name: '報表功能', path: '/reports' },
])

const showPageInfo = computed(() => {
  return pageInfo.value.filter((pageInfo: DataObject) => {
    let isShow = currentUser.level_group == 'Admin' ? true : false

    if (currentUser.permissions[pageInfo.dep_permission] == 'Y') {
      isShow = true
    }

    return isShow
  })
})

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

const checkoutTrade = (mode: string) => {
  goPage('/checkout', {
    mode: mode
  })
  htmlElems.sidebar.hide()
}

onMounted(() => {
  let sidebarElem = document.querySelector('#sidebar')

  htmlElems.sidebar = new Offcanvas(sidebarElem)
})
</script>

<template>
  <nav class="navbar navbar-dark bg-body-tertiary flex-nowrap">
    <div id="menu-bar" class="container-fluid">
      <button v-show="isLoginSuccess" class="navbar-toggler" @click="htmlElems.sidebar.show()">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>
    <div v-show="isLoginSuccess" class="container-fluid justify-content-end">
      <span class="navbar-brand">Hi, {{ currentUser.nickname }} ({{ shiftText }})</span>
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
        <div v-for="page in showPageInfo" :key="page.name" class="mx-3 p-2">
          <span role="button" @click="goPage(page.path); htmlElems.sidebar.hide()">
            {{ page.name }}
          </span>
        </div>
        <div id="finish-btns">
          <template v-if="currentUser.shift == 'day_class'">
            <button class="btn btn-success mx-2" @click="() => checkoutTrade('day')">結帳</button>
          </template>
          <template v-else-if="currentUser.shift == 'night_class'">
            <button class="btn btn-success mx-2" @click="() => checkoutTrade('night-1')">當日結帳</button>
            <button class="btn btn-success mx-2" @click="() => checkoutTrade('night-2')">跨日結帳</button>
          </template>
        </div>
        <div id="sidebar-footer">
          <button class="btn btn-secondary mx-2" @click="logout()">登出</button>
          <span class="mx-4">Updated: {{ updateDate }} (Ver {{ currentVersion }})</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#menu-bar {
  min-height: 40px;
}
#finish-btns {
  position: absolute;
  bottom: 70px;
  left: 20px;
}
#sidebar-footer {
  position: absolute;
  bottom: 20px;
  left: 20px;
}
</style>
