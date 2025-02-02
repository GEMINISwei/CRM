<script setup lang="ts">
import type { CustomTextareaProps } from '@/type'

const props = withDefaults(defineProps<CustomTextareaProps>(), {
  label: '',
  required: false,
  disabled: false,
  hidden: false,
  textPos: 'center',
  rows: 3,
})
const inputData = defineModel<any>('inputData', { required: true })
</script>

<template>
  <template v-if="!props.hidden">
    <textarea
      :class="`form-control text-${props.textPos}`"
      :required="props.required"
      :disabled="props.disabled"
      :hidden="props.hidden"
      :rows="props.rows"
      style="height: 100%;"
      v-model="inputData"
    ></textarea>
    <label
      v-if="props.label"
    >
      {{ (props.required ? '* ' : '') + props.label }}
    </label>
  </template>
</template>
