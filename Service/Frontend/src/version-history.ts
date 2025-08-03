import { reactive, computed } from "vue"
import { DataObject } from "@/type"

/*
  [媒合紀錄] 詳細規則
    假設入金 - 匯率 1:130 (向玩家賣出 1300000 遊戲幣)
    => 入金 1300000 / 130 = 10,000 台幣

    假設出金 - 匯率 1:140 (向玩家買入 1300000 遊戲幣)
    => 出金 1300000 / 140 = 9,286 台幣

    媒合階段
    => 10000 - 9286 = 714 (獲利)

  [系統設定] 權限功能
    針對權限群組分類, 並且控管權限群組可檢視 & 操作設定
    再將使用者加入群組, 來達到權限管理
    新建立的使用者預設為無權限, 需等待管理員進行設定
*/

const versionDetails = reactive<DataObject>({
  "20250512_v0.1.2": [
    "[資產管理] 交流紀錄 - 修正顯示順序異常",
    "[資產管理] 交流紀錄 - 欄位順序修改 (庫存角色移至最後)",
    "[資產管理] 新增銀行交流單 - 新增跨行手續費, 預設值為 0 (選填)",
    "[資產管理] 編輯銀行交流單 - 新增跨行手續費, 預設值為 0 (選填)",
    "[系統設定] 手續費 - 文字敘述修改 (代收平台 -> 超商平台)",
    "[系統設定] 手續費 - 數值限制為 0 以上"
  ],
  "20250527_v0.1.3": [
    "[小遊戲] 新增抽獎 - 需要先勾選此次中獎的項目, 轉盤依舊正常顯示抽獎動畫",
    "[交流單管理] 新增交流單 - 出金類別區分手打金額 & 實收金額",
    "[庫存管理] 庫存列表 - 遊戲幣修正數值需要帶入角色庫存",
    "[資產管理] 交流紀錄 - 台幣 & 遊戲幣修正數值需要帶入金額 & 遊戲幣",
    "[資產管理] 資產列表 - 台幣 & 遊戲幣修正數值需要帶入總餘額",
    "[資產管理] 超商交流紀錄 - 實收金額顯示修正, 需帶入超商手續費"
  ],
  "20250603_v0.1.4": [
    "[資產管理] 超商交流紀錄 - 修正實收金額數字不對 (平台手續費)"
  ],
  "20250605_v0.1.5": [
    "[遊戲管理] 遊戲列表 - 交易手續費改為超商手續費",
    "[交流單管理] 新增交流單 - 入金為實收金額, 出金為實轉金額",
    "[交流單管理] 新增交流單 - 出金計算功能修正",
    "[資產管理] 超商交流紀錄 - 繳費金額、實收金額公式修正"
  ],
  "20250709_v0.1.6": [
    "[交流單管理] 出金 - 輸入遊戲幣量負數也自動歸 0",
    "[資產管理] 銀行交流紀錄 - 手續費顯示修正"
  ],
  "20250720_v0.1.7": [
    "[交流單管理] 新增交流單 - 超商類別欄位敘述修改 (滿額免費 -> 滿額免手續費)",
    "[資產管理] 編輯交流單 - 欄位敘述修改 (多給的 -> 錯帳)",
    "[資產管理] 交流紀錄 - 若此筆交流單有錯帳修改, 金額及遊戲幣部分會呈現紅字",
    "[資產管理] 交流紀錄 - 超商及虛擬帳號, 可以選擇顯示每日實收金額清單",
    "[遊戲管理] 新增遊戲 - 新增超商滿額免手續費設定, 可依照遊戲決定滿額免額手續費的設定值",
  ],
  "20250728_v0.2.0": [
    "[遊戲管理] 新增遊戲 - 新增排序設定, 可自行決定排序的依據",
    "[資產管理] 交流紀錄 - 紀錄建立交流單的使用者 (還沒顯示出來, 純粹紀錄)",
    "[交流單管理] 新增交流單 - 可以選擇輸入遊戲暱稱或是分身, 可以直接輸入搜尋",
    "[會員管理] 出入金列表 - 每個遊戲帳號個別呈現每個月的出入金額度列表",
  ],
  "20250803_v0.2.1": [
    "[交流單管理] 新增交流單 - 滿額免手續費設定為 0, 則當作永遠需要手續費",
    "[會員管理] 會員列表 - 遊戲分身顯示異常修正",
    "[會員管理] 會員列表 - 補上遊戲暱稱搜尋框",
    // "[資產管理] 交流紀錄 - 建立交流單 (白色), 完成訂單 (當班顏色), 檢查完成 (下一班顏色), 共用按鈕",
    // "[頁面清單] 結帳功能 - 晚班需要進行兩次結帳動作, 按鈕會區分開 (一種是晚上 12:00 前的結帳)",
    // "[員工管理] 業績列表 - 呈現員工的個別遊戲業績",
    // "[系統設定] 使用權限 - 群組設定、建立使用者 (幫每個員工建立一個帳號)",
  ]
})

const updateDate = computed(() => {
  let versionElements = Object.keys(versionDetails)
  let lastDate = versionElements[versionElements.length - 1].split("_")[0]
  let year = lastDate.slice(0, 4)
  let month = lastDate.slice(4, 6)
  let day = lastDate.slice(6, 8)

  return `${year}/${month}/${day}`
})

const currentVersion = computed(() => {
  let versionElements = Object.keys(versionDetails)
  let lastVersion = versionElements[versionElements.length - 1].split("_v")[1]

  return lastVersion
})

const showHistory = computed(() => {
  let versionElements = Object.keys(versionDetails)
  let showCount = 3
  let showInfo: DataObject = {}

  // 版本顯示順序由上至下 (由新至舊)
  versionElements.reverse().forEach((version, index) => {
    let dateInfo = version.split("_")[0]
    let year = dateInfo.slice(0, 4)
    let month = dateInfo.slice(4, 6)
    let day = dateInfo.slice(6, 8)

    if (index < showCount) {
      showInfo[`${year}/${month}/${day}`] = versionDetails[version]
    }
  })

  return showInfo
})

export {
  updateDate,
  currentVersion,
  showHistory,
}
