<script setup>
    import Header from '../components/Header.vue';
    import DeconnexionBtn from '@/components/DeconnexionBtn.vue';
    import { ref, onMounted, onUnmounted, computed } from 'vue';
    import { useRoute } from 'vue-router';
    import ModalTask from '@/components/ModalTask.vue';
    import KanbanArray from '@/components/KanbanArray.vue';

    //récupération de l'id du projet depuis l'URL
    const route = useRoute();
    const projectId = ref(route.query.project_id);


    
    // controller pour annuler les fetch si l'utilisateur quitte la page
    const controller = new AbortController();

    // booleen pour afficher le bouton de suppression des tâches
    const showDeleteButton = ref(false);

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
    });

    // Annulation des fetch si l'utilisateur quitte la page
    onUnmounted(() => {
        controller.abort();
    });

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

    const handleTaskCreate = async (newTask) => {
        tasks.value.push(newTask);
        closeModal();

        try {
            const response = await fetch('http://localhost:8000/api/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(newTask),
                signal: controller.signal
            });
            if (!response.ok) {
                throw new Error('Erreur lors de la création de la tâche' + response.status);
            }
            const createdTask = await response.json();
            // remplacer la tâche temporaire par la tâche créée depuis l'API
            const index = tasks.value.findIndex(t => t === newTask);
            if (index !== -1) {
                tasks.value[index] = createdTask;
            }
            // recharger la vue pour afficher la tâche créée
            window.location.reload();

        } catch (error) {
            console.error("Erreur lors de la création de la tâche :", error);
            tasks.value.pop();
        }
    };

    const handleTaskUpdate = async (updatedTask) => {
        const index = tasks.value.findIndex(t => t.task_id === updatedTask.task_id);
        if (index !== -1) {
            tasks.value[index] = updatedTask;
        }
        closeModal();
        try {
            const response = await fetch(`http://localhost:8000/api/tasks/${updatedTask.task_id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(updatedTask),
                signal: controller.signal
            });
            if (!response.ok) {
                throw new Error('Erreur lors de la mise à jour de la tâche' + response.status);
            }
            const updatedTaskFromApi = await response.json();
            // mettre à jour la tâche avec les données renvoyées par l'API
            const index = tasks.value.findIndex(t => t.task_id === updatedTaskFromApi.task_id);
            if (index !== -1) {
                tasks.value[index] = updatedTaskFromApi;
            }
        } catch (error) {
            console.error("Erreur lors de la mise à jour de la tâche :", error);
        }
    };

    // fonction pour supprimer une tâche
    const deleteTask = async (task) => {
        try {
            const response = await fetch(`http://localhost:8000/api/tasks/${task.task_id}/`, {
                method: 'DELETE',
                credentials: 'include',
                signal: controller.signal
            });
            if (!response.ok) {
                throw new Error('Erreur lors de la suppression de la tâche' + response.status);
            } else {
                alert("Tâche supprimée avec succès");
            }
            const index = tasks.value.findIndex(t => t.task_id === task.task_id);
            if (index !== -1) {
                tasks.value.splice(index, 1);
            }
        } catch (error) {
            console.error("Erreur lors de la suppression de la tâche :", error);
        }
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
                <button id="add-task" @click="openAddTaskModal" class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
                    + Ajouter une tâche
                </button>
                <button 
                id="delete-task" 
                @click="showDeleteButton = !showDeleteButton" 
                class="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                    - Supprimer une tâche
                </button>
            </div>
        </div>
        <KanbanArray 
        :project_id="projectId"
        :show_delete_button="showDeleteButton"
        :tasks="tasks"
        @edit_task="openEditTaskModal"
        @delete_task="deleteTask"
         />


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