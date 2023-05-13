<script setup>
defineProps({
    word: {
        type: String,
        default: ""
    }
})
</script>
<template>
    <div class="alert">
        <span class="word">
            {{ word }}
            <slot></slot>
        </span>
    </div>
</template>
<style scoped>
    .alert{
        height: 60px;
        text-align: center;
    }

    .word{
        padding: 20px;
        background: #393d49;
        color: white;
    }
</style>