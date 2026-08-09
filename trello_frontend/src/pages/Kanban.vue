<script setup>
    import Header from '../components/Header.vue';
    import { ref } from 'vue';

    // fetch /api/columns
    const column_ = ref([
        { column_id: 1, column_name: "À faire" },
        { column_id: 2, column_name: "En cours" },
        { column_id: 3, column_name: "Terminée" }
    ]);

    const columnsNumber = column_.value.length;
    const classColumn = `grid grid-cols-${columnsNumber} gap-4`;

    // fetch /api/projects/id
    const project = ref({
        project_id: 1,
        project_name: "Projet 1",
        project_description: "Description du projet 1",
        project_creation_date: "01/01/2026"
    });
    
    // fetch /api/tasks/project_id 
    const tasks = ref([
        { task_id: 1, task_name: "Tâche 1", task_description: "Description de la tâche 1", column_id: 1},
        { task_id: 2, task_name: "Tâche 2", task_description: "Description de la tâche 2", column_id: 2},
        { task_id: 3, task_name: "Tâche 3", task_description: "Description de la tâche 3", column_id: 3},
        { task_id: 4, task_name: "Tâche 4", task_description: "Description de la tâche 4", column_id: 1},
        { task_id: 5, task_name: "Tâche 5", task_description: "Description de la tâche 5", column_id: 2},
    ]);

    // fetch /api/tagged/joinTag
    const tagged = ref([
        { task_id: 1, tag_id: 1, tag_name: "Urgent", tag_color: "red" },
        { task_id: 2, tag_id: 2, tag_name: "Peu urgent", tag_color: "yellow" },
        { task_id: 3, tag_id: 3, tag_name: "Moyennement urgent", tag_color: "orange" },
        { task_id: 4, tag_id: 4, tag_name: "Frontend", tag_color: "blue" },
        { task_id: 5, tag_id: 5, tag_name: "Backend", tag_color: "green" },
        { task_id: 1, tag_id: 6, tag_name: "Devops", tag_color: "purple" }, 
        { task_id: 1, tag_id: 4, tag_name: "Frontend", tag_color: "blue" },
        { task_id: 2, tag_id: 5, tag_name: "Backend", tag_color: "green" },
        { task_id: 3, tag_id: 4, tag_name: "Frontend", tag_color: "blue" },
        { task_id: 4, tag_id: 5, tag_name: "Backend", tag_color: "green" },
        { task_id: 5, tag_id: 6, tag_name: "Devops", tag_color: "purple" },
    ]);

    const getClassForTag = (tag_color) => {
        switch(tag_color) {
            case 'red':
                return 'bg-red-500';
            case 'yellow':
                return 'bg-yellow-500';
            case 'orange':
                return 'bg-orange-500';
            case 'blue':
                return 'bg-blue-500';
            case 'green':
                return 'bg-green-500';
            case 'purple':
                return 'bg-purple-500';
            default:
                return '';
        }
    };


</script>

<template>
    <main class="text-white min-h-screen">
        <div id="header-row" class="grid grid-cols-3">
            <div id="header-col" class="col-span-1">
                <Header />
            </div>
            <div id="logout-col" class="col-start-3 col-span-1 flex items-center justify-end px-20">
                <a href="#" class="text-white">[→ Déconnexion</a>
            </div>
        </div>
        <hr class="mb-10 border-gray-500" />

        <div :class="[classColumn, 'mx-20']">
            <div v-for="column in column_" 
            :key="column.column_id" 
            class="rounded-lg p-4"
            style="background-color: var(--column-bg);"
            >
                <h2 class="text-xl font-bold mb-4">{{ column.column_name }}</h2>
                <div v-for="task in tasks.filter(t => t.column_id === column.column_id)" 
                    :key="task.task_id" 
                    class="rounded-lg p-4 mb-4"
                     style="background-color: var(--input-bg);">
                    <h3 class="text-lg font-semibold mb-2">{{ task.task_name }}</h3>
                    <p class="mb-2">{{ task.task_description }}</p>
                    <div class="flex flex-wrap gap-2">
                        <span v-for="tag in tagged.filter(tag => tag.task_id === task.task_id)" :key="tag.tag_id" :class="[getClassForTag(tag.tag_color), 'text-white px-2 py-1 rounded-full text-sm']">{{ tag.tag_name }}</span>
                    </div>
                </div>
            </div>

        </div>


    </main>
</template>

<style>
    main{
        background-color: var(--main-bg);
    }       
</style>