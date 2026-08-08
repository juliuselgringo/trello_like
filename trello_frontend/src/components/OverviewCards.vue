<script setup>
    defineProps({
        label: String,
    })
</script>

<template>
    <div :id="label" class="h-28 mx-2 border border-gray-500 rounded-md text-gray-500 p-4" style="background-color: var(--input-bg);">
        <label for="">{{ label }}</label>
    </div>
</template>

<style></style>