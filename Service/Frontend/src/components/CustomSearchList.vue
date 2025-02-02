<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { OptionObject, CustomSearchListProps } from '@/type'

const props = withDefaults(defineProps<CustomSearchListProps>(), {
  label: '',
  required: false,
  disabled: false,
  hidden: false,
  textPos: 'center',
  options: () => [] as OptionObject[]
})
const inputData = defineModel<any>('inputData', { required: true })

const inputElem = ref<HTMLElement>()
const listBlock = ref<HTMLElement>()
const searchString = ref<string>('')
const inputShowData = ref<string>('')
const isListOpen = ref<boolean>(false)

onMounted(() => {
  listCreate()
})
onUnmounted(() => {
  document.removeEventListener('click', docClickEvent)
})

const listCreate = () => {
  let  matchedOption = props.options.find((option: OptionObject) => option.value == inputData.value)

  inputElem.value?.addEventListener('click', () => {
    isListOpen.value = true
  })

  inputElem.value?.addEventListener('input', (e: any) => {
    searchString.value = e.target.value
  })

  listBlock.value?.addEventListener("click", (e: any) => {
    if (e.target.nodeName.toLocaleLowerCase() === "li") {
      inputShowData.value = e.target.innerText
      searchString.value = e.target.innerText
      inputData.value = e.target.getAttribute('value')
      isListOpen.value = false
    }
  })

  document.addEventListener('click', docClickEvent)

  if (inputData.value) {
    searchString.value = matchedOption ? matchedOption.text : ''
    inputShowData.value = searchString.value
  }
}

const docClickEvent = (e: any) => {
  if (isListOpen.value && e.target != inputElem.value) {
    let hasMatched = props.options.find((option: OptionObject) => option.text == searchString.value)

    if (!hasMatched) {
      inputData.value = ''
      searchString.value = ''
      inputShowData.value = ''
    }

    isListOpen.value = false
  }
}
</script>

<template>
  <template v-if="!props.hidden">
    <input
      ref="inputElem"
      :class="`custom-list form-control text-${props.textPos}`"
      type="text"
      :required="props.required"
      :disabled="props.disabled"
      :hidden="props.hidden"
      v-model="inputShowData"
    >
    <label
      v-if="props.label"
    >
      {{ (props.required ? '* ' : '') + props.label }}
    </label>
    <ul ref="listBlock" v-show="isListOpen">
      <li
        v-for="option in props.options"
        v-show="option.text.includes(searchString)"
        :key="option.value"
        :class="`text-${props.textPos}`"
        role="button"
        :value="option.value"
      >
        {{ option.text }}
      </li>
    </ul>
  </template>
</template>


<style lang="scss" scoped>
ul {
	position: absolute;
  margin: 0 0.75rem;
	padding: 0;
	width: calc(100% - 1.5rem);
	top: 100%;
	left: 0;
	list-style: none;
	border-radius: 2px;
	background: var(--bs-body-bg);
	overflow: hidden;
	overflow-y: auto;
	z-index: 100;
  border: var(--bs-border-width) solid var(--bs-border-color);
  border-radius: var(--bs-border-radius);
}

li {
	display: block;
	background: var(--bs-body-bg);

  &:hover {
    color: var(--bs-body-bg);
	  background: var(--bs-link-hover-color);
  }
}
</style>
