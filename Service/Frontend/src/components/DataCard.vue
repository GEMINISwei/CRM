<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { setStatusFlag } from '@/composables/globalUse'
import { callApi } from '@/composables/api'
import type { DataObject, DataCardField } from '@/type'

// DataTable Props Interface
interface DataTableProps {
  titleText?: string
  fieldInfo: DataCardField[]
  apiUrl?: string,
  urlQuery?: DataObject,
  cardClick?: Function,
}

// DataTable Props Define & Default
const props = withDefaults(defineProps<DataTableProps>(), {
  titleText: '',
  apiUrl: '',
  urlQuery: undefined,
  cardClick: undefined,
})

// DataTable Sync Props Define
const tableData = defineModel<DataObject>('tableData', { required: true })

const currentPage = ref<number>(1)
const maxPage = ref<number>(1)

const cardCount = computed<number>(() => {
  return Math.ceil(tableData.value.length / 3) * 3
})

const searchField = computed<DataCardField[]>(() => {
  return props.fieldInfo.filter(field => field.canSearch)
})

const searchVal = reactive<DataObject>(searchField.value.reduce((accu, curr) => {
  return { ...accu, [curr.depValue]: '' }
}, {}))

// DataTable Slot Define
const slots = defineSlots<{
  tableCell?(props: {
    fieldName: string,
    hasData: boolean,
    dataIndex: number,
  }): any,
}>()

onMounted(() => {
  searchData()
})

const getTableData = (queryData?: string): void => {
  if (props.apiUrl != '') {
    let getUrlWithQuery: string = `${props.apiUrl}?count=100&page=${currentPage.value}`

    setStatusFlag('loading', true)

    if (queryData !== undefined) {
      getUrlWithQuery += queryData
    }

    callApi('get', getUrlWithQuery)
      .then((res: any) => {
        console.log(res)
        tableData.value = res.data
        maxPage.value = res.info.pageCount > 0 ? res.info.pageCount : 1; // 沒資料顯示第一頁

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
        convertResult = data[fieldName].join(', ')
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

const getCardTitle = (index: number): string => {
  let titleResult = ''

  if (tableData.value[index]) {
    titleResult = tableData.value[index][props.fieldInfo[0].depValue]
  }

  return titleResult
}

</script>

<template>
  <div class="container">
    <div class="d-flex mt-4 ms-5 me-5">
      <h2 class="col-4 ms-4">{{ props.titleText }}</h2>
      <div class="col-8 d-flex justify-content-end">
        <div v-for="(search, searchIndex) in searchField" :key="searchIndex" class="mx-3 my-auto">
          <input class="form-control" type="text" :placeholder="search.label" v-model="searchVal[search.depValue]" @keyup.enter="searchData(true)">
        </div>
      </div>
    </div>
    <div class="d-flex flex-wrap justify-content-center">
      <div v-for="i in cardCount" :key="i" :class="`card m-3 ${i > tableData.length ? 'invisible' : ''}`">
        <div class="card-header" :role="`${typeof props.cardClick === 'function' ? 'button' : ''}`" @click="props.cardClick?.(i - 1)">
          <h3 class="text-center">{{ getCardTitle(i - 1) }}</h3>
        </div>
        <div class="card-body">
          <div v-for="(field, fieldIndex) in fieldInfo" :key="field.label" class="container d-flex column card-field-data">
            <template v-if="fieldIndex > 0">
              <span class="col-3 text-center">{{ field.label }}</span>
              <slot
                name="tableCell"
                :fieldName="field.depValue"
                :hasData="(i - 1) < tableData.length"
                :dataIndex="i - 1"
              >
                <span>{{ tableTextConvert(tableData[i - 1], field.depValue) }}</span>
              </slot>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div v-if="maxPage > 1" class="d-flex justify-content-center mt-3">
      <nav>
        <ul class="pagination">
          <li class="page-item" role="button" @click="goPrevPage()">
            <span class="page-link">&laquo;</span>
          </li>
          <li v-for="i in maxPage" :key="i" class="page-item" role="button" @click="">
            <span :class="`page-link ${ currentPage == i ? 'active' : ''}`">{{ i }}</span>
          </li>
          <li class="page-item" role="button" @click="goNextPage()">
            <span class="page-link">&raquo;</span>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.card {
  width: 30%;
  min-width: 320px;
}

:slotted(span) {
  flex: 0 0 auto;
  width: 75%;
  text-align: center;
}
</style>
