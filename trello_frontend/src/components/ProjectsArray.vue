<script setup>
    import { ref, computed } from 'vue';
    import { useProjectTasks } from '@/composables/useProjectTasks.js';
    
    const props = defineProps({
        projectsFiltered: Array,
        showDeleteButton: Boolean,
        tasks: Array,
    });

    const taskRef = computed(() => props.tasks);
    const { getProjectTasks, getProjectTasksDone, getProjectTasksToDo, getProjectTasksOverdue } = useProjectTasks(taskRef);

    const emit = defineEmits(['deleteProject', 'openEditProjectModal']);

    // Couleurs pour les projets et la barre de progression
    const colors = ref([
        "text-purple-500",
        "text-yellow-500",
        "text-green-500",
        "text-red-500",
        "text-blue-500",
    ]);

    const progressColors = ref([
        "bg-purple-500",
        "bg-yellow-500",
        "bg-green-500",
        "bg-red-500",
        "bg-blue-500",
    ]); 

    // récupérer la couleur d'un projet spécifique
    const getProjectColor = (project_id) => {
        const projectColor = colors.value[project_id-1];
        const moduloIndex = project_id % colors.value.length;
        if(project_id > colors.value.length){
            if(moduloIndex === 0) {
                return colors.value[colors.value.length - 1];
            }
            return colors.value[moduloIndex - 1];
        }
        return projectColor;
    };

    // récupérer la couleur de progression d'un projet spécifique
    const getProjectProgressColor = (project_id) => {
        const projectProgressColor = progressColors.value[project_id-1];
        const moduloIndex = project_id % progressColors.value.length;
        if(project_id > progressColors.value.length){
            if(moduloIndex === 0) {
                return progressColors.value[progressColors.value.length - 1];
            }
            return progressColors.value[moduloIndex - 1];
        }
        return projectProgressColor;
    };

        // récupérer le pourcentage de progression d'un projet spécifique
    const getProjectProgress = (project_id) => {
        const totalTasks = getProjectTasks(project_id);
        const completedTasks = getProjectTasksDone(project_id);
        return totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    };
</script>

<template>
    <div id="mes_projets" class="mt-10">
        <p class="text-xl font-bold">Mes Projets</p>
        <div class="flex flex-wrap gap-4">
            <div id="project-card" 
            v-for="project in props.projectsFiltered" 
            :key="project.project_id" 
            class="flex flex-col border border-gray-500 rounded-md p-4 w-64"  
            style="background-color: var(--input-bg);">
                <a :href="`http://localhost:5173/kanban?project_id=${project.project_id}`" class="flex flex-col h-full">
                    <div 
                    :class="[`text-2xl font-bold mb-2 border rounded-md w-fit py-2 px-4`, getProjectColor(project.project_id)]"
                    >
                        {{ project.project_name[0] }}
                    </div>
                    <h2 class="text-lg font-bold">{{ project.project_name }}</h2>
                    <p>{{ project.project_description }}</p>
                    <!-- barre de progression -->
                    <div id="progress-bar" class="mt-auto">
                        <div class="w-full grid grid-cols-2">
                            <span>
                                {{ getProjectTasksDone(project.project_id) }} / {{ getProjectTasks(project.project_id) }}
                            </span>
                            <span class="col-span-1 text-gray-500 text-right">
                                {{ getProjectProgress(project.project_id).toFixed(2) }}%
                            </span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-4 dark:bg-gray-700">
                            <div :class="[`h-4 rounded-full`, getProjectProgressColor(project.project_id)]" :style="`width: ${getProjectProgress(project.project_id)}%`">
                            </div>
                        </div>
                        <p class="text-gray-500">{{ project.project_creation_date }}</p>
                    </div>
                </a>
                <button 
                id="update-task" 
                class="mt-auto bg-purple-500 hover:bg-purple-700 text-white font-bold py-1 px-2 rounded"
                @click="emit('openEditProjectModal', project)"
                >
                    Modifier
                </button>
                <button 
                v-if="showDeleteButton"
                id="delete-task" 
                class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded"
                @click="emit('deleteProject', project)"
                >
                    Supprimer
                </button>
            </div>
        </div>
    </div>
</template>