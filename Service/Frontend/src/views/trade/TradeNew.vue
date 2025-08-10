<script lang="ts" setup>
// ====================================================================================================================
//                  Import
// ====================================================================================================================
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { currentUser } from '@/composables/globalUse'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'


// ====================================================================================================================
//                  Enumeration
// ====================================================================================================================
enum PageStep {
  BuildPage,
  SelectGame,
  SelectMember,
  FillInTradeDetail,
}


// ====================================================================================================================
//                  Variable
// ====================================================================================================================

const tradeNewFields = reactive<CustomFormField[]>([
  { step: PageStep.SelectGame, label: '遊戲類別', type: 'select', depValue: 'game_id' },
  { step: PageStep.SelectMember, label: '會員', type: 'text', depValue: 'member_id', hidden: true },
  { step: PageStep.SelectMember, label: '遊戲帳號', type: 'searchList', depValue: 'player_id' },
  // { step: PageStep.FillInTradeDetail, label: '遊戲帳號', type: 'searchList', depValue: 'player_id' },
  { step: PageStep.FillInTradeDetail, label: '庫存角色', type: 'select', depValue: 'stock_id', required: true },
  { step: PageStep.FillInTradeDetail, label: '資產', type: 'select', depValue: 'property_id', required: true },
  { step: PageStep.FillInTradeDetail, label: '出入金類型', type: 'select', depValue: 'base_type', required: true },
  { step: PageStep.FillInTradeDetail, label: '繳費金額', type: 'number', depValue: 'money', required: true },
  { step: PageStep.FillInTradeDetail, label: '超商手續費', type: 'number', depValue: 'charge_fee', required: true, disabled: true },
  { step: PageStep.FillInTradeDetail, label: '遊戲幣', type: 'number', depValue: 'game_coin', required: true, disabled: true, min: 0 },
  { step: PageStep.FillInTradeDetail, label: '遊戲幣手續費', type: 'number', depValue: 'game_coin_fee', required: true, disabled: true },
  { step: PageStep.FillInTradeDetail, label: '末五碼', type: 'text', depValue: 'last_five_code', required: false, hidden: true },
  { step: PageStep.FillInTradeDetail, label: '繳費代碼', type: 'text', depValue: 'pay_code', required: false, hidden: true },
  { step: PageStep.FillInTradeDetail, label: '跨行手續費', type: 'number', depValue: 'diff_bank_fee', required: false, hidden: true },
])
const formBtns = reactive<CustomFormButton[]>([
  { step: PageStep.SelectMember, color: 'secondary', text: '重新選擇遊戲', method: () => setStep(PageStep.SelectGame) },
  { step: PageStep.FillInTradeDetail, color: 'secondary', text: '重新選擇會員', method: () => setStep(PageStep.SelectMember) },
  { step: PageStep.FillInTradeDetail, color: 'primary', text: '新增', method: () => createTrade(), needValid: true },
])

const currentStep = ref<PageStep>(PageStep.BuildPage)
const formData = reactive<DataObject>({})
const gamesInfo = ref<DataObject[]>([])
const membersInfo = ref<DataObject[]>([])
const propertiesInfo = ref<DataObject[]>([])
const stocksInfo = ref<DataObject[]>([])
const activitiesInfo = ref<DataObject[]>([])


// ====================================================================================================================
//                  Computed
// ====================================================================================================================
const currentGame = computed<DataObject>(() => {
  let currentInfo = gamesInfo.value.find(x => x.id == formData["game_id"])

  return currentInfo ? currentInfo : {}
})

const currentMember = computed<DataObject>(() => {
  let currentInfo = membersInfo.value.find(x => {
    let players = x.player.map((y: any) => y.id)

    return players.includes(formData["player_id"])
  })

  return currentInfo ? currentInfo : {}
})

const currentPlayer = computed<DataObject>(() => {
  return currentMember.value['player'].find((x: any) => x.id == formData['player_id'])
})

const currentProperty = computed<DataObject>(() => {
  let currentInfo = propertiesInfo.value.find(x => x.id == formData['property_id'])

  return currentInfo ? currentInfo : {}
})

const currentActivity = computed<DataObject>(() => {
  let currentInfo = {}
  let matchedInfo = activitiesInfo.value.filter(x => {
    return x.base_type == formData['base_type'] && x.money_floor <= formData['money']
  })

  if (matchedInfo.length) {
    currentInfo = matchedInfo[0]
  }

  return currentInfo
})

const isActivityOK = computed<boolean>(() => {
  return Object.keys(currentActivity.value).length > 0
})


// ====================================================================================================================
//                  Function
// ====================================================================================================================
const setStep = (index: PageStep): void => {
  currentStep.value = index
}

const getFormField = (field: string): CustomFormField | undefined => {
  return tradeNewFields.find(x => x.depValue == field)
}

const initFieldsData = (fields: string[]): void => {
  fields.forEach(field => {
    formData[field] = ''
  })
}

const calcGameCoin = (): void => {
  formData['game_coin'] = formData['money'] * (currentGame.value['money_in_exchange'])
  formData['game_coin'] = Math.ceil(formData['game_coin'])
  formData['game_coin_fee'] = Math.ceil(formData['game_coin'] * (currentGame.value['game_coin_fee']))
}

const calcMoney = (): void => {
  formData['money'] = formData['game_coin'] / currentGame.value['money_out_exchange']
  formData['money'] = Math.round(formData['money'])
  formData['game_coin_fee'] = Math.ceil(formData['game_coin'] * (currentGame.value['game_coin_fee']))
}

const getGamesInfo = () => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      let gameIdField = getFormField("game_id")

      gamesInfo.value = resData.list_data

      if (gameIdField) {
        gameIdField.options = gamesInfo.value.map((game: DataObject) => {
          return {
            text: game['name'],
            value: game['id']
          }
        })
      }
    })
}

const getMembersInfo = () => {
  let currentGameId = currentGame.value["id"]

  callApi('get', `/apis/members?game_id=${currentGameId}`)
    .then((resData: any) => {
      let playersField = getFormField("player_id")
      let resultOptions: any[] = []

      membersInfo.value = resData.list_data

      if (playersField) {
        membersInfo.value.forEach(memberInfo => {
          memberInfo['player'].forEach((player: any) => {
            resultOptions.push({
              text: player['name'],
              value: player['id']
            })
          })
        })

        playersField.options = resultOptions
      }
    })
}

const getPropertiesInfo = () => {
  callApi('get', '/apis/properties')
    .then((resData: any) => {
      let propertyIdField = getFormField("property_id")

      propertiesInfo.value = resData.list_data

      if (propertyIdField) {
        propertyIdField.options = propertiesInfo.value.map((property: DataObject) => {
          return {
            text: property['name'],
            value: property['id']
          }
        })
      }
    })
}

const getStocksInfo = (): void => {
  let currentGameId = currentGame.value["id"]

  callApi('get', `/apis/stocks?game_id=${currentGameId}`)
    .then((resData: any) => {
      let stockIdField = getFormField("stock_id")

      stocksInfo.value = resData.list_data

      if (stockIdField) {
        stockIdField.options = stocksInfo.value.map((stock: DataObject) => {
          return {
            text: stock['role_name'],
            value: stock['id']
          }
        })
      }
    })
}

const getactivitiesInfo = () => {
  callApi('get', `/apis/activities?game_id=${formData['game_id']}`)
    .then((resData: any) => {
      if (resData.list_data.length > 0) {
        activitiesInfo.value = resData.list_data
      }
    })
}

const createTrade = (): void => {
  let current_time = new Date(Date.now())
  let acitvityStartTime = new Date(currentActivity.value.start_time)
  let activityEndTime = new Date(currentActivity.value.end_time)
  // let lastFiveCodeField = getFormField("last_five_code")

  // if (lastFiveCodeField) {
  //   if (lastFiveCodeField.hidden != true && formData["last_five_code"].length != 5) {
  //     createNotify('error', "末五碼字數不正確 !")

  //     return
  //   }
  // }

  if (isActivityOK.value) {
    if (acitvityStartTime < current_time && current_time < activityEndTime) {
      createNotify('success', "符合活動資格 !")
    } else {
      setStep(PageStep.SelectGame)
      createNotify('error', [
        "已不在活動時間內 !",
        "已重新載入活動資訊"
      ])

      return // 不執行建立動作
    }
  }

  callApi('post', '/apis/trades', getRequestData())
    .then(() => {
      createNotify('success', "建立成功")
      goPage('/properties/details', {
        showTitle: currentProperty.value["name"],
        showKind: currentProperty.value["kind"],
        showId: currentProperty.value["id"],
      })
    })
    .catch((_: any) => {
      createNotify('error', "建立失敗")
    })
}

const getRequestData = (): DataObject => {
  let lastFiveCodeField = getFormField("last_five_code")
  let payCodeField = getFormField("pay_code")
  let resultObj: DataObject = {
    game_id: formData['game_id'],
    member_id: currentMember.value['id'],
    player_id: formData['player_id'],
    property_id: formData['property_id'],
    stock_id: formData['stock_id'],
    base_type: formData['base_type'],
    money: formData['money'],
    charge_fee: formData['charge_fee'],
    game_coin: formData['game_coin'],
    game_coin_fee: formData['game_coin_fee'],
    created_by: currentUser.username,
    details: {},
  }

  if (!lastFiveCodeField || !payCodeField) {
    return {}
  }

  if (formData["last_five_code"]) {
    resultObj['details']['last_five_code'] = formData["last_five_code"]
  }
  if (formData["pay_code"]) {
    resultObj['details']['pay_code'] = formData["pay_code"]
  }
  if (formData["diff_bank_fee"]) {
    resultObj['details']['diff_bank_fee'] = formData["diff_bank_fee"]
  }

  return resultObj
}


// ====================================================================================================================
//                  Watch
// ====================================================================================================================
watch(currentStep, (newVal) => {
  switch (newVal) {
    case PageStep.SelectGame:
      let gameCoinField = getFormField("game_coin")

      if (gameCoinField) {
        gameCoinField.description = ""
      }

      getGamesInfo()
      initFieldsData(["game_id"])
      break

    case PageStep.SelectMember:
      getMembersInfo()
      initFieldsData(["member_id", "sock_puppets"])
      break

    case PageStep.FillInTradeDetail:
      getPropertiesInfo()
      getStocksInfo()
      getactivitiesInfo()
      initFieldsData(["stock_id", "property_id", "base_type", "money", "last_five_code", "diff_bank_fee"])
      break
  }
})
watch(() => formData['game_id'], (newVal) => {
  if (newVal) {
    setStep(PageStep.SelectMember)
  }
})
watch(() => formData['player_id'], (newVal) => {
  if (newVal) {
    setStep(PageStep.FillInTradeDetail)
  }
})
watch(() => formData['property_id'], (newVal) => {
  let baseTypeField = getFormField("base_type")
  let chargeFeeField = getFormField("charge_fee")
  let lastFiveCodeField = getFormField("last_five_code")
  let payCodeField = getFormField("pay_code")

  if (!baseTypeField || !chargeFeeField || !lastFiveCodeField || !payCodeField) {
    return
  }

  lastFiveCodeField.hidden = true
  payCodeField.hidden = true
  chargeFeeField.hidden = true
  payCodeField.required = false

  if (newVal) {
    formData['charge_fee'] = 0
    baseTypeField.options = [
      { text: '入金', value: 'money_in' },
    ]

    if (currentProperty.value.kind == 'bank') {
      baseTypeField.options = [
        { text: '入金', value: 'money_in' },
        { text: '出金', value: 'money_out' },
      ]

      if (formData['base_type']) {
        lastFiveCodeField.hidden = false
      }
    } else if (currentProperty.value.kind == 'supermarket') {
      payCodeField.hidden = false
      chargeFeeField.hidden = false
      payCodeField.required = true
      formData['base_type'] = 'money_in'
      formData["charge_fee"] = currentGame.value["charge_fee"]
    } else if (currentProperty.value.kind == 'v_account') {
      formData['base_type'] = 'money_in'
    }

    if (!baseTypeField.options.find(x => x.value == formData['base_type'])) {
      formData['base_type'] = ''
    }
  } else {
    baseTypeField.options = []
    formData['charge_fee'] = ''
  }
})
watch(() => formData['base_type'], (newVal) => {
  let moneyField = getFormField("money")
  let gameCoinField = getFormField("game_coin")
  let gameCoinFeeField = getFormField("game_coin_fee")
  let lastFiveCodeField = getFormField("last_five_code")
  let diffBankFeeField = getFormField("diff_bank_fee")

  if (!moneyField || !gameCoinField || !gameCoinFeeField || !lastFiveCodeField || !diffBankFeeField) {
    return
  }

  lastFiveCodeField.hidden = true
  diffBankFeeField.hidden = true
  gameCoinFeeField.hidden = false

  if (newVal) {
    moneyField.disabled = false
    gameCoinField.disabled = false
    formData['money'] = 0
    formData['charge_fee'] = 0
    formData['game_coin'] = 0
    formData['game_coin_fee'] = 0

    if (currentProperty.value.kind == 'bank') {
      if (newVal == 'money_in') {
        moneyField.label = "實收金額"
        gameCoinField.disabled = true
        lastFiveCodeField.hidden = false
      } else if (newVal == 'money_out') {
        diffBankFeeField.hidden = false
        gameCoinFeeField.hidden = true
        moneyField.disabled = true
        moneyField.label = "實轉金額"
        formData['diff_bank_fee'] = 0
      }
    } else {
      moneyField.label = "繳費金額"
    }

  } else {
    moneyField.disabled = true
    formData['money'] = ''
  }
})
watch(() => formData['money'], (newVal) => {
  let moneyField = getFormField("money")
  let chargeFeeField = getFormField("charge_fee")
  let gameCoinField = getFormField("game_coin")

  if (!moneyField || !chargeFeeField || !gameCoinField) {
    return
  }

  if (typeof newVal === 'number') {
    if (formData['base_type'] == 'money_in') {
      calcGameCoin()
    }
    formData["charge_fee"] = 0

    if (currentGame.value["market_free_fee"] != 0 && newVal >= currentGame.value["market_free_fee"]) {
      chargeFeeField.label = '交易手續費 (滿額免手續費)'
    } else {
      chargeFeeField.label = '交易手續費'

      if (currentProperty.value.kind == 'supermarket') {
        formData["charge_fee"] = currentGame.value["charge_fee"]
      }
    }

    if (isActivityOK.value) {
      let result = formData["game_coin"] + currentActivity.value["coin_free"]
      let description = `${formData["game_coin"]} + ${currentActivity.value["coin_free"]} = ${result}`

      gameCoinField.description = description
      formData["game_coin"] = result
      formData["game_coin_fee"] = Math.ceil(formData['game_coin'] * (currentGame.value['game_coin_fee']))
    } else {
      gameCoinField.description = ""
    }

  } else {
    formData['game_coin'] = ''
    formData['game_coin_fee'] = ''
  }
})
watch(() => formData['game_coin'], (newVal) => {
  let moneyField = getFormField("money")

  if (!moneyField) {
    return
  }

  if (typeof newVal === 'number') {
    if (formData['base_type'] == 'money_out') {
      calcMoney()
    }
  } else {
    formData['money'] = ''
    formData['game_coin_fee'] = ''
  }

})

onMounted(() => {
  setStep(PageStep.SelectGame)
})
</script>

<template>
  <div class="container">
    <div class="m-4">
      <h3 class="text-center">新增交流單</h3>
      <h3 v-show="currentStep == PageStep.SelectGame" class="text-center">
        選擇遊戲類別
      </h3>
      <h3 v-show="currentStep == PageStep.SelectMember" class="text-center">
        選擇 "{{ currentGame.name }}" 類別之遊戲帳號
      </h3>
      <template v-if="currentStep == PageStep.FillInTradeDetail">
        <h3 class="text-center">會員 {{ currentMember.nickname }} - {{ currentPlayer.name }}</h3>
        <div v-if="isActivityOK" class="text-center activity-ok">
          <p>*** 符合優惠條件 ***</p>
        </div>
      </template>
    </div>
    <CustomForm
      :fields="tradeNewFields"
      hasStep
      :currentStep
      :buttons="formBtns"
      v-model:formData="formData"
    />
  </div>
</template>

<style lang="scss" scoped>
.activity-ok {
  color: white;
  animation: neon 2s ease-in-out infinite alternate;
}
@keyframes neon {
  0%,
  100% {
    text-shadow: 0 0 10px white, 0 0 10px white, 0 0 10px white;
  }
  50% {
    text-shadow: 0 0 15px white, 0 0 10px white, 0 0 15px white;
  }
}
</style>
