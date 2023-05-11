<script setup>
defineProps({
    triangle:{
        type: String,
        default:'triangle1'
    }
})
</script>
<template>
    <div :class="triangle"></div>
</template>
<style scoped>
    .triangle1{
        display: inline-block;
        position: absolute;
        right: 10px;
        top: 15px;
        width: 0;
        height: 0;
        border-top: solid 8px #ccc;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        transition: all .3s;
    }
    .triangle2{
        flex: 2;
        display: inline-block;
        position: absolute;
        right: 10px;
        top: 15px;
        width: 0;
        height: 0;
        border-left: solid 8px #ccc;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        transition: all .3s;
    }
    .rotate{
        transform: rotateZ(180deg);
    }
</style>