<script setup>
    import { ref, onMounted, onUnmounted, watch } from 'vue';
    import Draggable  from 'vuedraggable';

    const props = defineProps({
        project_id: String,
        show_delete_button: Boolean,
        tasks: Array
    });

    const emit = defineEmits(['edit_task', 'delete_task', 'task_moved']);

    const tasksByColumn = ref({});

    // controller pour annuler les fetch si l'utilisateur quitte la page
    const controller = new AbortController();

    // fetch /api/columns
    const columns = ref([]);
    const fetchColumns = async () => {
        try{
            const response = await fetch('http://localhost:8000/api/columns/', { 
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: controller.signal });
            if(!response.ok){
                throw new Error('Erreur lors de la récupération des colonnes');
            }
            const data = await response.json();
            columns.value = data;
        } catch (error) {
            console.error(error);
        }
    };

    // fonction qui construit tasksByColumn à partir de columns.value + props.tasks
    const buildTasksByColumn = () => {
        const result = {};
        columns.value.forEach(column => {
            result[column.column_id] = props.tasks.filter(task => task.column === column.column_id);
        });
        tasksByColumn.value = result;
    };

    // Fonction pour obtenir la classe CSS en fonction de la couleur du tag
    const getClassForTag = (tag_color) => {
        return `bg-${tag_color}-500`;
    };

    onMounted(() => {
        fetchColumns();
        watch([columns, () => props.tasks], buildTasksByColumn, { immediate: true });
    });

    // Annulation des fetch si l'utilisateur quitte la page
    onUnmounted(() => {
        controller.abort();
    });

    // Fonction pour gérer le déplacement des tâches entre les colonnes
    const onDragEnd = (event) => {
        const taskId = Number(event.item.dataset.taskId);
        const newColumnId = Number(event.to.dataset.columnId);
        emit('task_moved', { taskId, newColumnId });
    };
</script>

<template>
    <div class="mx-10 flex flex-wrap gap-4">
            <div v-for="column in columns" 
            :key="column.column_id" 
            class="rounded-lg p-4 flex-1 min-w-[250px]"
            style="background-color: var(--column-bg);"
            >
                <h2 class="text-xl font-bold mb-4">{{ column.column_name }}</h2>
                <Draggable 
                :list="tasksByColumn[column.column_id] || []"
                :data-column-id="column.column_id"
                item-key="task_id"
                group="tasks"
                @end="onDragEnd">
                    <template #item="{ element: task }">
                        <div 
                        :data-task-id="task.task_id"
                        class="flex flex-col rounded-lg p-4 mb-4"
                        style="background-color: var(--input-bg);">
                            <h3 class="text-lg font-semibold mb-2">{{ task.task_name }}</h3>
                            <p class="mb-2">{{ task.task_description }}</p>
                            <div class="mt-auto flex flex-wrap gap-2">
                                <span v-for="taggedItem in task.taggeds" :key="taggedItem.tag.tag_id" :class="[getClassForTag(taggedItem.tag.tag_color), 'text-white px-2 py-1 rounded-full text-sm']">{{ taggedItem.tag.tag_name }}</span>
                            </div>
                            <div id="deadline" 
                            class="mt-auto text-gray-400 mt-2">
                                Date limite : {{ task.task_dead_line }}
                            </div>
                            <button id="update-task" 
                            @click="emit('edit_task', task)" 
                            class="mt-auto bg-purple-500 hover:bg-purple-700 text-white font-bold py-1 px-2 rounded">
                                Modifier
                            </button>
                            <button v-if="props.show_delete_button" 
                            @click="emit('delete_task', task)" 
                            class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">
                                Supprimer
                            </button>
                        </div>
                    </template>
                </Draggable>   
            </div>

        </div>
</template>