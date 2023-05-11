<template>
    <canvas width="400" height="400" class="numberCanvas"></canvas>
    <div class="imgBox">
        <img src="" width="28" height="28">
    </div>
    <div class="buttonBox">
        <button @click="$emit('clearCanvas')">清空</button>
        <button @click="$emit('recognition')">生成</button>
    </div>
</template>

<script>
export default {
    emits: ['clearCanvas','recognition']
}
</script>

<style scoped>
    .numberCanvas {
        display: block;
        background: black;
        margin: 20px auto 0;
    }

    .imgBox {
        width: 28px;
        height: 28px;
        border: 1px solid black;
        margin: 5px auto;
        background-color: black;
    }

    img[src=''],img:not([src]) {
        opacity: 0;
    }

    /* img{
        display: none;
    } */

    .buttonBox {
        display: flex;
        width: 180px;
        margin: 10px auto;
        justify-content: space-between;
    }

    button{
        font-size: 18px;
        border: solid 1px black;
        border-radius: 5px;
        padding: 5px 10px;
    }

</style>