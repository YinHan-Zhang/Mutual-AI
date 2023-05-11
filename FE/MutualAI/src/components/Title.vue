<script setup>
defineProps(['title'])
</script>
<template>
    <h2>{{ title }}</h2>
</template>
<style scoped>
h2{
    height: 60px;
    width: 600px;
    line-height: 60px;
    margin:0 auto 30px;
    color: black;
    text-align: center;
    font-size: 20px;
    border-bottom: #087dea 3px solid;
}
</style>