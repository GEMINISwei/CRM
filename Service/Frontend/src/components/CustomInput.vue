<script setup lang="ts">
import { computed } from 'vue'
import type { CustomInputProps } from '@/type'

const props = withDefaults(defineProps<CustomInputProps>(), {
  label: '',
  required: false,
  disabled: false,
  hidden: false,
  textPos: 'center',
})
const inputData = defineModel<any>('inputData', { required: true })

const finalType = computed<string>(() => {
  let typeResult = props.type

  if (props.type == 'float') {
    typeResult = 'number'
  }

  return typeResult
})
</script>

<template>
  <template v-if="!props.hidden">
    <input
      :class="`form-control text-${props.textPos}`"
      :type="finalType"
      :required="props.required"
      :disabled="props.disabled"
      :hidden="props.hidden"
      :step="props.type == 'float' ? '0.001': ''"
      v-model="inputData"
    >
    <label
      v-if="props.label"
    >
      {{ (props.required ? '* ' : '') + props.label }}
  </label>
  </template>
</template>
