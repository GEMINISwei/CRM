import { reactive, computed } from "vue"
import { DataObject } from "@/type"

/*
  2025/05/06 待處理項目
  [資產管理] 編輯銀行交流單 - 時間紀錄改為 24 小時制 (*** 待思考如何處理 ***)
*/

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
  "20250629_v0.1.3": [
    "[交流單管理] 出金 - 輸入遊戲幣量負數也自動歸 0",
    "[資產管理] 銀行交流紀錄 - 手續費顯示修正"
  ],
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
