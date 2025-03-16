<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { goPage } from '@/router'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import type { DataObject, DataTableField, FuncListItem } from '@/type'

const apiUrl = ref<string>("/apis/activities")
const activities = ref<DataObject[]>([])

const fieldInfo = reactive<DataTableField[]>([
  { label: '活動名稱', depValue: 'name', width: '15%' },
  { label: '遊戲類別', depValue: 'game_name', width: '10%' },
  { label: '開始時間', depValue: 'start_time', width: '20%' },
  { label: '結束時間', depValue: 'end_time', width: '20%' },
  { label: '滿額條件', depValue: 'money_floor', width: '15%' },
  { label: '贈送遊戲幣', depValue: 'coin_free', width: '10%' },
  { label: '操作', depValue: 'operate', width: '10%' },
])
const operateItems = reactive<DataObject[]>([
  { icon: "bi-pencil-square", color: "primary", text: "編輯活動", method: (index: number) => goActivityEdit(index) }
])
const functionList = reactive<FuncListItem[]>([
  { text: '新增活動', icon: 'plus-square', goPath: '/activities/new' },
])

const titleText = computed<string>(() => {
  return "活動列表"
})

const goActivityEdit = (index: number) => {
  goPage('/activities/edit', {
    editId: activities.value[index]['id']
  })
}

const textTranstion = (field: string, index: number): string => {
  let resultStr = "-"

  switch (field)
  {
    case 'start_time':
      resultStr = activities.value[index][field].replace("T", " ")
      break

    case 'end_time':
      resultStr = activities.value[index][field].replace("T", " ")
      break

    case 'game_name':
      resultStr = activities.value[index]['game'][0]['name']
      break

    default:
      resultStr = activities.value[index][field]
      break
  }

  return resultStr
}
</script>

<template>
  <div class="container">
    <DataTable :titleText :fieldInfo :apiUrl v-model:tableData="activities">
      <template #tableCell="{ fieldName, hasData, dataIndex }">
        <div v-if="fieldName == 'operate' && hasData">
          <i
            v-for="(item, index) in operateItems"
            :key="index"
            :class="`${item.icon} text-${item.color} fs-4 mx-2`"
            role="button"
            @click="item.method(index)"
            v-tooltip="item.text"
          ></i>
        </div>
        <span v-else>{{ textTranstion(fieldName, dataIndex) }}</span>
      </template>
    </DataTable>
    <FunctionBall :functionList />
  </div>
</template>
