import { ref, reactive } from "vue"

const updateDate = ref("2025/04/09")
const version = ref("0.1.4")
const history = reactive({
  "2025/03/30": [
    "系統設定 - 拆分為小項目各別調整"
  ],
  "2025/04/09": [
    "Bug Fixed"
  ]
})

export {
  updateDate,
  version,
  history,
}
