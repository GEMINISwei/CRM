<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import CustomForm from '@/components/CustomForm.vue'
import type { DataObject, OptionObject, CustomFormField, CustomFormButton } from '@/type'


const justInTypeOptions: OptionObject[] = [
  { text: '入金', value: 'money_in' },
]
const baseTypeOptions: OptionObject[] = [
  { text: '入金', value: 'money_in' },
  { text: '出金', value: 'money_out' },
]

const tradeNewFields = reactive<CustomFormField[]>([
  { step: 0, label: '遊戲類別', type: 'select', depValue: 'game_id' },
  { step: 1, label: '遊戲暱稱', type: 'searchList', depValue: 'member_id' },
  { step: 2, label: '庫存角色', type: 'select', depValue: 'stock_id', required: true },
  { step: 2, label: '資產', type: 'select', depValue: 'property_id', required: true },
  { step: 2, label: '出入金類型', type: 'select', depValue: 'base_type', required: true, options: baseTypeOptions },
  { step: 2, label: '金額', type: 'number', depValue: 'money', required: true },
  { step: 2, label: '交易手續費', type: 'number', depValue: 'charge_fee', required: true, disabled: true },
  { step: 2, label: '遊戲幣', type: 'number', depValue: 'game_coin', required: true, disabled: true },
  { step: 2, label: '遊戲幣手續費', type: 'number', depValue: 'game_coin_fee', required: true, disabled: true },
])
const formData = reactive<DataObject>({})
const gamesInfo = ref<DataObject[]>([])
const membersInfo = ref<DataObject[]>([])
const propertiesInfo = ref<DataObject[]>([])
const stocksInfo = ref<DataObject[]>([])
const couponInfo = ref<DataObject>({})
const hasCoupon = ref<boolean>(false)
const currentStep = ref<number>(0)

const formBtns: CustomFormButton[] = [
  { step: 1, color: 'secondary', text: '重新選擇遊戲', method: () => currentStep.value = 0 },
  { step: 2, color: 'secondary', text: '重新選擇會員', method: () => currentStep.value = 1 },
  { step: 2, color: 'primary', text: '新增', method: () => createTrade(), needValid: true },
]

const currentGame = computed<DataObject>(() => {
  let currentInfo = gamesInfo.value.find(x => x.id == formData["game_id"])

  return currentInfo ? currentInfo : {}
})

const currentMember = computed<DataObject>(() => {
  let currentInfo = membersInfo.value.find(x => x.id == formData["member_id"])

  return currentInfo ? currentInfo : {}
})

const currentProperty = computed<DataObject>(() => {
  let currentInfo = propertiesInfo.value.find(x => x.id == formData["property_id"])

  return currentInfo ? currentInfo : {}
})

const isCouponOK = computed<boolean>(() => {
  return hasCoupon.value && formData['money'] >= couponInfo.value.money_floor
})

onMounted(() => {
  getGamesInfo()
})

watch(currentStep, (newVal) => {
  switch (newVal) {
    case 0:
      formData['game_id'] = ''
      break

    case 1:
      formData['member_id'] = ''
      formData['base_type'] = ''
      formData['property_id'] = ''
      formData['money'] = ''
      break

    case 2:
      getCouponInfo()
  }
})

watch(() => formData['game_id'], (newVal) => {
  if (newVal) {
    getMembersInfo()

    currentStep.value = 1
  }
})

watch(() => formData['member_id'], (newVal) => {
  if (newVal) {
    getPropertiesInfo()
    getStocksInfo()

    currentStep.value = 2
  }
})

watch(() => formData['base_type'], (newVal) => {
  let moneyField = getFormField("money")
  let chargeFeeField = getFormField("charge_fee")

  if (moneyField && chargeFeeField) {
    if (newVal != '') {
      moneyField.disabled = false
      chargeFeeField.disabled = (newVal != 'money_out')
      calcGameCoin()
    } else {
      moneyField.disabled = true
    }
  }
})

watch(() => currentProperty.value.kind, (newVal) => {
    let baseTypeField = getFormField("base_type")

    formData['base_type'] = ''
    formData['money'] = 0
    formData['charge_fee'] = 0

    if (baseTypeField) {
      if (newVal == 'bank') {
        baseTypeField.options = baseTypeOptions
      } else if (newVal == 'supermarket') {
        baseTypeField.options = justInTypeOptions
        formData["charge_fee"] = currentGame.value["charge_fee"]
        formData['base_type'] = 'money_in'
      } else if (newVal == 'v_account') {
        baseTypeField.options = justInTypeOptions
        formData['base_type'] = 'money_in'
      }
    }
  }
)

watch(() => formData["money"], (newVal) => {
  let chargeFeeField = getFormField("charge_fee")

  if (newVal >= 0) {
    calcGameCoin()
  }

  if (chargeFeeField) {
    if (newVal >= 2000) {
      chargeFeeField.label = '交易手續費 (滿額免費)'
      formData["charge_fee"] = 0
    } else {
      chargeFeeField.label = '交易手續費'
    }
  }
})

watch(
  () => [
    formData["money"],
    isCouponOK.value
  ], ([_, newVal_2]) => {
    let gameCoinField = getFormField("game_coin")

    if (gameCoinField) {
      if (newVal_2) {
        let result = formData["game_coin"] + couponInfo.value["coin_free"]
        let description = `${formData["game_coin"]} + ${couponInfo.value["coin_free"]} = ${result}`

        gameCoinField.description = description
        formData["game_coin"] = result
      } else {
        gameCoinField.description = ""
      }
    }
  }
)

const calcGameCoin = (): void => {
  if (formData['base_type'] == 'money_in') {
    formData['game_coin'] = formData['money'] * (currentGame.value['money_in_exchange'])
  } else if (formData['base_type'] == 'money_out') {
    formData['game_coin'] = formData['money'] * (currentGame.value['money_out_exchange'])
  } else {
    formData['game_coin'] = 0
  }

  formData['game_coin'] = Math.ceil(formData['game_coin'])
  formData['game_coin_fee'] = Math.ceil(formData['game_coin'] * (currentGame.value['game_coin_fee']))
}


const getFormField = (field: string): CustomFormField | undefined => {
  return tradeNewFields.find(x => x.depValue == field)
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
      let memberIdField = getFormField("member_id")

      membersInfo.value = resData.list_data

      if (memberIdField) {
        memberIdField.options = membersInfo.value.map((member: DataObject) => {
          return {
            text: member['nickname'],
            value: member['id']
          }
        })
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

const getCouponInfo = () => {
  callApi('get', '/apis/coupons')
    .then((resData: any) => {
      if (resData.list_data.length > 0) {
        couponInfo.value = resData.list_data[0]
        hasCoupon.value = true
      } else {
        hasCoupon.value = false
      }
    })
}

const createTrade = () => {
  let current_time = new Date(Date.now())
  let start_time = new Date(couponInfo.value.start_time)
  let end_time = new Date(couponInfo.value.end_time)

  if (hasCoupon.value) {
    if (start_time < current_time && current_time < end_time) {
      createNotify('success', "符合活動資格 !")
    } else {
      getCouponInfo()
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
  let resultObj: DataObject = {
    'member_id': formData['member_id'],
    'property_id': formData['property_id'],
    'stock_id': formData['stock_id'],
    'base_type': formData['base_type'],
    'money': formData['money'],
    'charge_fee': formData['charge_fee'],
    'game_coin': formData['game_coin'],
    'game_coin_fee': formData['game_coin_fee'],
  }

  switch (currentProperty.value["kind"]) {
    case 'supermarket':
      resultObj['stage_fee'] = 5
      break

    case 'v_account':
      resultObj['stage_fee'] = -10
      break
  }

  return resultObj
}
</script>

<template>
  <div class="container">
    <div class="m-4">
      <h3 class="text-center">新增交流單</h3>
      <h3 v-show="currentStep == 0" class="text-center">
        選擇遊戲類別
      </h3>
      <h3 v-show="currentStep == 1" class="text-center">
        選擇 "{{ currentGame.name }}" 類別之會員
      </h3>
      <template v-if="currentStep == 2">
        <h3 class="text-center">會員 "{{ currentMember.nickname }}" 新增交流單</h3>
        <div v-if="isCouponOK" class="text-center coupon-ok">
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
.coupon-ok {
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
