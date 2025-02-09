import { ref, reactive } from "vue"

const updateDate = ref("2025/02/09")
const version = ref("0.1.1")
const history = reactive({
  "2025/02/05": [
    "新增 - 側邊欄連結畫面 (待更新也顯示)"
  ],
  "2025/02/06": [
    "新增 - 側邊欄底部新增版號及最後更新日期",
    "新增 - 登入完成後跳出近期更新項目"
  ],
  "2025/02/08": [
    "新增 - 閒置過久, 強制登出畫面",
  ],
  "2025/02/09": [
    "新增 - 權限畫面中, 可以看到目前在線使用者",
  ]
})

export {
  updateDate,
  version,
  history,
}
