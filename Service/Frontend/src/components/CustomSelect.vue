<script setup lang="ts">
import type { OptionObject, CustomSelectProps } from '@/type'

const props = withDefaults(defineProps<CustomSelectProps>(), {
  label: '',
  required: false,
  disabled: false,
  hidden: false,
  textPos: 'center',
  options: () => [] as OptionObject[]
})
const inputData = defineModel<any>('inputData', { required: true })
</script>

<template>
  <template v-if="!props.hidden">
    <select
      :class="`form-select text-${props.textPos}`"
      :required="props.required"
      :disabled="props.disabled"
      :hidden="props.hidden"
      v-model="inputData"
    >
      <option
        v-for="option in props.options"
        :key="option.value"
        :value="option.value"
        :selected="inputData == option.value"
      >
        {{ option.text }}
      </option>
    </select>
    <label
      v-if="props.label"
    >
      {{ (props.required ? '* ' : '') + props.label }}
    </label>
  </template>
</template>

<style lang="scss" scoped>
select.text-center {
  text-align: center;
  text-align-last: center;
}
</style>
