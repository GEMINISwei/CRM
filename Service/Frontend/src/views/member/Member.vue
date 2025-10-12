<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { goPage } from '@/router'
import { callApi } from '@/composables/api'
import { createNotify } from '@/composables/notify'
import { pageParameters, setPageParams, setStatusFlag } from '@/composables/globalUse'
import DataTable from '@/components/DataTable.vue'
import FunctionBall from '@/components/FunctionBall.vue'
import CustomSelect from '@/components/CustomSelect.vue'
import CustomInput from '@/components/CustomInput.vue'
import type { DataTableField, DataObject, OptionObject, FuncListItem } from '@/type'

const fieldInfo: DataTableField[] = [
  { label: '首次交流日期', depValue: 'first_communication_time', width: '15%' },
  { label: '遊戲暱稱', depValue: 'players', width: '15%', canSearch: true },
  { label: '交流方式', depValue: 'first_communication_way', width: '15%' },
  { label: '銀行帳戶', depValue: 'accounts', width: '20%', canSearch: true },
  { label: '電話 / 手機號碼', depValue: 'phones', width: '15%', canSearch: true },
  { label: '操作', depValue: 'operate', width: '20%' },
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

const playersList = ref<DataObject[]>([])
const currentPlayer = ref<string>('')
const currentPlayerName = ref<string>('')

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

const goMemberAddPlayer = (index: number) => {
  goPage('/members/add_player', {
    editId: members.value[index]['id']
  })
}

const goMemberPhones = (index: number) => {
  goPage('/members/edit_phones', {
    editId: members.value[index]['id']
  })
}

const goPlayerRecord = (index: number) => {
  goPage('/members/player_record', {
    memberId: members.value[index].id,
    memberName: members.value[index].player[0].name,
  })
}

const goSelectGame = (): void => {
  selectedGame.value = ''
}

const showPlayers = (index: number): void => {
  playersList.value = members.value[index]['players']
  setStatusFlag('modalShow', true)
}

const editPlayerName = (info: DataObject): void => {
  currentPlayer.value = info['id']
  currentPlayerName.value = info['name']

  setStatusFlag('modalShow', false)
  setStatusFlag('modalShow2', true)
}

const updatePlayerName = (): void => {
  let playerUpdateInfo = {
    name: currentPlayerName.value
  }

  callApi('patch', `/apis/players/${currentPlayer.value}`, playerUpdateInfo)
    .then(() => {
      currentPlayer.value = ''
      currentPlayerName.value = ''
      setStatusFlag('dataNeedUpdate', true)
      createNotify('success', '已更新遊戲暱稱 !')
      setStatusFlag('modalShow2', false)
    })
}

const deletePlayerName = (): void => {
  callApi('delete', `/apis/players/${currentPlayer.value}`)
    .then(() => {
      setStatusFlag('dataNeedUpdate', true)
      createNotify('success', '已刪除遊戲暱稱 !')
    })
    .catch((err: any) => {
      if (err.status == 404) {
        createNotify('error', `此為建立時之主要遊戲暱稱, 不可刪除 !`)
      }
    })
    .finally(() => {
      currentPlayer.value = ''
      currentPlayerName.value = ''
      setStatusFlag('modalShow2', false)
    })
}
</script>

<template>
  <template v-if="selectedGame">
    <DataTable :titleText :fieldInfo :apiUrl :urlQuery :containerSize :dataCount="9" v-model:tableData="members">
      <template #tableCell="{ fieldName, dataIndex }">
        <div v-if="fieldName == 'players'">
          <span class="text-primary" role="button" @click="showPlayers(dataIndex)">
            {{ members[dataIndex]['players'][0]['name'] }}
          </span>
        </div>
        <div v-if="fieldName == 'first_communication_time'">
          {{ members[dataIndex]['first_info']['communication_time'] ? members[dataIndex]['first_info']['communication_time'].slice(0, 10) : " - " }}
        </div>
        <div v-if="fieldName == 'first_communication_way'">
          {{ members[dataIndex]['first_info']['communication_way'] ? members[dataIndex]['first_info']['communication_way'].slice(0, 10) : " - " }}
        </div>
        <div v-if="fieldName == 'operate'">
          <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="goMemberEdit(dataIndex)" v-tooltip="'編輯會員'"></i>
          <i class="bi-bank text-primary fs-4 mx-2" role="button" @click="goMemberAccounts(dataIndex)" v-tooltip="'編輯帳戶'"></i>
          <i class="bi-people-fill text-primary fs-4 mx-2" role="button" @click="goMemberAddPlayer(dataIndex)" v-tooltip="'新增分身'"></i>
          <i class="bi-phone text-primary fs-4 mx-2" role="button" @click="goMemberPhones(dataIndex)" v-tooltip="'編輯手機'"></i>
          <i class="bi-list-ul text-primary fs-4 mx-2" role="button" @click="goPlayerRecord(dataIndex)" v-tooltip="'出入金紀錄'"></i>
        </div>
      </template>
    </DataTable>
  </template>
  <div v-else id="member-page-select-body" class="container">
    <h3>會員列表</h3>
    <h3>請選擇遊戲類別</h3>
    <div class="col-6 mt-2">
      <CustomSelect type="select" :options="gameOptions" v-model:inputData="selectedGame" />
    </div>
  </div>

  <FunctionBall :functionList />

  <Teleport to="#modal-header">
    <h3>遊戲暱稱列表</h3>
  </Teleport>
  <Teleport to="#modal-body">
    <div class="d-flex justify-content-center row">
      <div v-for="player in playersList" :key="player.id" class="text-center">
        <span >{{ player.name }}</span>
        <i class="bi-pencil-square text-primary fs-4 mx-2" role="button" @click="editPlayerName(player)"></i>
      </div>
    </div>
  </Teleport>

  <Teleport to="#modal-header-2">
    <h3>編輯遊戲暱稱</h3>
  </Teleport>
  <Teleport to="#modal-body-2">
    <div class="d-flex justify-content-center row">
      <CustomInput type="text" v-model:inputData="currentPlayerName" />
      <div class="d-flex flex-row justify-content-center">
        <button class="btn btn-primary mx-2 my-4" type="button" @click="updatePlayerName()">儲存</button>
        <button class="btn btn-danger mx-2 my-4" type="button" @click="deletePlayerName()">刪除</button>
      </div>
    </div>
  </Teleport>
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
