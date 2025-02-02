import { App, DirectiveBinding } from "vue"
import { Tooltip } from 'bootstrap'

// 新增驗證成功才執行的 Click 指令
const validClick = {
  mounted: (el: any, binding: DirectiveBinding) => {
    el.addEventListener('click', () => {
      let validResult: boolean = false
      let form: any = el.form

      if (form) {
        if (form.checkValidity()) {
          validResult = true
        }

        form.classList.add('was-validated')
      } else {
        console.log('Form not found.')
      }

      if (validResult == true) {
        binding.value()
      }
    })
  }
}

const tooltip = {
  mounted: (el: any, binding: DirectiveBinding) => {
    let tooltipObject = new Tooltip(el, {
      title: binding.value,
      customClass: 'custom-tooltip',
      trigger: 'hover manual'
    })

    el.addEventListener('click', () => {
      tooltipObject.hide()
    })
  }
}

export default {
  install: (app: App) => {
    app.directive('validClick', validClick)
    app.directive('tooltip', tooltip)
  }
}
