import { reactive, computed } from 'vue'
import { DataObject, UserInfo } from '@/type'

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
const currentUser = reactive<UserInfo>({
  id: '',
  name: '未登入',
  shift: '管理者',
  level: 99, // 最低權限
})
const setUser = (userInfo: UserInfo): void => {
  currentUser.id = userInfo.id
  currentUser.name = userInfo.name
  currentUser.level = userInfo.level
}
const setShift = (shift: string): void => {
  currentUser.shift = shift
}
const isLoginSuccess = computed<boolean>(() => {
  return currentUser.id ? true : false
})

export {
  // Flag Use
  statusFlag,
  setStatusFlag,

  // Page Parameters Pass Use
  pageParameters,
  setPageParams,
  deletePageParam,

  // UserInfo Use
  currentUser,
  setUser,
  setShift,
  isLoginSuccess,
}
