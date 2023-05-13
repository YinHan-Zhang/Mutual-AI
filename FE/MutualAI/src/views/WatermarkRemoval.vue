<script setup>
import Button from "../components/Button.vue";
import Alert from "../components/Alert.vue"
import Title from "../components/Title.vue"

import { ref } from "vue";

const alerts = ["让子弹飞一会儿~","出错了,请重新试试~"];
const currentAlert = ref("")
const imgInput = ref()
const imgSrc = ref("")

function uploadImg(e){
    let reader = new FileReader();
    // 用户选择的文件列表： e.target.files[0]
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function () {
        imgSrc.value = reader.result;
        console.log(imgSrc.value);
    }
}
function submit() {
    currentAlert.value = alerts[0];
    axios({
        method: "POST",
        url: "http://ai.9998k.cn/api3/watermark_removal",
        headers: { "Content-Type": "application/json" },
        data: {
          "img": imgSrc.value
        }
    })
        .then(function (response) {
            currentAlert.value=""
            // console.log(response.data.res);
            imgSrc.value = response.data.res
        })
        .catch(function (error) {
            console.log(error);
            currentAlert.value = alerts[1]
        })
}
</script>
<template>
    <div class="watermarkRemoval">
        <Title title="水印去除"></Title>  
        <div class="img-box">
            <img :src=imgSrc alt="" height="400">
        </div>
        <div class="button-box">
            <div class="upload-box">
                <Button button-name="上传图片" color="blue"></Button>
                <input ref="imgInput" type="file" accept="image/*" @change="uploadImg($event)">
            </div>
            <Button button-name="去除水印" color="green" @click="submit()"></Button>
        </div>
        <div class="showBox" :class="{ generateAlert: currentAlert }">
            <Alert v-if="currentAlert" :word="currentAlert"></Alert>
        </div>
    </div>
</template>
<style scoped>
.watermarkRemoval{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 0;
}
.button-box{
    display: flex;
    width: 240px;
    margin: 30px auto ;
    justify-content: space-between;
}
.upload-box{
    position: relative;
    width: 80px;
    height: 40px;
}
.upload-box input{
    display: inline-block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
}
.img-box{
    display: flex;
    justify-content: center;
    width: 400px;
    height: 400px;
    background: #393d49;
}

.img-box img[src=''],img:not([src]) {
    opacity: 0;
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