<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi, callMultipleGetApi } from '@/composables/api'
import { currentUser } from '@/composables/globalUse'
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
  // { step: 2, label: '末五碼', type: 'text', depValue: 'last_five_code', required: true, hidden: true },
  // { step: 2, label: '繳費代碼', type: 'text', depValue: 'pay_code', required: true, hidden: true },
  // { step: 2, label: '門市', type: 'text', depValue: 'store', hidden: true },
  // { step: 2, label: '虛擬帳號', type: 'text', depValue: 'v_account', required: true, hidden: true },
])
const formData = reactive<DataObject>({})
const couponInfo = ref<DataObject>({})

const formBtns: CustomFormButton[] = [
  { step: 1, color: 'secondary', text: '重新選擇遊戲', method: () => currentStep.value = 0 },
  { step: 2, color: 'secondary', text: '重新選擇會員', method: () => currentStep.value = 1 },
  { step: 2, color: 'primary', text: '新增', method: () => createTrade(), needValid: true },
]

const propertiesInfo = ref<DataObject[]>([])
const membersInfo = ref<DataObject[]>([])
const hasCoupon = ref<boolean>(false)

const currentStep = ref<number>(0)

const memberGameName = computed<string>(() => {
  let memberIdFieldIndex = tradeNewFields.findIndex(x => x.depValue == 'member_id')
  let currentGameName = tradeNewFields[memberIdFieldIndex].options?.find((option: OptionObject) => option.value == formData['member_id'])

  return currentGameName ? currentGameName.text : ''
})

const currentKind = computed<string>(() => {
  let kindResult = ''

  propertiesInfo.value.forEach((property: DataObject) => {
    if (property['id'] == formData['property_id']) {
      kindResult = property['kind']
    }
  })

  return kindResult
})

const isCouponOK = computed<boolean>(() => {
  return hasCoupon.value && formData['money'] >= couponInfo.value.money_floor
})

onMounted(() => {
  getOptionsList()
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
    let gameNameFieldIndex: number = tradeNewFields.findIndex(x => x.depValue == 'member_id')
    let matchedMembers: DataObject[] = membersInfo.value.filter((member: DataObject) => {
      return member['games'][0]['id'] == newVal
    })

    tradeNewFields[gameNameFieldIndex].options = matchedMembers.map((member: DataObject) => {
      return {
        text: member['nickname'],
        value: member['id']
      }
    })

    currentStep.value = 1
  }
})

watch(() => formData['member_id'], (newVal) => {
  if (newVal) {
    let memberInfo = membersInfo.value.find(x => x['id'] == newVal)

    getStockOptions(memberInfo?.['games'][0]['id'])

    currentStep.value = 2
  }
})

watch(() => formData['base_type'], (newVal) => {
  let moneyFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'money')
  let chargeFeeFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'charge_fee')

  if (newVal != '') {
    tradeNewFields[moneyFieldIndex].disabled = false
    tradeNewFields[chargeFeeFieldIndex].disabled = (newVal != 'money_out')
    calcGameCoin()
  } else {
    tradeNewFields[moneyFieldIndex].disabled = true
  }
})

watch(currentKind, (newVal) => {
  let memberInfo = membersInfo.value.find(x => x['id'] == formData['member_id'])
  let baseTypeFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'base_type')
  // let lastFiveFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'last_five_code')
  // let payCodeFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'pay_code')
  // let storeFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'store')
  // let vAccountFieldIndex = tradeNewFields.findIndex((field: CustomFormField) => field.depValue == 'v_account')

  // tradeNewFields[lastFiveFieldIndex].hidden = true
  // tradeNewFields[payCodeFieldIndex].hidden = true
  // tradeNewFields[storeFieldIndex].hidden = true
  // tradeNewFields[vAccountFieldIndex].hidden = true
  formData['base_type'] = ''
  formData['charge_fee'] = 0
  formData['money'] = 0

  if (newVal == 'bank') {
    // tradeNewFields[lastFiveFieldIndex].hidden = false
    tradeNewFields[baseTypeFieldIndex].options = baseTypeOptions
  } else if (newVal == 'supermarket') {
    formData['charge_fee'] = memberInfo?.['game_info']['charge_fee']
    // tradeNewFields[payCodeFieldIndex].hidden = false
    // tradeNewFields[storeFieldIndex].hidden = false
    tradeNewFields[baseTypeFieldIndex].options = justInTypeOptions
    formData['base_type'] = 'money_in'
  } else if (newVal == 'v_account') {
    // tradeNewFields[lastFiveFieldIndex].hidden = false
    // tradeNewFields[vAccountFieldIndex].hidden = false
    tradeNewFields[baseTypeFieldIndex].options = justInTypeOptions
    formData['base_type'] = 'money_in'
  }
})

watch(() => formData['money'], (newVal) => {
  if (newVal >= 0) {
    calcGameCoin()
  }

  if (currentKind.value == 'supermarket') {
    let chargeFeeFieldIndex = tradeNewFields.findIndex(x => x.depValue == 'charge_fee')

    // 超商有滿額免手續費
    if (newVal >= 2000) {
      tradeNewFields[chargeFeeFieldIndex].label = '交易手續費 (滿額免費)'

      formData['charge_fee'] = 0
    } else {
      let memberInfo = membersInfo.value.find(x => x['id'] == formData['member_id'])

      tradeNewFields[chargeFeeFieldIndex].label = '交易手續費'
      formData['charge_fee'] = memberInfo?.['game_info']['charge_fee']
    }
  }
})

watch(isCouponOK, (newVal) => {
  let moneyFieldIndex = tradeNewFields.findIndex(x => x.depValue == "money")

  if (newVal) {
    let result = formData["money"] - couponInfo.value["money_free"]
    let description = `${formData["money"]} - ${couponInfo.value["money_free"]} = ${result}`

    tradeNewFields[moneyFieldIndex].description = description
  } else {
    tradeNewFields[moneyFieldIndex].description = ""
  }
})

const calcGameCoin = (): void => {
  let memberInfo = membersInfo.value.find(x => x['id'] == formData['member_id'])

  if (formData['base_type'] == 'money_in') {
    formData['game_coin'] = formData['money'] * (memberInfo ? memberInfo['games'][0]['money_in_exchange'] : 0)
  } else if (formData['base_type'] == 'money_out') {
    formData['game_coin'] = formData['money'] * (memberInfo ? memberInfo['games'][0]['money_out_exchange'] : 0)
  } else {
    formData['game_coin'] = 0
  }

  formData['game_coin'] = Math.ceil(formData['game_coin'])
  formData['game_coin_fee'] = Math.ceil(formData['game_coin'] * (memberInfo ? memberInfo['games'][0]['game_coin_fee'] : 0))
}

const getOptionsList = (): void => {
  callMultipleGetApi([
    '/apis/members?count=100&page=1',
    '/apis/properties?count=100&page=1',
    '/apis/games'
  ])
    .then((res: any) => {
      setMemberOptions(res[0].data)
      setPropertyOptions(res[1].data)
      setGameOptions(res[2].data)
    })
}

const setGameOptions = (gamesData: DataObject[]) => {
  let gameIdFieldIndex: number = tradeNewFields.findIndex(x => x.depValue == 'game_id')

  tradeNewFields[gameIdFieldIndex].options = gamesData.map((game: DataObject) => {
    return {
      text: game['name'],
      value: game['id']
    }
  })
}

const getStockOptions = (gameId: string): void => {
  callApi('get', `/apis/stocks?game_id=${gameId}`)
    .then((res: any) => {
      setStockOptions(res.data)
    })
}

const setMemberOptions = (membersData: DataObject[]) => {
  membersInfo.value = membersData.map(x => x)
}

const setStockOptions = (stocksData: DataObject[]) => {
  let stockIdFieldIndex: number = tradeNewFields.findIndex(x => x.depValue == 'stock_id')

  tradeNewFields[stockIdFieldIndex].options = stocksData.map((stock: DataObject) => {
    return {
      text: stock['role_name'],
      value: stock['id'],
    }
  })
}

const setPropertyOptions = (propertiesData: any[]) => {
  let propertyIdFieldIndex: number = tradeNewFields.findIndex(x => x.depValue == 'property_id')

  propertiesInfo.value = propertiesData

  tradeNewFields[propertyIdFieldIndex].options = propertiesData.map((data: any) => {
    return {
      text: data['name'],
      value: data['id'],
    }
  })
}

const getCouponInfo = () => {
  callApi('get', '/apis/coupons')
    .then((res: any) => {
      if (res.data.length > 0) {
        couponInfo.value = res.data[0]
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
      let propertyIdFieldIndex = tradeNewFields.findIndex((x) => x.depValue == 'property_id')
      let currentProperty = tradeNewFields[propertyIdFieldIndex].options?.find(x => x.value == formData['property_id'])

      createNotify('success', "建立成功")
      goPage('/properties/details', {
        showTitle: currentProperty?.text,
        showKind: currentKind.value,
        showId: currentProperty?.value,
      })
    })
    .catch((err: any) => {
      console.log(err)
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
    'first_check': currentUser['shift']
  }

  switch (currentKind.value) {
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
      <h3 v-show="currentStep == 0" class="text-center">選擇遊戲類別</h3>
      <h3 v-show="currentStep == 1" class="text-center">選擇會員</h3>
      <template v-if="currentStep == 2">
        <h3 class="text-center">會員 "{{ memberGameName }}" 新增交流單</h3>
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
