<script setup>
    import Header from '../components/Header.vue';
    import DeconnexionBtn from '@/components/DeconnexionBtn.vue';
    import { ref, onMounted, onUnmounted, computed } from 'vue';
    import { useRoute } from 'vue-router';
    import ModalTask from '@/components/ModalTask.vue';

    //récupération de l'id du projet depuis l'URL
    const route = useRoute();
    const projectId = ref(route.query.project_id);
    
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

    // fetch /api/projects/id
    const project = ref({})
    const fetchProject = async () => {
        try{
            const response = await fetch('http://localhost:8000/api/projects/' + projectId.value + '/', { 
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: controller.signal });
            if(!response.ok){
                throw new Error('Erreur lors de la récupération du projet');
            }
            const data = await response.json();
            project.value = data;
        } catch (error) {
            console.error(error);
        }
    };
    
    // fetch /api/tasks/project_id 
    const tasks = ref([]);
    const fetchTasksByProjectId = async () => {
        try{
            const response = await fetch(`http://localhost:8000/api/tasks/?project_id=${projectId.value}`, { 
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: controller.signal });
            if(!response.ok){
                throw new Error('Erreur lors de la récupération des tâches');
            }
            const data = await response.json();
            tasks.value = data;
        } catch (error) {
            console.error(error);
        }
    };

    // Appel des fonctions fetch lors du montage du composant
    onMounted(() => {
        fetchProject();
        fetchTasksByProjectId();
        fetchColumns();
    });

    // Annulation des fetch si l'utilisateur quitte la page
    onUnmounted(() => {
        controller.abort();
    });

    // Fonction pour obtenir la classe CSS en fonction de la couleur du tag
    const getClassForTag = (tag_color) => {
        return `bg-${tag_color}-500`;
    };

</script>

<template>
    <main class="text-white min-h-screen">
        <div id="header-row" class="flex flex-wrap gap-4 items-center justify-between mb-4">
            <div id="header-col">
                <Header />
            </div>
            <div class="ml-20">
                <a href="http://localhost:5173/Dashboard" class="text-white">&lt; Dashboard</a>
            </div>
            <div>
                <DeconnexionBtn />
            </div>
        </div>
        <hr class="mb-10 border-gray-500" />

        <div id="project-info" class="mx-20 mb-10 flex flex-wrap gap-4">
            <div id="project-details" class="col-span-1 min-w-[50%]">
                <div id="today" class="text-gray-400 mb-2">Aujourd'hui : {{ new Date().toLocaleDateString() }}</div>
                <h1 class="text-3xl font-bold mb-4">{{ project.project_name }}</h1>
                <p class="mb-2">{{ project.project_description }}</p>
                <p class="mb-2">Date de création : {{ project.project_creation_date }}</p>
            </div>
            <div id="project-actions" class="col-span-1 flex items-center justify-end min-w-[45%]">
                <button id="add-task" @click="openAddTaskModal" class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">+ Ajouter une tâche</button>
            </div>
        </div>
        <div class="mx-10 flex flex-wrap gap-4">
            <div v-for="column in columns" 
            :key="column.column_id" 
            class="rounded-lg p-4 flex-1 min-w-[250px]"
            style="background-color: var(--column-bg);"
            >
                <h2 class="text-xl font-bold mb-4">{{ column.column_name }}</h2>
                <div v-for="task in tasks.filter(t => t.column === column.column_id)" 
                    :key="task.task_id" 
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
                    @click="openEditTaskModal(task)" 
                    class="mt-auto bg-purple-500 hover:bg-purple-700 text-white font-bold py-1 px-2 rounded">Modifier</button>
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