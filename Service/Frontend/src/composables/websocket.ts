import { ref } from 'vue'
import { onlineUsers, currentUser } from '@/composables/globalUse'

const wsUrl = import.meta.env.VITE_WS_URL

const socket = ref<any>(null)
const retryFlag = ref(false)
const retryTimes = ref(0)

const connectWebsocket = () => {
    socket.value = new WebSocket(`${wsUrl}/ws/${currentUser.username}`);
    retryFlag.value = true

    socket.value.onmessage = (event: any) => {
      // console.log(event.data)
      onlineUsers.value = JSON.parse(event.data)
    }

    socket.value.onopen = () => {
      console.log("WebSocket Open")
      // sendWSMessage({
      //   login: {
      //     username: currentUser.username
      //   }
      // })
    }

    socket.value.onclose = () => {
      if (retryTimes.value == 0) {
        console.log("WebSocket Close")
      } else if (retryTimes.value == 3) {
        retryTimes.value = 0
        return
      }

      if (retryFlag.value == true && retryTimes.value < 3) {
        console.log(`WebSocket Connect Retry (${retryTimes.value + 1})...`)
        setTimeout(connectWebsocket, 3000);
        retryTimes.value = retryTimes.value + 1
      }
    }
}

const disconnectWebsocket = () => {
  retryFlag.value = false
  socket.value.close()
}

const sendWSMessage = (info: string | object) => {
  let messageType = typeof info
  if (messageType == "string") {
    socket.value.send(info)
  } else if (messageType == "object") {
    socket.value.send(JSON.stringify(info))
  }
}

export {
  onlineUsers,
  connectWebsocket,
  disconnectWebsocket,
  sendWSMessage,
}
