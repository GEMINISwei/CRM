import { ref, reactive } from 'vue'

interface NotifyInfo {
  id: string,
  status: string,
  msg: string[],
  timeAt: Date,
}

const notifyHistoryCount = ref(0)
const notifyMaxCount = ref(0)
const notifyInfo = reactive([] as NotifyInfo[])

const setNotifyMaxCount = (maxCount: number): void => {
  notifyMaxCount.value = maxCount
}

const createNotify = (status: string, msgs: string[] | string) => {
  let newNotify: NotifyInfo = {
    id: `notify-${notifyHistoryCount.value}`,
    status: '',
    msg: [],
    timeAt: new Date(),
  }

  if (Array.isArray(msgs)) {
    newNotify.status = status
    newNotify.msg = msgs
  } else {
    newNotify.status = status
    newNotify.msg = [msgs]
  }

  notifyInfo.push(newNotify)
  notifyHistoryCount.value += 1
}

const removeNotify = (id: string) => {
  let notifyIndex: number = notifyInfo.findIndex(x => x.id == id)

  if (notifyIndex != -1) {
    notifyInfo.splice(notifyIndex, 1)
  }
}

export {
  notifyInfo,
  setNotifyMaxCount,
  createNotify,
  removeNotify,
}
