import { ref, reactive } from "vue"

const updateDate = ref("2025/04/09")
const version = ref("0.1.4")
const history = reactive({
  "2025/04/20": [
    "新增交流單 - 超商必填繳費代碼",
    "新增交流單 - 活動不符合規則時, 建立失敗問題修復"
  ]
})

export {
  updateDate,
  version,
  history,
}
