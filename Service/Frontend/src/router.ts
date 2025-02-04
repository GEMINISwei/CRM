import { createRouter, createWebHistory } from 'vue-router'
import { statusFlag, pageParameters, deletePageParam, isLoginSuccess, setPageParams } from '@/composables/globalUse'
import { DataObject } from '@/type'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/common/Home.vue')
    },
    {
      path: '/games',
      name: 'GameList',
      component: () => import('@/views/game/Game.vue')
    },
    {
      path: '/games/new',
      name: 'GameNew',
      component: () => import('@/views/game/GameNew.vue')
    },
    {
      path: '/games/edit',
      name: 'GameEdit',
      component: () => import('@/views/game/GameEdit.vue')
    },
    {
      path: '/members',
      name: 'MemberList',
      component: () => import('@/views/member/Member.vue')
    },
    {
      path: '/members/new',
      name: 'MemberNew',
      component: () => import('@/views/member/MemberNew.vue')
    },
    {
      path: '/members/edit',
      name: 'MemberEdit',
      component: () => import('@/views/member/MemberEdit.vue')
    },
    {
      path: '/members/edit_accounts',
      name: 'MemberEditAccounts',
      component: () => import('@/views/member/MemberEditAccounts.vue')
    },
    {
      path: '/members/edit_sock_puppets',
      name: 'MemberEditSockPuppets',
      component: () => import('@/views/member/MemberEditSockPuppets.vue')
    },
    {
      path: '/members/edit_phones',
      name: 'MemberEditPhones',
      component: () => import('@/views/member/MemberEditPhones.vue')
    },
    {
      path: '/properties',
      name: 'PropertyList',
      component: () => import('@/views/property/Property.vue')
    },
    {
      path: '/properties/new',
      name: 'PropertyNew',
      component: () => import('@/views/property/PropertyNew.vue')
    },
    {
      path: '/properties/details',
      name: 'PropertyDetail',
      component: () => import('@/views/property/PropertyDetail.vue')
    },
    {
      path: '/stocks',
      name: 'StockList',
      component: () => import('@/views/stock/Stock.vue')
    },
    {
      path: '/stocks/new',
      name: 'StockNew',
      component: () => import('@/views/stock/StockNew.vue')
    },
    {
      path: '/stocks/details',
      name: 'StockDetail',
      component: () => import('@/views/stock/StockDetail.vue')
    },
    {
      path: '/trades/new',
      name: 'TradeNew',
      component: () => import('@/views/trade/TradeNew.vue')
    },
    {
      path: '/trades/edit',
      name: 'TradeEdit',
      component: () => import('@/views/trade/TradeEdit.vue')
    },
    {
      path: '/matches',
      name: 'MatchList',
      component: () => import('@/views/match/Match.vue')
    },
    {
      path: '/coupons',
      name: 'CouponList',
      component: () => import('@/views/coupon/Coupon.vue')
    },
    {
      path: '/coupons/new',
      name: 'CouponNew',
      component: () => import('@/views/coupon/CouponNew.vue')
    },
    {
      path: '/reports',
      name: 'Report',
      component: () => import('@/views/report/Report.vue')
    },
    {
      path: '/permissions',
      name: 'Permission',
      component: () => import('@/views/permission/Permission.vue')
    },
    {
      path: '/settings',
      name: 'Setting',
      component: () => import('@/views/common/Setting.vue')
    },
    {
      path: '/test',
      name: 'Test',
      component: () => import('@/views/common/Test.vue')
    },
    {
      path: '/not_found',
      name: 'NotFound',
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
  if (!isLoginSuccess.value && to.name != 'Home') {
    return { name: 'Home' }
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
