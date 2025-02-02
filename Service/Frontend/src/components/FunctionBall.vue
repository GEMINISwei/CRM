<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { FuncListItem } from '@/type.d.ts'

// Interface Define
interface FunctionBallProps {
  functionList: FuncListItem[]
}

// FunctionBall Props Define & Default
const props = withDefaults(defineProps<FunctionBallProps>(), {
  // All Props Required
})

// FunctionBall Component Use
const router = useRouter()
const isListOpen = ref(false)
const btnClass = computed(() => {
  return {
    'list-container': true,
    'active': isListOpen.value,
  }
})

const BtnListSettingChange = (): void => {
  isListOpen.value = !isListOpen.value
}
const useListFunction = (index: number): void => {
  if (props.functionList[index].goPath!) {
    router.push({ path: props.functionList[index].goPath })
  } else {
    props.functionList[index].method?.()
  }

  BtnListSettingChange()
}
</script>

<template>
  <div :class="btnClass">
    <button class="more-button" aria-label="Menu Button" @click="BtnListSettingChange">
      <div class="menu-icon-wrapper">
        <div class="menu-icon-line half first"></div>
        <div class="menu-icon-line"></div>
        <div class="menu-icon-line half last"></div>
      </div>
    </button>
    <ul class="more-button-list">
      <li v-for="(info, index) in props.functionList" :key="index" class="more-button-list-item" @click="useListFunction(index)">
        <i :class="`bi-${info.icon} fs-5`"></i>
        <span>{{ info.text }}</span>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
$body-bg: #84a0f4;
$button-bg: #5c67ff;
$list-bg: #fff;
$text-color: #1c3991;
$text-color-hover: #5c67ff;
$menu-icon-transition: transform 300ms cubic-bezier(0.52, -0.80, 0.52, 0.52);

body {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $body-bg;
  background-image: linear-gradient(to top, #84a0f4 0%, #c2e9fb 100%);
}

.list-container {
  position: absolute;
  right: 20px;
  bottom: 20px;

  &.active {
    .more-button-list {
       opacity: 1;
       transform: scale(1);
    }

    .more-button-list-item {
      animation: fadeInItem .6s .2s forwards;

      @for $i from 2 to 7 {
        &:nth-child(#{$i}) { animation-delay: .2s * $i; }
      }
    }

    .more-button {
      animation: onePulse .6s forwards linear;
    }

    .menu-icon-wrapper {
      transform: rotate(-45deg);
    }

    .menu-icon-line {
      &.first {
        transform: rotate(-90deg) translateX(1px);
      }

      &.last {
        transform: rotate(-90deg) translateX(-1px);
      }
    }
  }
}

.more-button {
  background-color: $button-bg;
  box-shadow: 0px 0px 0px 4px rgba(92,103,255,0.3);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: .2s ease-in;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  position: relative;
  z-index: 2;

  &:hover, &:focus {
    box-shadow: 0px 0px 0px 8px rgba(92,103,255,0.3);
    background-color: darken($button-bg,4%);
  }

  &:focus { outline: 0; }

  &-list {
    background-color: $list-bg;
    border-radius: 8px;
    list-style-type: none;
    min-width: 120px;
    // max-width: 200px;
    box-shadow: 0px 0px 4px 4px rgba(150, 157, 249, 0.16);
    padding: 0;
    padding: 6px;
    position: absolute;
    right: 24px;
    bottom: 0;
    opacity: 0;
    transform: scale(0);
    transform-origin: bottom right;
    transition : all .3s ease .1s;

    li { opacity: 0; }
  }

  &-list-item {
    display: flex;
    align-items: center;
    color: $text-color;
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    position: relative;
    transition: .2s ease-in;
    transform: translatex(-10px);

    &:hover { color: $text-color-hover; }

    &:after {
      content: '';
      position: absolute;
      height: 1px;
      width: calc(100% - 24px);
      left: 12px;
      bottom: 0;
      background-color: rgba(132, 160, 244, 0.1);
    }
    &:last-child:after { display: none; }

    svg {
      width: 18px;
      height: 18px;
    }

    span {
      display: inline-block;
      text-wrap: nowrap;
      line-height: 20px;
      font-size: 14px;
      margin-left: 8px;
    }
  }
}

@keyframes onePulse {
  0% {
    box-shadow: 0px 0px 0px 0px rgba(92,103,255,0.3);
  }

  50% {
    box-shadow: 0px 0px 0px 12px rgba(92,103,255,0.1);
  }

  100% {
    box-shadow: 0px 0px 0px 4px rgba(92,103,255,0.3);
  }
}

@keyframes fadeInItem {
  100% {
    transform: translatex(0px);
    opacity: 1;
  }
}

.menu-icon-wrapper {
  border-radius: 2px;
  width: 20px;
  height: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: transform 330ms ease-out;
}

.menu-icon-line {
  background-color: #fff;
  border-radius: 2px;
  width: 100%;
  height: 2px;

  &.half { width: 50%;}

  &.first {
    transition: $menu-icon-transition;
    transform-origin: right;
  }

  &.last {
    align-self: flex-end;
    transition: $menu-icon-transition;
    transform-origin: left;
  }
}
</style>
