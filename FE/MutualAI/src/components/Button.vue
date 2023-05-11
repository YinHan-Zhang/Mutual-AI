<script setup>
defineProps({
    buttonName:{
        type: String,
        default:''
    },
    color:{
        type: String,
        default:'green'
    },
    type:{
        type: String,
        default:'button'
    }
})
</script>
<template>
    <button :class="color" :type="type">{{ buttonName }}</button>
</template>
<style scoped>
button{
    width: 80px;
    height: 40px;
    border: solid 1px #ccc;
    border-radius: 5px;
    color: white;
    transition: all 0.3s;
    font-size: 14px;
}    
button:hover {
  border: solid 1px black;
  border-radius: 5px;
}
.green{
    background: #10b981;
}
.grey{
    background: grey;
}
.blue{
    background: #087dea;
}
</style>