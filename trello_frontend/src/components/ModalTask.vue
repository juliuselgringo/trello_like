<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        mode: String,
        project: Object,
        task: Object,
    });

    const emit = defineEmits(['create', 'update', 'cancel']);

    const formData = ref({
        task_name: props.task?.task_name || '',
        task_description: props.task?.task_description || '',
        task_dead_line: props.task?.task_dead_line || '',
        column_id: props.task?.column_id || '1',
        project_id: props.task?.project_id || props.project?.project_id,
    });

    const isEdit = computed(() => props.mode === 'edit');
    const modalTitle = computed(() => isEdit.value ? 'Modifier la tâche' : 'Ajouter une tâche');
    const buttonLabel = computed(() => isEdit.value ? 'Modifier' : 'Ajouter');

    const handleSubmit = () => {
        if (isEdit.value) {
            // Handle task update logic here
            emit("update", {task_id: props.task.task_id, ...formData.value});
            console.log('Updating task:', formData.value);
        } else {
            // Handle task creation logic here
            emit("create", formData.value);
            console.log('Creating new task:', formData.value);
        }
    };
</script>

<template>
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white rounded-lg p-6 w-96">
            <h2 class="text-xl font-bold mb-4">{{ modalTitle }}</h2>
            <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                    <label for="task_name" class="block text-gray-700">Nom de la tâche</label>
                    <input v-model="formData.task_name" type="text" id="task_name" class="w-full border border-gray-300 rounded-md p-2" required />
                </div>
                <div class="mb-4">
                    <label for="task_description" class="block text-gray-700">Description</label>
                    <textarea v-model="formData.task_description" id="task_description" class="w-full border border-gray-300 rounded-md p-2" required></textarea>
                </div>
                <div class="mb-4">
                    <label for="task_dead_line" class="block text-gray-700">Date limite</label>
                    <input v-model="formData.task_dead_line" type="date" id="task_dead_line" class="w-full border border-gray-300 rounded-md p-2" required />
                </div>
                <button 
                type="submit" 
                class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
                >
                    {{ buttonLabel }}
                </button>
                <button id="cancel-button" @click="$emit('cancel')" type="button" class="ml-2 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                    Annuler
                </button>
            </form>
        </div>
    </div>
</template>