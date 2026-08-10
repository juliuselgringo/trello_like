<script setup>
    import Header from '../components/Header.vue';
    import DeconnexionBtn from '@/components/DeconnexionBtn.vue';
    import { ref } from 'vue';
    import ModalTask from '@/components/ModalTask.vue';

    // modal task
    const showModalTask = ref(false);
    const modalMode = ref('add');
    const selectedTask = ref(null);

    const openAddTaskModal = () => {
        modalMode.value = 'add';
        selectedTask.value = null;
        showModalTask.value = true;
    };

    const openEditTaskModal = (task) => {
        modalMode.value = 'edit';
        selectedTask.value = task;
        showModalTask.value = true;
    };

    const closeModal = () => {
        showModalTask.value = false;
    };

    const handleTaskCreate = (newTask) => {
    tasks.value.push(newTask);
    closeModal();
    };

    const handleTaskUpdate = (updatedTask) => {
    const index = tasks.value.findIndex(t => t.task_id === updatedTask.task_id);
    if (index !== -1) {
        tasks.value[index] = updatedTask;
    }
    closeModal();
    };

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
        { task_id: 1, task_name: "Tâche 1", task_description: "Description de la tâche 1", task_dead_line: "01/01/2027", column_id: 1},
        { task_id: 2, task_name: "Tâche 2", task_description: "Description de la tâche 2", task_dead_line: "02/01/2027", column_id: 2},
        { task_id: 3, task_name: "Tâche 3", task_description: "Description de la tâche 3", task_dead_line: "03/01/2027", column_id: 3},
        { task_id: 4, task_name: "Tâche 4", task_description: "Description de la tâche 4", task_dead_line: "04/01/2027", column_id: 1},
        { task_id: 5, task_name: "Tâche 5", task_description: "Description de la tâche 5", task_dead_line: "05/01/2027", column_id: 2},
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
        return `bg-${tag_color}-500`;
    };


</script>

<template>
    <main class="text-white min-h-screen">
        <div id="header-row" class="grid grid-cols-3">
            <div id="header-col" class="col-span-1">
                <Header />
            </div>
            <div class="col-start-2 col-span-1 flex items-center justify-center">
                <a href="http://localhost:5173/Dashboard" class="text-white">&lt; Dashboard</a>
            </div>
            <DeconnexionBtn />
        </div>
        <hr class="mb-10 border-gray-500" />

        <div id="project-info" class="mx-20 mb-10 grid grid-cols-2 gap-4">
            <div id="project-details" class="col-span-1">
                <div id="today" class="text-gray-400 mb-2">Aujourd'hui : {{ new Date().toLocaleDateString() }}</div>
                <h1 class="text-3xl font-bold mb-4">{{ project.project_name }}</h1>
                <p class="mb-2">{{ project.project_description }}</p>
                <p class="mb-2">Date de création : {{ project.project_creation_date }}</p>
            </div>
            <div id="project-actions" class="col-span-1 flex items-center justify-end">
                <button id="add-task" @click="openAddTaskModal" class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">+ Ajouter une tâche</button>
            </div>
        </div>
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
                    <div id="deadline" class="text-gray-400 mt-2">Date limite : {{ task.task_dead_line }}</div>
                    <button id="update-task" @click="openEditTaskModal(task)" class="mt-2 bg-purple-500 hover:bg-purple-700 text-white font-bold py-1 px-2 rounded">Modifier</button>
                </div>
            </div>

        </div>


        <ModalTask 
            v-if="showModalTask" 
            :mode="modalMode" 
            :task="selectedTask" 
            :project="project" 
            @create="handleTaskCreate" 
            @update="handleTaskUpdate" 
            @cancel="showModalTask = false"
        />
    </main>
</template>

<style>
    main{
        background-color: var(--main-bg);
    }       
</style>