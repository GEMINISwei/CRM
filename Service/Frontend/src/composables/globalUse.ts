import { ref, reactive, computed, watch } from 'vue'
import { DataObject, UserInfo } from '@/type'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { connectWebsocket, disconnectWebsocket } from '@/composables/websocket'

// Flag Use
const statusFlag = reactive<DataObject>({
  init: false,
  loading: false,
  modalShow: false,
  dataNeedUpdate: false,
})
const setStatusFlag = (flagName: string, status: boolean): void => {
  statusFlag[flagName] = status
}

// Page Parameters Pass Use
const pageParameters = reactive<DataObject>({})
const setPageParams = (page: string, params: DataObject): void => {
  pageParameters[page] = params
}
const deletePageParam = (page: string): void => {
  delete pageParameters[page]
}

// UserInfo Use
const onlineUsers = ref([])
const userIdleTime = ref(0)
const userIdleMax = ref(10 * 60)
const currentUser = reactive<UserInfo>({
  username: "",
  token: "",
  shift: '管理者',
  level: 99, // 最低權限
})

const setUser = (userInfo: UserInfo): void => {
  currentUser.username = userInfo.username
  currentUser.token = userInfo.token
  currentUser.level = userInfo.level
}
const initUser = (): void => {
  currentUser.username = ""
  currentUser.token = ""
  currentUser.level = 99
}
const setShift = (shift: string): void => {
  currentUser.shift = shift
}
const isLoginSuccess = computed<boolean>(() => {
  return currentUser?.token.length > 0
})

watch(isLoginSuccess, (newVal) => {
  if (newVal) {
    idleTimerEnable()
    window.addEventListener("mousedown", resetTimer)
    connectWebsocket()
  } else {
    disconnectWebsocket()
  }
})
watch(userIdleTime, (newVal) => {
  if (newVal > userIdleMax.value) {
    callApi("post", "/apis/users/logout", {
      username: currentUser.username
    })
      .then((_) => {
        initUser()
        resetTimer()
        window.removeEventListener("mousedown", resetTimer)
        createNotify("info", "閒置太久請重新登入 !")
      })
      .catch((_) => {
        createNotify("error", "異常錯誤 !")
      })

  }
})

const idleTimerEnable = () => {
  if (isLoginSuccess.value) {
    setTimeout(() => {
      userIdleTime.value++
      idleTimerEnable()
    }, 1000)
  }
}
const resetTimer = () => {
  userIdleTime.value = 0
}

export {
  // Flag Use
  statusFlag,
  setStatusFlag,

  // Page Parameters Pass Use
  pageParameters,
  setPageParams,
  deletePageParam,

  // UserInfo Use
  onlineUsers,
  userIdleTime,
  userIdleMax,
  currentUser,
  setUser,
  initUser,
  setShift,
  isLoginSuccess,
}
