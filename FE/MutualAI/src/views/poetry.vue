<script setup>
import { ref } from "vue";
import Alert from "../components/Alert.vue";
import Triangle from "../components/Triangle.vue";
import Title from "../components/Title.vue";
import Button from "../components/Button.vue";

let options = [
  {
    string: "自动生成",
    value: 1,
  },
  {
    string: "根据首句生成",
    value: 2,
  },
  {
    string: "藏头诗",
    value: 3,
  },
];
let activeValue = ref(options[0].value);
let optionActive = ref(options[0].string);

let alerts = ["让子弹飞一会儿~","关键词未输入","请检查关键词是否合规"];
let currentAlert = ref("");

let isOptionShow = ref(false);
let rise = ref("");
function optionShow() {
  isOptionShow.value = !isOptionShow.value;
  setTimeout(() => {
    if (rise.value === "") {
      rise.value = "rise";
    } else {
      rise.value = "";
    }
  }, 1);
}

let addition = ref("");
function isOption(option) {
  activeValue.value = option.value;
  optionActive.value = option.string;
  addition.value = "";
}

function reset() {
  activeValue.value = 1;
  optionActive.value = options[activeValue.value - 1].string;
  addition.value = "";
}

const reg = /^[\u4e00-\u9fa5]{5,}$/g
function generate() {
    let result = ref(reg.test(addition.value))
    // console.log(addition.value);
    // console.log(result.value);
    if (activeValue.value === 1 || (activeValue.value !== 1 && result.value && addition.value )) {
        currentAlert.value=""
        currentAlert.value = alerts[0];
        axios({
            method: "get",
            url: "http://ai.9998k.cn/api/poetry-generator",
            params: {
                type_choice: activeValue.value,
                addition: addition.value,
            },
        })
            .then(function (response) {
                currentAlert.value = "";
                currentAlert.value = response.data.res;
            })
            .catch(function (error) {
                currentAlert.value = '出错了,请重新试试~'
                console.log(error);
            })
    }
    else if (addition.value === "") {
        currentAlert.value = alerts[1];
        setTimeout(() => {
        currentAlert.value = "";
        }, 1000);
    }
    else {
        currentAlert.value = alerts[2];
        setTimeout(() => {
        currentAlert.value = "";
        }, 1000);
    }
}
function random() {
    activeValue.value = 2;
    optionActive.value = options[activeValue.value - 1].string;
    addition.value = "窗前明月光";
}
</script>
<template>
  <div class="poetry">
    <div class="poetry-box">
      <Title title="古诗词生成"></Title>
      <form>
        <div class="type-box">
          <label>生成类型</label>
          <div class="select" @click="optionShow()">
            <div class="option-active">
              {{ optionActive }}
              <Triangle :class="{rotate:isOptionShow}" triangle="triangle1"></Triangle>
            </div>
            <ul v-show="isOptionShow" :class="rise">
              <li v-for="option in options"
                  @click="isOption(option)"
                  :class="{ active: activeValue === option.value }">
                  {{ option.string }}
              </li>
            </ul>
          </div>
        </div>
        <div class="keywords-box" v-if="activeValue != 1">
          <label>关键词</label>
          <input
            type="text"
            name="addition"
            placeholder="请输入生成诗词的关键词（最少输入五个汉字）"
            v-model="addition"/>
        </div>
        <div class="button-box">
            <Button button-name="重置" type="reset" color="grey" @click="reset()" class="reset"></Button>
            <Button button-name="生成" type="button" color="green" @click="generate()" class="generate"></Button>
            <Button button-name="赋值" type="button" color="blue" @click="random()" class="random"></Button>
        </div>
      </form>
    </div>
    <div class="showBox" :class="{ generateAlert: currentAlert }">
         <Alert v-if="currentAlert" :word="currentAlert"></Alert>
    </div>
  </div>
</template>

<style scoped>
.poetry-box {
  margin: auto;
  padding-top: 0;
}

.poetry-box form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.type-box,
.keywords-box {
  margin-bottom: 40px;
  width: 600px;
}

.poetry-box label {
  width: 100px;
  height: 40px;
  line-height: 40px;
  font-size: 20px;
  text-align: right;
}

.keywords-box {
  display: flex;
}
.keywords-box input {
  border: solid 1px #ccc;
  height: 40px;
  width: 480px;
  outline: none;
  font-size: 16px;
  color: black;
  padding-left: 10px;
  border-radius: 5px;
}

.type-box {
  z-index: 10;
  position: relative;
}
.type-box .select {
  height: 40px;
  width: 480px;
}
.type-box .select .option-active {
  height: 40px;
  line-height: 40px;
  border: solid 1px #ccc;
  background: white;
  padding-left: 10px;
  border-radius: 5px;
}

.type-box .select ul {
  margin-top: 20px;
  background: white;
  border: solid 1px #ccc;
  opacity: 0.5;
  transition: all 0.3s;
}
.type-box .select ul.rise {
  margin-top: 5px;
  opacity: 1;
}

.type-box .select li {
  list-style: none;
  height: 40px;
  line-height: 40px;
  padding-left: 10px;
  transition: all .3s;
}
.type-box .select li:hover {
  background: rgba(0, 0, 0, 0.1);
}
.type-box .select .active {
  background: #087dea;
}

.type-box,
.keywords-box {
  height: 40px;
  display: flex;
  justify-content: space-between;
}

.button-box {
  display: flex;
  justify-content: space-evenly;
  margin-top: 20px;
  width: 600px;
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