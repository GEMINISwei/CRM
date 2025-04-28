import { reactive, computed } from "vue"
import { DataObject } from "@/type"

const versionDetails = reactive<DataObject>({
  "20250420_v0.1.0": [
    "新增交流單 - 超商必填繳費代碼",
    "新增交流單 - 活動不符合規則時, 建立失敗問題修復"
  ],
  "20250428_v0.1.1": [
    "新增交流單 - 遊戲幣手續費計算異常修正",
    "新增交流單 - 末五碼改為選填, 可自行決定是否是後編輯"
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

    if (index >= (versionElements.length - showCount)) {
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
