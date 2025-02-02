<script setup lang="ts">
import { onMounted, watch } from 'vue';
import CustomInput from '@/components/CustomInput.vue';
import CustomSelect from '@/components/CustomSelect.vue';
import CustomTextarea from '@/components/CustomTextarea.vue';
import CustomSearchList from '@/components/CustomSearchList.vue';
import type { DataObject, CustomFormField, CustomFormButton } from '@/type'

interface CustomFormProps {
  fields: CustomFormField[]
  columnGap?: number
  colSize?: number
  colOffset?: number
  textPos?: string
  btnPos?: string
  buttons?: CustomFormButton[]
  hasStep?: boolean
  currentStep?: number
}

// FieldInput Props Define & Default
const props = withDefaults(defineProps<CustomFormProps>(), {
  columnGap: 4,
  colSize: 8,
  colOffset: 2,
  textPos: 'center',
  btnPos: 'center',
  buttons: () => [] as CustomFormButton[],
  hasStep: false,
  currentStep: 0,
})

// FieldInput Sync Props Define
const formData = defineModel<DataObject>('formData', { required: true })

onMounted(() => {
  props.fields.forEach((field: CustomFormField) => {
    setFieldToForm(field.depValue)
  })
})

watch(() => props.fields, (newVal) => {
  newVal.forEach((field: CustomFormField) => {
    setFieldToForm(field.depValue)
  })
})

const setFieldToForm = (fieldName: string): void => {
  if (formData.value[fieldName] === undefined) {
    formData.value[fieldName] = ''
  }
}
</script>

<template>
  <form :class="`row g-${props.columnGap}`" novalidate @submit.prevent="">
    <div
      v-for="field in props.fields"
      :key="field.depValue"
      :class="`col-md-${props.colSize} offset-${props.colOffset} form-floating`"
      :style="`${field.hidden ? 'display: none' : '' }`"
    >
      <template v-if="!props.hasStep || (props.hasStep && field.step == props.currentStep)">
        <template v-if="field.type == 'textarea'">
          <CustomTextarea
            :label="field.label"
            :required="field.required"
            :disabled="field.disabled"
            :hidden="field.hidden"
            :textPos="props.textPos"
            :rows="field.rows"
            v-model:inputData="formData[field.depValue]"
          />
        </template>
        <template v-else-if="field.type == 'select'">
          <CustomSelect
            :label="field.label"
            :required="field.required"
            :disabled="field.disabled"
            :hidden="field.hidden"
            :textPos="props.textPos"
            :options="field.options"
            v-model:inputData="formData[field.depValue]"
          />
        </template>
        <template v-else-if="field.type == 'searchList'">
          <CustomSearchList
            :label="field.label"
            :required="field.required"
            :disabled="field.disabled"
            :hidden="field.hidden"
            :textPos="props.textPos"
            :options="field.options"
            v-model:inputData="formData[field.depValue]"
          />
        </template>
        <template v-else>
          <CustomInput
            :label="field.label"
            :type="field.type"
            :required="field.required"
            :disabled="field.disabled"
            :hidden="field.hidden"
            :textPos="props.textPos"
            v-model:inputData="formData[field.depValue]"
          />
        </template>
        <div class="text-center">
          {{ field.description }}
        </div>
      </template>
    </div>
    <div v-if="props.buttons.length > 0" :class="`d-flex justify-content-${props.btnPos}`">
      <div v-for="(btn, index) in props.buttons" :key="index" class="d-flex justify-content-center m-2 mt-4">
        <template v-if="!props.hasStep || (props.hasStep && btn.step == props.currentStep)">
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
