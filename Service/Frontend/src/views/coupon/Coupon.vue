<script setup lang="ts">
import { ref } from 'vue'
// import { goPage } from '@/router'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataObject, DataTableField, FuncListItem } from '@/type'

const titleText: string = '活動列表'
const fieldInfo: DataTableField[] = [
  { label: '活動名稱', depValue: 'name', width: '20%' },
  { label: '開始時間', depValue: 'start_time', width: '20%' },
  { label: '結束時間', depValue: 'end_time', width: '20%' },
  { label: '滿額條件', depValue: 'money_floor', width: '20%' },
  { label: '贈送遊戲幣', depValue: 'coin_free', width: '20%' },
  // { label: '操作', depValue: 'operate', width: '15%' },
]
const apiUrl: string = '/apis/coupons'
const coupons = ref<DataObject[]>([])

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增活動', icon: 'plus-square', goPath: '/coupons/new' },
]

// const goGameEdit = (index: number) => {
//   goPage('/coupons/edit', {
//     editId: coupons.value[index]['id']
//   })
// }
</script>

<template>
  <div class="container">
    <DataTable :titleText :fieldInfo :apiUrl v-model:tableData="coupons">
      <template #tableCell="{ fieldName, hasData, dataIndex }">
        <div v-if="fieldName == 'start_time' && hasData">
          {{ coupons[dataIndex]["start_time"].replace("T", " ") }}
        </div>
        <div v-if="fieldName == 'end_time' && hasData">
          {{ coupons[dataIndex]["end_time"].replace("T", " ") }}
        </div>
        <!-- <div v-if="fieldName == 'operate' && hasData">
          <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goGameEdit(dataIndex)" v-tooltip="'編輯會員'"></i>
        </div> -->
      </template>
    </DataTable>
    <FunctionBall :functionList />
  </div>
</template>
