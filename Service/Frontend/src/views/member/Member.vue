<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { pageParameters, setPageParams } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import type { DataTableField, DataObject, OptionObject, FuncListItem } from '@/type'

const fieldInfo: DataTableField[] = [
  { label: '首次交流日期', depValue: 'first_communication_time', width: '15%' },
  { label: '遊戲暱稱', depValue: 'nickname', width: '15%', canSearch: true },
  { label: '交流方式', depValue: 'first_communication_way', width: '10%' },
  { label: '銀行帳戶', depValue: 'accounts', width: '20%', canSearch: true },
  { label: '遊戲分身', depValue: 'sock_puppets', width: '10%', canSearch: true },
  { label: '電話 / 手機號碼', depValue: 'phones', width: '15%', canSearch: true },
  { label: '操作', depValue: 'operate', width: '15%' },
]
const apiUrl: string = '/apis/members'
const urlQuery = computed<DataObject>(() => {
  return {
    'game_id': selectedGame.value
  }
})
const containerSize: string = 'fluid'
const members = ref([] as DataObject[])
const selectedGame = ref<string>('')
const gameOptions = ref<OptionObject[]>([])

const titleText = computed<string>(() => {
  let selectedGameName = gameOptions.value.find((option: OptionObject) => option.value == selectedGame.value)

  return `會員列表 (${selectedGameName?.text})`
})

// FunctionBall Props Setting
const functionList: FuncListItem[] = [
  { text: '新增會員', icon: 'plus-square', goPath: '/members/new' },
  { text: '選擇遊戲', icon: 'arrow-return-left', method: () => goSelectGame() },
]

onMounted(() => {
  getGameList()

  selectedGame.value = pageParameters.members?.gameId
})

watch(selectedGame, (newVal: string) => {
  setPageParams('members', {
    'gameId': newVal
  })
})

const getGameList = (): void => {
  callApi('get', '/apis/games')
    .then((resData: any) => {
      gameOptions.value = resData.list_data.map((x: any) => {
        return {
          text: x['name'],
          value: x['id'],
        }
      })
    })
}

const goMemberEdit = (index: number) => {
  goPage('/members/edit', {
    editId: members.value[index]['id']
  })
}

const goMemberAccounts = (index: number) => {
  goPage('/members/edit_accounts', {
    editId: members.value[index]['id']
  })
}

const goMemberSockPuppets = (index: number) => {
  goPage('/members/edit_sock_puppets', {
    editId: members.value[index]['id']
  })
}

const goMemberPhones = (index: number) => {
  goPage('/members/edit_phones', {
    editId: members.value[index]['id']
  })
}

const goSelectGame = (): void => {
  selectedGame.value = ''
}
</script>

<template>
  <template v-if="selectedGame">
    <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize :dataCount="9" v-model:tableData="members">
      <template #tableCell="{ fieldName, dataIndex }">
        <div v-if="fieldName == 'first_communication_time'">
          {{ members[dataIndex][fieldName] ? members[dataIndex][fieldName].slice(0, 10) : " - " }}
        </div>
        <div v-if="fieldName == 'operate'">
          <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goMemberEdit(dataIndex)" v-tooltip="'編輯會員'"></i>
          <i class="bi-bank text-primary fs-4 mx-2" role="button" @click="goMemberAccounts(dataIndex)" v-tooltip="'編輯帳戶'"></i>
          <i class="bi-people-fill text-primary fs-4 mx-2" role="button" @click="goMemberSockPuppets(dataIndex)" v-tooltip="'編輯分身'"></i>
          <i class="bi-phone text-primary fs-4 mx-2" role="button" @click="goMemberPhones(dataIndex)" v-tooltip="'編輯手機'"></i>
        </div>
      </template>
    </DataTable>
  </template>
  <div v-else id="member-page-select-body" class="container">
    <h3>會員列表</h3>
    <h3>請選擇遊戲類別</h3>
    <div class="col-6 mt-2">
      <CustomSelect :options="gameOptions" v-model:inputData="selectedGame" />
    </div>
  </div>
  <FunctionBall :functionList />
</template>

<style lang="scss" scoped>
#member-page-select-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
}
</style>
