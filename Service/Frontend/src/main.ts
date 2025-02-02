import { createApp } from 'vue'
import { router } from '@/router'
import directive from '@/directive'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import App from '@/App.vue'
import '@/assets/scss/customVariables.scss'

const app = createApp(App)

app.use(directive)
app.use(router)
app.mount('#app')
