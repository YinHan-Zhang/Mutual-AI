<script setup>
import NumberCanvas from "../components/NumberCanvas.vue";
import Tip from "../components/Tip.vue";
import Alert from "../components/Alert.vue";
import Button from "../components/Button.vue";
import Title from "../components/Title.vue";
import { onMounted,ref } from "vue";

let number = ref('')
let alerts = [
  '让子弹飞一会儿~',
]
let currentAlert = ref('')

let canvas = ref()
let img = ref()
function initCanvas() {
    let oCanvas = canvas.value
    let topDistance = canvas.value.getBoundingClientRect().top
    let leftDistance = canvas.value.getBoundingClientRect().left
    let ctx = oCanvas.getContext("2d");
    let gradient = ctx.createLinearGradient(0, 0, 500, 0);
    gradient.addColorStop("0", "white");
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 30
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    oCanvas.onmousedown = function (event) {
        ctx.beginPath();
        ctx.moveTo(event.clientX - leftDistance, event.clientY - topDistance);
        oCanvas.onmousemove = function (event) {
            ctx.lineTo(event.clientX - leftDistance, event.clientY - topDistance);
            ctx.stroke();
        }
    }
    oCanvas.onmouseup = function () {
        oCanvas.onmousemove = null;
    }
    //移动端触摸
    var flag = false;
    oCanvas.addEventListener("touchstart", function (evt) {
        var evt = evt || window.event;
        var x = evt.touches[0].pageX - leftDistance;
        var y = evt.touches[0].pageY - topDistance;
        ctx.beginPath();
        ctx.moveTo(x, y);
        flag = true;
    });
    oCanvas.addEventListener("touchmove", function (evt) {
        if (flag) {
            var evt = evt || window.event;
            var x = evt.touches[0].pageX - leftDistance;
            var y = evt.touches[0].pageY - topDistance;
            ctx.lineTo(x, y);
            ctx.stroke();
        }
      });
    oCanvas.addEventListener("touchend", function () {
        flag = false;
        ctx.closePath();
  });
}
onMounted(() => {
  initCanvas()
})
function clearCanvas() {
    var oCanvas = canvas.value
    var ctx = oCanvas.getContext("2d");
    ctx.fillStyle = '#393d49';
    ctx.fillRect(0, 0, 400, 400);
    img.value.src = ''
    currentAlert.value = ''
    number.value = ''
}
function recognition() {
    var oCanvas = canvas.value
    let strDataURI = oCanvas.toDataURL("image/png");
    currentAlert.value = alerts[0]
    axios({
        method: "POST",
        url: "http://ai.9998k.cn/api/written_digit_recognition",
        headers: { "Content-Type": "application/json" },
        data: {
          "img": strDataURI
        }
    })
      .then(function (response) {
          // console.log(response.data.res);
          currentAlert.value = "经识别，这个数字为"+response.data.res
      })
      .catch(function (error) {
          currentAlert.value = '出错了,请重新试试~'
          console.log(error);
      })
}
</script>
<template>
  <div class="number">
    <Title title="手写数字识别"></Title> 
    <canvas width="400" height="400" class="numberCanvas" ref="canvas"></canvas>
    <img src="" width="28" height="28" ref="img">
    <div class="buttonBox">
      <Button button-name="清空" type="button" color="grey" @click="clearCanvas()"></Button>
      <Button button-name="识别" type="button" color="green" @click="recognition()"></Button>
    </div>
    <Tip>PC端按下鼠标(左键，右键，中键均可)后移动鼠标、移动端直接触摸画板，即可在画板上绘出数字。</Tip>
    <div class="showBox" :class="{ generateAlert: currentAlert }">
         <Alert v-if="currentAlert" :word="currentAlert"></Alert>
    </div>
  </div>
</template>

<style scoped>
.number{
    padding-top: 0;
}
.numberCanvas {
    display: block;
    background: #393d49;
    margin: auto;
    border: grey 1px solid;
}
img{
    display: none;
}
.buttonBox {
    display: flex;
    width: 240px;
    margin: 30px auto 0;
    justify-content: space-between;
}
.showBox {
    margin:30px auto;
    height: 5px;
    line-height: 60px;
    color: white;
    text-align: center;
    transition: all .5s;
    opacity: 0;
}
.generateAlert {
    height: 60px;
    opacity: 1;
}
</style>