<script setup>
</script>

<template>
    <div class="tip">
        <h3>提示</h3>
        <slot></slot>
    </div>
</template>

<style scoped>
    .tip{
        flex:0.8;
        margin: 30px auto;
        padding: 15px;
        border: solid 1px #087dea;
        border-radius: 20px;
        background: #f6f6f7;
    }

    .tip h3{
        padding-bottom: 15px;
        color: #393d49;
        letter-spacing: 2px;
    }
</style>