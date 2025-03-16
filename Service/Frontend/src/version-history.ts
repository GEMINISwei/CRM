import { ref, reactive } from "vue"

const updateDate = ref("2025/03/16")
const version = ref("0.1.2")
const history = reactive({
  "2025/03/15": [
    "新增會員 - 敘述 \"新增員工\" 改為 \"新增會員\"",
    "新增交流單 - 銀行轉帳時, 新增末五碼欄位 (必填)"
  ],
  "2025/03/16": [
    "新增活動 - 新增指定遊戲類別",
    "活動列表 - 增加編輯、刪除功能"
  ]
})

export {
  updateDate,
  version,
  history,
}
