<script setup>
import { ref } from "vue";
import Title from "../components/Title.vue";
import Input from '../components/Input.vue';
import Button from "../components/Button.vue";
import Alert from "../components/Alert.vue"
import Tip from "../components/Tip.vue"
const text = ref("")
const alerts = ["让子弹飞一会儿~","文本未输入","请检查文本是否合规"];
const classes = ['finance', 'realty', 'stocks', 'education', 'science', 'society', 'politics', 'sports', 'game', 'entertainment']
const currentAlert = ref("")

const reg = /^[\u4e00-\u9fa5]{1,}$/g
function submit() {
    const result = ref(reg.test(text.value))
    // console.log(text.value);
    // console.log(result.value);
    if (result.value) {
        currentAlert.value = alerts[0];
        axios({
            method: "get",
            url: "http://ai.9998k.cn/api//Chinese_Text_Classification",
            headers: { "Content-Type": "application/json" },
            params: {
                text: text.value,
            }
        })
            .then(function (res) {
                console.log(res.data.res);
                currentAlert.value = ""
                currentAlert.value = "这段文本的类别属于"+classes[res.data.res]
                console.log(currentAlert);
            })
            .catch(function (error) {
                currentAlert.value = '出错了,请重新试试~'
                console.log(error);
            })
    }
    else if (text.value === "") {
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
</script>
<template>
    <div class="text-classification">
        <Title title="文本分类"></Title>  
        <Input v-model="text"
               label="中文文本"
               type="text"
               placeholder="请输入一段中文文本"
               class="input">
        </Input>
        <div class="button-box">
            <Button button-name="提交" color="green" @click="submit()"></Button>
        </div>
        <Tip>
            文本类别:
            <span v-for="item in classes" class="classSpan">{{ item }}</span>
        </Tip>
        <div class="showBox" :class="{ generateAlert: currentAlert }">
            <Alert v-if="currentAlert" :word="currentAlert"></Alert>
        </div>
    </div>
</template>
<style scoped>
.text-classification{
    display: flex;
    flex-direction: column;
    padding-top: 0;
}

.button-box{
    margin: 30px auto;
    width: 80px;
}

.classSpan{
    margin: 4px;
    display: inline-block;
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