<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import CustomInput from '@/components/CustomInput.vue';
import CustomSelect from '@/components/CustomSelect.vue';
import CustomSearchList from '@/components/CustomSearchList.vue';
import CustomTextarea from '@/components/CustomTextarea.vue';
import type { BaseFormProps, BaseFormFields, BaseFormButton, DataObject } from '@/type'


const props = withDefaults(defineProps<BaseFormProps>(), {
  columnGap: 4,
  colSize: 8,
  colOffset: 2,
  textPos: 'center',
  btnPos: 'center',
})
const fields = defineModel<BaseFormFields>('fields', { required: true })
const formData = defineModel<DataObject>('formData', { required: true })
const buttons = defineModel<BaseFormButton[]>('buttons', { required: true })
const descriptions = reactive<DataObject>({})


// 處理 field props 並給予預設值
onMounted(() => {
  Object.keys(fields.value).forEach(depValue => {
    fields.value[depValue].label = fields.value[depValue].label ?? ''
    fields.value[depValue].required = fields.value[depValue].required ?? false
    fields.value[depValue].disabled = fields.value[depValue].disabled ?? false
    fields.value[depValue].hidden = fields.value[depValue].hidden ?? false

    descriptions[depValue] = fields.value[depValue].description ?? ''
  })
})
</script>

<template>
  <form :class="`row g-${props.columnGap}`" novalidate @submit.prevent="">
    <div
      v-for="(field, depValue) in fields"
      :key="depValue"
      :class="`col-md-${props.colSize} offset-${props.colOffset} form-floating`"
      :style="`${field.hidden ? 'display: none' : '' }`"
    >
      <template v-if="!field.hidden">
        <template v-if="field.type == 'select'">
          <CustomSelect
            v-bind="field"
            v-model:inputData="formData[depValue]"
            :textPos="props.textPos"
          />
        </template>
        <template v-else-if="field.type == 'searchList'">
          <CustomSearchList
            v-bind="field"
            v-model:inputData="formData[depValue]"
            :textPos="props.textPos"
          />
        </template>
        <template v-else-if="field.type == 'textarea'">
          <CustomTextarea
            v-bind="field"
            v-model:inputData="formData[depValue]"
            :textPos="props.textPos"
          />
        </template>
        <template v-else>
          <CustomInput
            v-bind="field"
            v-model:inputData="formData[depValue]"
            :textPos="props.textPos"
          />
        </template>
        <div class="text-center">
          {{ descriptions[depValue] }}
        </div>
      </template>
    </div>
    <div v-if="buttons.length > 0" :class="`d-flex justify-content-${props.btnPos}`">
      <div v-for="(btn, btn_index) in buttons" :key="btn_index" class="d-flex justify-content-center m-2 mt-4">
        <template v-if="!btn.hidden">
          <template v-if="btn.needValid">
            <button :class="`btn btn-${btn.color}`" type="button" v-validClick="btn.method">{{ btn.text }}</button>
          </template>
          <template v-else>
            <button :class="`btn btn-${btn.color}`" type="button" @click="btn.method()">{{ btn.text }}</button>
          </template>
        </template>
      </div>
    </div>
  </form>
</template>
