<script setup>
defineProps(['modelValue','label','type','placeholder'])
defineEmits(['update:modelValue'])
</script>
<template>
    <div class="input">
        <label>{{ label }}</label>
        <input :type=type
               :placeholder="placeholder"
               :value="modelValue"
               @input="$emit('update:modelValue', $event.target.value)"/>
    </div>
</template>
<style scoped>
.input{
    display: flex;
    width: 600px;
    margin: auto;
    justify-content: space-between;
}
.input label {
    box-sizing: border-box;
    width: 100px;
    height: 40px;
    line-height: 40px;
    font-size: 20px;
    text-align: right;
}
input {
  border: solid 1px #ccc;
  height: 40px;
  width: 480px;
  outline: none;
  font-size: 16px;
  color: black;
  padding-left: 10px;
  border-radius: 5px;
}
</style>