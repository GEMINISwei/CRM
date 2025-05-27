<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { callApi } from '@/composables/api'
import CustomSelect from '@/components/CustomSelect.vue'
import type { DataObject, OptionObject } from '@/type'

const hasClicked = ref<boolean>(false)
const itemsInfo = ref<DataObject[]>([])
const resultAward = ref<string>('--')

const awardOptions = ref<OptionObject[]>([
  { text: '頭獎', value: 'one' },
  { text: '二獎', value: 'two' },
  { text: '三獎', value: 'three' },
  { text: '未中獎', value: 'no' },
  { text: '隨機中獎', value: 'random' },
])
const targetAward = ref<string>('')

const getAwardInfo = () => {
  callApi('get', '/apis/settings/award/block')
    .then((resData: any) => {
      let awardInfo = [
        { title: 'oneAward', count: resData['value']['one_award'] },
        { title: 'twoAward', count: resData['value']['two_award'] },
        { title: 'threeAward', count: resData['value']['three_award'] },
        { title: 'noAward', count: resData['value']['no_award'] },
      ]
      let currentAwardText = ''
      let currentRotate = 0

      itemsInfo.value = []

      for (let countIdx = 0; countIdx < 12; countIdx++) {
        let awardIndex = Math.floor(Math.random() * awardInfo.filter(x => x.count).length)
        let awardItem = awardInfo[awardIndex].title

        switch (awardItem) {
          case 'oneAward':
            currentAwardText = '頭獎'
            break

          case 'twoAward':
            currentAwardText = '二獎'
            break

          case 'threeAward':
            currentAwardText = '三獎'
            break

          case 'noAward':
            currentAwardText = '未中獎'
            break
        }

        itemsInfo.value.push(
          { value: awardItem, text: currentAwardText, rotate: currentRotate }
        )

        currentRotate += 30
        awardInfo[awardIndex].count -= 1
        if (awardInfo[awardIndex].count == 0) {
          awardInfo.splice(awardIndex, 1)
        }
      }
    })
}
const playGame = (): void => {
  if (hasClicked.value) return

  let rotate = 0
  let yu = rotate % 60
  let targetElem = document.querySelector('.xuanxiang')

  if (targetAward.value == 'random') {
    let num = Math.floor(Math.random() * 1800 + 360)

    rotate = rotate + num
  } else {
    let matchedItems = itemsInfo.value.filter(x => x.value == `${targetAward.value}Award`)
    let randomIndex = Math.floor(Math.random() * matchedItems.length)
    let randomRotate = matchedItems[randomIndex].rotate

    let targetItemIndex = itemsInfo.value.findIndex(x => x.rotate == randomRotate)
    if (targetItemIndex >= 0) {
      console.log(targetItemIndex)
      let randomNum = Math.floor(Math.random() * 15)
      let direction = Math.random() >= 0.5 ? 1 : -1

      rotate = (12 - targetItemIndex) * 30 + 1800 + randomNum * direction
    }
  }

  if (yu > 10 && yu < 30) rotate -= 20;
  if (yu > 30 && yu < 50) rotate += 20;

  targetElem?.setAttribute('style', `transform: rotate(${rotate}deg)`)

  setTimeout(() => {
    let resultIndex = 11 - Math.floor(((rotate - 15) % 360) / 30)

    resultAward.value = itemsInfo.value[resultIndex].text
  }, 5500)

  hasClicked.value = true
}

onMounted(() => {
  getAwardInfo()
})
</script>

<template>
  <div id="test-page-body">
    <div v-if="targetAward == ''">
      <h3>請選擇中獎目標</h3>
      <CustomSelect type="select" :options="awardOptions" v-model:inputData="targetAward" />
    </div>
    <div v-else>
      <div class="zhu">
        <div class="pan">
          <div class="wai"></div>
          <div class="mao">
          </div>
          <div class="xuanxiang" style="transform: rotate(0deg)">
            <span
              v-for="(item, itemIdx) in itemsInfo"
              :key="itemIdx"
              :style="`transform: rotate(${item.rotate}deg)`"
            >
              <i>{{ item.text }}</i>
            </span>
          </div>
          <div class="nei" @click="playGame()">
            <div class="huan">
              <span>點擊<br/>抽大獎</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <h2 class="d-flex">
      <span class="mx-2 w-50 text-end">中獎品項: </span>
      <span class="mx-2 w-50 text-start">{{ resultAward }}</span>
    </h2>
  </div>
</template>

<style lang="scss" scoped>
#test-page-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(80vh - 56px);
}

.zhu .pan{
  position: absolute;
  top: calc(50% - 200px);
  left: calc(50% - 200px);
  width: 400px;
  height: 400px;
}
.zhu .pan .wai{
  width: 100%;
  height: 100%;
  border-radius: 100%;
  background: #fdc081;
}
.zhu .pan .wai::before{
  content: '';
  display: block;
  width: 86%;
  height: 86%;
  border-radius: 100%;
  position: absolute;
  top: 7%;
  left:  7%;
  background-color: #fff;
}
.zhu .pan .wai span{
  display: block;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
.zhu .pan .wai span::before{
  content: '';
  display: block;
  width: 16px;
  height: 16px;
  border-radius: 100%;
  position: absolute;
  top: 6px;
  left:  calc(50% - 8px);
}
.zhu .pan .wai span:nth-child(2n)::before{
  width: 14px;
  height: 14px;
}
.zhu .pan .wai span:nth-child(4n)::before{
  background-color: #7c83f8;
}
.zhu .pan .wai span:nth-child(4n-1)::before{
  background-color: #7efffd;
}
.zhu .pan .wai span:nth-child(4n-2)::before{
  background-color: #fe7d00;
}
.zhu .pan .wai span:nth-child(4n-3)::before{
  background-color: #e3ff2f;
}


/* 抽奖选项 */
.xuanxiang{
  width: 80%;
  height: 80%;
  background-color: #fff;
  position: absolute;
  top: 10%;
  left: 10%;
  border-radius: 100%;
  overflow: hidden;
  transition: all 5s;
}
.xuanxiang::after{
  content: '';
  display: block;
  width: 50%;
  height: 50%;
  background-color: #fff;
  position: absolute;
  top: 25%;
  left: 25%;
  border-radius: 100%;
  overflow: hidden;
}
.xuanxiang span{
  width:100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
.xuanxiang span::before{
  content: '';
  display:block;
  width:0px;
   border:40px solid transparent;
   border-top-width: 160px;
   border-top-style: solid;
   position: absolute;
   left: calc(50% - 40px);
}
.xuanxiang span:nth-child(2n-1)::before{
border-top-color: #fcc;
}
.xuanxiang span:nth-child(2n)::before{
border-top-color: #ffc;
}
.xuanxiang span i{
  display:block;
  font-style: normal;
  font-weight: bold;
  color: #f35;
  position: absolute;
  left:calc(50% - 8px);
  top: 2%;
  width: 16px;
  font-size:16px;
}
/* 中心部位 */
.nei{
  width: 34%;
  height: 34%;
  position: absolute;
  top: 33%;
  left: 33%;
  border-radius: 100%;
  background-color: #ffbf81;
  cursor:pointer;
  z-index: 3;
}

.nei span{
  display:block;
  width: 100%;
  padding-top: 20px;
  color: #f35;
  font-size: 32px;
  text-align: center;
    transition: .3s;
}
.nei:hover span{
  color: #fff;
  transition: .3s;
}
/* 选项锚 */
.mao{
  width: 80%;
  height: 80%;
  position: absolute;
  top: 8%;
  left: 10%;
  text-align: center;
  z-index: 2;
}
.mao::before{
  content: '';
  display: inline-block;
  border: 10px solid transparent;
  border-top:18px solid #69f;

}
</style>
