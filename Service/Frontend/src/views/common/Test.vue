<script lang="ts" setup>
import { ref, reactive } from 'vue'

const hasClicked = ref(false)
const itemsInfo = reactive([
  { text: '頭獎', rotate: 0 },
  { text: '可惜了', rotate: 30 },
  { text: '三獎', rotate: 60 },
  { text: '可惜了', rotate: 90 },
  { text: '五獎', rotate: 120 },
  { text: '可惜了', rotate: 150 },
  { text: '三獎', rotate: 180 },
  { text: '可惜了', rotate: 210 },
  { text: '五獎', rotate: 240 },
  { text: '可惜了', rotate: 270 },
  { text: '二獎', rotate: 300 },
  { text: '五獎', rotate: 330 },
])

const playGame = (): void => {
  if (hasClicked.value) return

  let rotate = 0
  let yu = rotate % 60
  let num = Math.floor(Math.random() * 1800 + 360)
  let targetElem = document.querySelector('.xuanxiang')

  rotate = rotate + num

  if (yu > 10 && yu < 30) rotate -= 20;
  if (yu > 30 && yu < 50) rotate += 20;

  targetElem?.setAttribute('style', `transform: rotate(${rotate}deg)`)

  hasClicked.value = true
}
</script>

<template>
  <div id="test-page-body">
    <h2>Test Page</h2>
    <div class="zhu">
      <div class="pan">
        <div class="wai"></div>
        <div class="mao">
        </div>
        <div class="xuanxiang">
          <span
            v-for="item in itemsInfo"
            :key="item.text"
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
</template>

<style lang="scss" scoped>
#test-page-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 56px);
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
