<script setup lang="ts">
import { onMounted, reactive, watch } from 'vue';
import { Toast } from 'bootstrap';
import { notifyInfo, setNotifyMaxCount, removeNotify } from '@/composables/notify'

interface NotifyLayoutProps {
  showMax?: number,
}
interface ShowNotify {
  id: string,
  show: boolean,
  timeAgo: string,
  status: string,
  messages: string[],
  notifyElem: Element | null,
  bootstrapObject: any
}

const props = withDefaults(defineProps<NotifyLayoutProps>(), {
  showMax: 3,
})

const showNotifies = reactive<ShowNotify[]>(Array.from({ length: props.showMax },  () => {
  return {
    id: '',
    show: false,
    timeAgo: '',
    status: '',
    messages: [],
    notifyElem: null,
    bootstrapObject: {}
  }
}))

onMounted(() => {
  setNotifyMaxCount(props.showMax)

  for (let index = 0; index < props.showMax; index++) {
    let notifyElem = document.querySelector(`#notify-${index + 1}`)

    showNotifies[index].notifyElem = notifyElem
    showNotifies[index].bootstrapObject = new Toast(notifyElem)
  }
})

watch(notifyInfo, (newVal) => {
  showNotifies.forEach((notify: ShowNotify, index: number) => {
    if (!notify.show && index <= newVal.length - 1) {
      let matchedNotify = newVal.find(x => !showNotifies.filter(nt => nt.id != '').map(nt => nt.id).includes(x.id) )

      if (matchedNotify) {
        showNotifies[index].id = matchedNotify.id
        showNotifies[index].show = true
        showNotifies[index].timeAgo = getTimeDiff(matchedNotify.timeAt)
        showNotifies[index].status = matchedNotify.status
        showNotifies[index].messages = matchedNotify.msg
        showNotifies[index].bootstrapObject.show()

        showNotifies[index].notifyElem?.addEventListener('hidden.bs.toast', () => {
          clearNotify(index)
        })
      }
    }
  })
})

const getTimeDiff = (startTime: Date): string => {
  let timeStr = ''
  let nowTime = new Date()
  let timeDiff: number = (nowTime.getTime() - startTime.getTime())

  // 超過一分鐘
  if (timeDiff > 60000) {
    timeStr = `${Math.floor(timeDiff / 60000)} minutes ago`
  } else {
    timeStr = `${Math.floor(timeDiff / 1000)} seconds ago`
  }

  return timeStr
}

const clearNotify = (index: number): void => {
  removeNotify(showNotifies[index].id)
  showNotifies[index].id = ''
  showNotifies[index].show = false
  showNotifies[index].timeAgo = ''
  showNotifies[index].status = ''
  showNotifies[index].messages = []
}

const notifyClass = (status: string): string => {
  let classResult = 'm-2 status-circle'

  switch (status) {
    case 'success':
      classResult += ' bg-success'
      break

    case 'error':
      classResult += ' bg-danger'
      break

    default:
      classResult += ' bg-primary'
      break
  }

  return classResult
}
</script>

<template>
<div class="toast-container position-fixed bottom-0 start-0 p-3">
  <div
    v-for="(i, index) in props.showMax"
    :key="i"
    :id="`notify-${i}`"
    class="toast"
    role="alert"
    aria-live="assertive"
    aria-atomic="true"
  >
    <div class="toast-header">
      <div :class="notifyClass(showNotifies[index].status)"></div>
      <strong class="me-auto">Sysyem Message</strong>
      <small>{{ showNotifies[index].timeAgo }}</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      <p v-for="msg in showNotifies[index].messages" :key="msg" class="m-2">{{ msg }}</p>
    </div>
  </div>
</div>
</template>

<style lang="scss" scoped>
.status-circle {
  width: 8px;
  height: 8px;
  border-radius:999em;
}
</style>
