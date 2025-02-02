<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { setStatusFlag, statusFlag } from '@/composables/globalUse.ts'
import { callApi } from '@/composables/api.ts'
import type { DataObject, DataTableField } from '@/type.d.ts'

// DataTable Props Interface
interface DataTableProps {
  titleText?: string
  dataCount?: number
  fieldInfo: DataTableField[]
  apiUrl?: string
  urlQuery?: DataObject
  containerSize?: string
}

// DataTable Props Define & Default
const props = withDefaults(defineProps<DataTableProps>(), {
  titleText: '',
  dataCount: 10,
  apiUrl: '',
  urlQuery: undefined,
  containerSize: ''
})

// DataTable Sync Props Define
const tableData = defineModel<DataObject[]>('tableData', { required: true })

const currentPage = ref<number>(1)
const maxPage = ref<number>(1)
const modalTitle = ref<string>('')
const modalInfo = ref([])

const searchField = computed<DataTableField[]>(() => {
  return props.fieldInfo.filter(field => field.canSearch)
})

const searchVal = reactive<DataObject>(searchField.value.reduce((accu, curr) => {
  return { ...accu, [curr.depValue]: '' }
}, {}))

// DataTable Slot Define
const slots = defineSlots<{
  tableCell?(props: {
    fieldName: string,
    // cellText: string,
    hasData: boolean,
    dataIndex: number,
  }): any,
}>()

onMounted(() => {
  searchData()
})

watch(() => statusFlag.dataNeedUpdate, (status: boolean) => {
  if (status) {
    searchData()
  }
})

const getTableData = (queryData?: string): void => {
  if (props.apiUrl != '') {
    let getUrlWithQuery: string = `${props.apiUrl}?count=${props.dataCount}&page=${currentPage.value}`

    setStatusFlag('loading', true)

    if (queryData !== undefined) {
      getUrlWithQuery += queryData
    }

    callApi('get', getUrlWithQuery)
      .then((res: any) => {
        console.log(res)
        tableData.value = res.data
        maxPage.value = res.info.pageCount > 0 ? res.info.pageCount : 1; // 沒資料顯示第一頁

        setStatusFlag('dataNeedUpdate', false)
        setStatusFlag('loading', false)
      })
  }
}

const tableTextConvert = (data: DataObject, fieldName: string): string => {
  let convertResult: string = '-'

  switch (typeof data?.[fieldName]) {
    case 'boolean':
      if (data?.[fieldName] === true) {
        convertResult = 'Y'
      } else if (data?.[fieldName] === false) {
        convertResult = 'N'
      }
      break

    case 'number':
      convertResult = `${data?.[fieldName]}`
      break

    case 'string':
      convertResult = data?.[fieldName]
      break

    case 'object':
      if (Array.isArray(data[fieldName]) && data[fieldName].length > 0) {
        convertResult = data[fieldName][0]
        // convertResult = data[fieldName].join(', ')
      }
      break
  }

  return convertResult
}
const goPrevPage = (): void => {
  if (currentPage.value > 1) {
    currentPage.value -= 1
    searchData()
  }
}
const goNextPage = (): void => {
  if (currentPage.value < maxPage.value) {
    currentPage.value += 1
    searchData()
  }
}
const goSpecificPage = (pageNum: number): void => {
  currentPage.value = pageNum
  searchData()
}
const searchData = (isGoFirst: boolean = false) => {
  let queryData: string = ''

  if (props.urlQuery) {
    Object.keys(props.urlQuery).forEach((fieldName: string) => {
      queryData += `&${fieldName}=${props.urlQuery?.[fieldName]}`
    })
  }

  Object.keys(searchVal).forEach((fieldName: string) => {
    if (searchVal[fieldName].length > 0) {
      queryData += `&${fieldName}=${searchVal[fieldName]}`
    }
  })

  if (isGoFirst) {
    currentPage.value = 1
  }

  if (queryData.length > 0) {
    getTableData(queryData)
  } else {
    getTableData()
  }
}

const isDataArray = (data: any): boolean => {
  return Array.isArray(data) && data.length > 0
}
const showArrayData = (fieldName: string, data: any): void => {
  let matchedField = props.fieldInfo.find((field: DataTableField) => field.depValue == fieldName)

  modalTitle.value = matchedField ? matchedField.label : ''
  modalInfo.value = data[fieldName]

  setStatusFlag('modalShow', true)
}
</script>

<template>
  <div :class="`container${containerSize ? `-${containerSize}`: ''}`">
    <div class="d-flex mt-4 ms-5 me-5">
      <h2 class="col-4 ms-4">{{ props.titleText }}</h2>
      <div class="col-8 d-flex justify-content-end">
        <div v-for="(search, searchIndex) in searchField" :key="searchIndex" class="mx-3 my-auto">
          <input class="form-control" type="text" :placeholder="search.label" v-model="searchVal[search.depValue]" @keyup.enter="searchData(true)">
        </div>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <table class="table table-primary">
        <thead>
          <tr>
            <th v-for="field in fieldInfo" :key="field.label" :width="field.width">
              <span>{{ field.label }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in tableData" :key="index">
            <td v-for="field in fieldInfo" :key="field.label" :style="data.customStyle">
              <slot name="tableCell"
                :fieldName="field.depValue"
                :hasData="index < tableData.length"
                :dataIndex="index"
              >
                <span v-if="isDataArray(data[field.depValue]) && data[field.depValue].length > 1" class="text-primary" role="button" @click="showArrayData(field.depValue, data)">
                  {{ tableTextConvert(data, field.depValue) }}
                </span>
                <span v-else>
                  {{ tableTextConvert(data, field.depValue) }}
                </span>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="maxPage > 1" class="d-flex justify-content-center">
      <nav>
        <ul class="pagination">
          <li class="page-item" role="button" @click="goPrevPage()">
            <span class="page-link">&laquo;</span>
          </li>
          <li v-for="i in maxPage" :key="i" class="page-item" role="button" @click="goSpecificPage(i)">
            <span :class="`page-link ${ currentPage == i ? 'active' : ''}`">{{ i }}</span>
          </li>
          <li class="page-item" role="button" @click="goNextPage()">
            <span class="page-link">&raquo;</span>
          </li>
        </ul>
      </nav>
    </div>
  </div>

  <Teleport to="#modal-header">
    <h3>{{ modalTitle }}</h3>
  </Teleport>
  <Teleport to="#modal-body">
    <div class="d-flex justify-content-center row">
      <p v-for="info in modalInfo" :key="info" class="text-center">
        {{ info }}
      </p>
    </div>
  </Teleport>
</template>

<style lang="scss" scoped>
table {
  width: 90%;
  margin: 20px;
  border: 1px #a39485 solid;
  font-size: 1rem;
  border-collapse: collapse;
  border-radius: 10px;
  overflow: hidden;
}

td, th {
  text-align: center;
  padding: 1em .5em;
  vertical-align: middle;
}

td {
  background: #fff;
}

@media all and (max-width: 768px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }

  th {
    text-align: right;
  }

  table {
    position: relative;
    padding-bottom: 0;
    border: none;
  }

  thead {
    float: left;
    white-space: nowrap;
  }

  tbody {
    overflow-x: auto;
    overflow-y: hidden;
    position: relative;
    white-space: nowrap;
  }

  tr {
    display: inline-block;
    vertical-align: top;
  }
}
</style>
