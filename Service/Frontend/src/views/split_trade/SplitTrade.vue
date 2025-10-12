<script setup lang="ts">
import { ref } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { setStatusFlag, currentUser } from '@/composables/globalUse'
import { createNotify } from '@/composables/notify'
import DataTable from '@/components/DataTable.vue'
import CustomInput from '@/components/CustomInput.vue'
import type { DataObject, DataTableField } from '@/type'

const titleText: string = '拆帳列表'
const fieldInfo: DataTableField[] = [
  { label: '日期', depValue: 'date', width: '15%' },
  { label: '會員', depValue: 'member_name', width: '15%' },
  { label: '已完成額度', depValue: 'already_money', width: '25%' },
  { label: '總額度', depValue: 'total_money', width: '25%' },
  { label: '操作', depValue: 'operate', width: '20%' },
]
const apiUrl: string = '/apis/split_trades'
const splitTrades = ref<DataObject[]>([])
const showIndex = ref<number>(-1)
const splitMoney = ref<number>(0)
const maxMoney = ref<number>(0)

const openModal = (index: number, modalName: string): void => {
  let currentData = splitTrades.value[index]

  showIndex.value = index
  maxMoney.value = currentData['total_money'] - currentData['already_money']

  if (modalName == 'splitTrade') {
    setStatusFlag('modalShow', true)
  } else if (modalName == 'refund') {
    setStatusFlag('modalShow2', true)
  }
}

const createSplitTrade = (): void => {
  let currentId = splitTrades.value[showIndex.value]['id']

   callApi('patch', `/apis/split_trades/${currentId}`, {
    money: splitMoney.value,
    created_by: currentUser.username,
    is_finish: splitMoney.value == maxMoney.value,
   })
    .then((_: any) => {
      createNotify('success', "建立成功")
      setStatusFlag('modalShow', false)
      goPage('/properties/details', {
        showTitle: splitTrades.value[showIndex.value]['property_name'],
        showKind: splitTrades.value[showIndex.value]['property_kind'],
        showId: splitTrades.value[showIndex.value]['property_id'],
      })
    })
}

const createRefundTrade = (): void => {
  let currentId = splitTrades.value[showIndex.value]['id']

   callApi('patch', `/apis/refund_split_trades/${currentId}`, {
    refund_money: maxMoney.value,
    created_by: currentUser.username,
   })
    .then((_: any) => {
      createNotify('success', "建立成功")
      setStatusFlag('modalShow2', false)
      goPage('/properties/details', {
        showTitle: splitTrades.value[showIndex.value]['property_name'],
        showKind: splitTrades.value[showIndex.value]['property_kind'],
        showId: splitTrades.value[showIndex.value]['property_id'],
      })
    })
}


</script>

<template>
  <div class="container">
    <DataTable :titleText :fieldInfo :apiUrl v-model:tableData="splitTrades">
      <template #tableCell="{ fieldName, hasData, dataIndex }">
        <div v-if="fieldName == 'operate' && hasData">
          <i class="bi-receipt text-primary fs-4 mx-2" role="button" @click="openModal(dataIndex, 'splitTrade')" v-tooltip="'拆帳'"></i>
          <i class="bi-ban text-danger fs-4 mx-2" role="button" @click="openModal(dataIndex, 'refund')" v-tooltip="'取消此筆'"></i>
        </div>
      </template>
    </DataTable>

    <Teleport to="#modal-header">
      <h3>拆帳金額</h3>
    </Teleport>
    <Teleport to="#modal-body">
      <div class="d-flex justify-content-center row">
        <CustomInput type="number" :max="maxMoney" :min="0" v-model:inputData="splitMoney" />
        <button class="btn btn-success m-4" @click="() => createSplitTrade()">執行拆帳</button>
      </div>
    </Teleport>

    <Teleport to="#modal-header-2">
      <h3>退款金額</h3>
    </Teleport>
    <Teleport to="#modal-body-2">
      <div class="d-flex justify-content-center row">
        <CustomInput type="number" v-model:inputData="maxMoney" disabled />
        <button class="btn btn-danger m-4" @click="() => createRefundTrade()">執行退款</button>
      </div>
    </Teleport>
  </div>
</template>
