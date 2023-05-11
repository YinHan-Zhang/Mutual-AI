<script setup>
import BlogPost from "./components/BlogPost.vue";
import {onDeactivated,ref,reactive,resolveDirective,withDirectives,onUpdated,} from "vue";
import { useRouter, useRoute } from "vue-router";
import Triangle from "./components/Triangle.vue";

let currentPost = ref("");
const router = useRouter();
const route = useRoute();
setTimeout(() => {
    currentPost.value = route.name;
}, 1);

const introduction = {
    title: "简介",
    path: "/introduction",
    view: "Introduction",
};
const posts = [
    {
        title: "手写数字识别",
        path: "/number",
        view: "Number",
    },
    {
        title: "古诗词生成",
        path: "/poetry",
        view: "Poetry",
    },
    {
        title: "文本分类",
        path: "/chinese_text_classification",
        view: "TextClassification",
    },
    {
        title: "情感识别",
        path: "/emotion_sentiment",
        view: "EmotionSentiment",
    },
    {
        title: "水印去除",
        path: "/watermark_removal",
        view: "WatermarkRemoval",
    },
];
const isAsideShrink = ref(false)
function shrinkBtnClick() {
    isAsideShrink.value=!isAsideShrink.value
}
</script>

<template>
  <div class="app">
    <header>
        <h1>Mutual AI</h1>
    </header>
    <aside :class="{asideShrink:isAsideShrink}">
        <h3 class="menu-header">开始</h3>
        <Triangle triangle="triangle2" class="shrink-btn" :class="{rotate:!isAsideShrink}" @click="shrinkBtnClick()"></Triangle>
        <router-link :to="introduction.path"
                     @click="currentPost = introduction.view"
                     :class="['menu-button', { active: currentPost === introduction.view }]">
            {{ introduction.title }}
        </router-link>
        <h3 class="menu-header">演示</h3>
        <router-link v-for="(post, index) in posts"
                     :key="index"
                     :to="post.path"
                     @click="currentPost = post.view"
                     :class="['menu-button', { active: currentPost == post.view }]">
            {{ post.title }}
        </router-link>
        </aside>
        <main>
        <router-view></router-view>
        </main>
    </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  display: flex;
}

header {
  position: fixed;
  top: 0;
  height: 80px;
  width: 100%;
  border-bottom: 1px solid #ccc;
  background: #f6f6f7;
  z-index: 2000;
}

header h1 {
  font-size: 43px;
  font-weight: 500;
  line-height: 80px;
}

aside {
  position: fixed;
  top: 80px;
  display: flex;
  flex-direction: column;
  width: 200px;
  height: 100%;
  padding: 0 20px;
  z-index: 1000;
  border-right: 1px solid #ccc;
  background: #f6f6f7;
  transition: all .3s;
  /* overflow-y: scroll; */
}

.asideShrink {
  margin-left: -160px;
  background: transparent;
  border: none;
}

.shrink-btn {
  border: red;
}

main {
  display: flex;
  justify-content: center;
  height: 100%;
  /* flex: 0.5; */
  margin: 80px auto 0;
}

.menu-header {
  height: 40px;
  line-height: 40px;
  font-size: 20px;
  font-weight: 600;
  color: #333333;
}

aside .triangle {
  transform: translateZ(180deg);
}

.menu-button {
  text-decoration: none;
  width: 160px;
  height: 40px;
  line-height: 40px;
  cursor: pointer;
  color: #3c3c3cb3;
  font-size: 18px;
  transition: color 0.3s;
}

.menu-button:hover {
  color: black;
}

.menu-button.active {
  color: #087dea;
}

.tab {
  font-size: 50px;
}
</style>
