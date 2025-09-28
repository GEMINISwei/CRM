import { createRouter, createWebHistory } from 'vue-router'
import { statusFlag, pageParameters, deletePageParam, isLoginSuccess, setPageParams } from '@/composables/globalUse'
import { DataObject } from '@/type'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      meta: { requiresAuth: false },
      component: () => import('@/views/common/Home.vue')
    },
    {
      path: '/games',
      name: 'GameList',
      meta: { requiresAuth: true },
      component: () => import('@/views/game/Game.vue')
    },
    {
      path: '/games/new',
      name: 'GameNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/game/GameNew.vue')
    },
    {
      path: '/games/edit',
      name: 'GameEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/game/GameEdit.vue')
    },
    {
      path: '/staffs',
      name: 'StaffList',
      meta: { requiresAuth: true },
      component: () => import('@/views/staff/Staff.vue')
    },
    {
      path: '/members',
      name: 'MemberList',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/Member.vue')
    },
    {
      path: '/members/new',
      name: 'MemberNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberNew.vue')
    },
    {
      path: '/members/edit',
      name: 'MemberEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberEdit.vue')
    },
    {
      path: '/members/edit_accounts',
      name: 'MemberEditAccounts',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberEditAccounts.vue')
    },
    {
      path: '/members/edit_phones',
      name: 'MemberEditPhones',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberEditPhones.vue')
    },
    {
      path: '/members/add_player',
      name: 'MemberAddPlayer',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberAddPlayer.vue')
    },
    {
      path: '/members/player_record',
      name: 'MemberPlayerRecord',
      meta: { requiresAuth: true },
      component: () => import('@/views/member/MemberPlayerRecord.vue')
    },
    {
      path: '/properties',
      name: 'PropertyList',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/Property.vue')
    },
    {
      path: '/properties/new',
      name: 'PropertyNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/PropertyNew.vue')
    },
    {
      path: '/properties/edit',
      name: 'PropertyEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/PropertyEdit.vue')
    },
    {
      path: '/properties/details',
      name: 'PropertyDetail',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/PropertyDetail.vue')
    },
    {
      path: '/properties/daily_list/supermarket',
      name: 'SupermarketDailyList',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/SupermarketDailyList.vue')
    },
    {
      path: '/properties/daily_list/v_account',
      name: 'VirtaulAccountDailyList',
      meta: { requiresAuth: true },
      component: () => import('@/views/property/VirtaulAccountDailyList.vue')
    },
    {
      path: '/split_trades',
      name: 'SplitTrade',
      meta: { requiresAuth: true },
      component: () => import('@/views/split_trade/SplitTrade.vue')
    },
    {
      path: '/stocks',
      name: 'StockList',
      meta: { requiresAuth: true },
      component: () => import('@/views/stock/Stock.vue')
    },
    {
      path: '/stocks/new',
      name: 'StockNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/stock/StockNew.vue')
    },
    {
      path: '/stocks/edit',
      name: 'StockEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/stock/StockEdit.vue')
    },
    {
      path: '/trades/new',
      name: 'TradeNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/trade/TradeNew.vue')
    },
    {
      path: '/trades/edit',
      name: 'TradeEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/trade/TradeEdit.vue')
    },
    {
      path: '/matches',
      name: 'MatchList',
      meta: { requiresAuth: true },
      component: () => import('@/views/match/Match.vue')
    },
    {
      path: '/activities',
      name: 'ActivityList',
      meta: { requiresAuth: true },
      component: () => import('@/views/activity/Activity.vue')
    },
    {
      path: '/activities/new',
      name: 'ActivityNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/activity/ActivityNew.vue')
    },
    {
      path: '/activities/edit',
      name: 'ActivityEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/activity/ActivityEdit.vue')
    },
    {
      path: '/reports',
      name: 'Report',
      meta: { requiresAuth: true },
      component: () => import('@/views/report/Report.vue')
    },
    {
      path: '/settings',
      name: 'Setting',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/Setting.vue')
    },
    {
      path: '/settings/communicate_way',
      name: 'SettingCommunicateWay',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingCommunicateWay.vue')
    },
    {
      path: '/settings/fee',
      name: 'SettingFee',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingFee.vue')
    },
    {
      path: '/settings/color',
      name: 'SettingColor',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingColor.vue')
    },
    {
      path: '/settings/online',
      name: 'SettingOnline',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingOnline.vue')
    },
    {
      path: '/settings/permission',
      name: 'SettingPermission',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingPermission.vue')
    },
    {
      path: '/settings/permission/new',
      name: 'SettingPermissionNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingPermissionNew.vue')
    },
    {
      path: '/settings/permission/edit',
      name: 'SettingPermissionEdit',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingPermissionEdit.vue')
    },
    {
      path: '/settings/user/new',
      name: 'SettingUserNew',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingUserNew.vue')
    },
    {
      path: '/settings/award',
      name: 'SettingAward',
      meta: { requiresAuth: true },
      component: () => import('@/views/setting/SettingAward.vue')
    },
    {
      path: '/checkout',
      name: 'Checkout',
      meta: { requiresAuth: true },
      component: () => import('@/views/common/Checkout.vue')
    },
    {
      path: '/award',
      name: 'Award',
      meta: { requiresAuth: false },
      component: () => import('@/views/common/Award.vue')
    },
    {
      path: '/link_invalid',
      name: 'LinkInvalid',
      meta: { requiresAuth: false },
      component: () => import('@/views/common/LinkInvalid.vue')
    },
    {
      path: '/not_found',
      name: 'NotFound',
      meta: { requiresAuth: false },
      component: () => import('@/views/common/NotFound.vue')
    },
    {
      // 為匹配的路徑通通轉到 Not Found Page
      path: '/:catchAll(.*)',
      redirect: '/not_found'
    },
  ]
})

const delayTime = (ms: number) => {
  return new Promise((resolve: any) => {
    setTimeout(() => {
      resolve()
    }, ms)
  })
}

router.beforeEach(async (to) => {
  while (statusFlag['init'] == false) {
    await delayTime(10)
  }

  // 未登入且跳轉至非首頁畫面時, 導回首頁
  if (to.meta['requiresAuth'] == true) {
    if (!isLoginSuccess.value && to.name != 'Home') {
      return { name: 'Home' }
    }
  }
})

// 提供全域使用的 Method
const goPage = (pagePath: string, pageParams?: DataObject): void => {
  let pageBelong = pagePath.split('/')[1]

  if (pageParams) {
    setPageParams(pageBelong, { ...pageParameters[pageBelong], ...pageParams })
  }

  Object.keys(pageParameters).forEach((page: string) => {
    if (pageBelong != page) {
      deletePageParam(page)
    }
  })

  router.push({ path: pagePath })
}

export {
  router,
  goPage
}
