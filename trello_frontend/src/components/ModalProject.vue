<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        mode: String,
        project: Object,
    });

    const emit = defineEmits(['create', 'update', 'cancel']);

    const formData = ref({
        project_name: props.project?.project_name || '',
        project_description: props.project?.project_description || '',
        project_creation_date: props.project?.project_creation_date || '',
    });

    const isEdit = computed(() => props.mode === 'edit');
    const modalTitle = computed(() => isEdit.value ? 'Modifier le projet' : 'Ajouter un projet');
    const buttonLabel = computed(() => isEdit.value ? 'Modifier' : 'Ajouter');

    const handleSubmit = () => {
        if (isEdit.value) {
            // Handle project update logic here
            emit("update", {project_id: props.project.project_id, ...formData.value});
            console.log('Updating project:', formData.value);
        } else {
            // Handle project creation logic here
            emit("create", formData.value);
            console.log('Creating new project:', formData.value);
        }
    };
</script>

<template>
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white rounded-lg p-6 w-96">
            <h2 class="text-xl font-bold mb-4">{{ modalTitle }}</h2>
            <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                    <label for="project_name" class="block text-gray-700">Nom du projet</label>
                    <input v-model="formData.project_name" type="text" id="project_name" 
                    class="w-full text-black border border-gray-300 rounded-md p-2" required />
                </div>
                <div class="mb-4">
                    <label for="project_description" class="block text-gray-700">Description</label>
                    <textarea v-model="formData.project_description" id="project_description" 
                    class="w-full text-black border border-gray-300 rounded-md p-2" required></textarea>
                </div>
                <div class="mb-4">
                    <label for="project_creation_date" class="block text-gray-700">Date de création</label>
                    <input v-model="formData.project_creation_date" type="date" id="project_creation_date" 
                    class="w-full text-black border border-gray-300 rounded-md p-2" required />
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