<script setup>
    defineProps({
        label: String,
        value: [String, Number],
    })
</script>

<template>
    <div :id="label" 
    class="border border-gray-500 rounded-md p-4 w-64 flex flex-col items-center justify-center gap-2" 
    style="background-color: var(--input-bg);">
        <p class="text-gray-500">{{ label }}</p>
        <span 
        :class="{
            'text-purple-500 text-4xl font-bold': label == 'Projet Actifs',
            'text-yellow-500 text-4xl font-bold': label == 'Tâches en cours',
            'text-green-500 text-4xl font-bold': label == 'Tâches terminées',
            'text-red-500 text-4xl font-bold': label == 'En retard'
        }">
            {{ value }}
        </span>
    </div>
</template>

<style></style>