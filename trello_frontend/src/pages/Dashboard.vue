<script setup>
    import DeconnexionBtn from '../components/DeconnexionBtn.vue';
    import Header from '../components/Header.vue';
    import OverviewCards from '../components/OverviewCards.vue';
    import ModalProject from '../components/ModalProject.vue';
    
    import { ref, onMounted, onUnmounted } from 'vue';

    // modal project
    const showModalProject = ref(false);
    const modalMode = ref('add');
    const selectedProject = ref(null);

    const openAddProjectModal = () => {
        modalMode.value = 'add';
        selectedProject.value = null;
        showModalProject.value = true;
    };

    const openEditProjectModal = (project) => {
        modalMode.value = 'edit';
        selectedProject.value = project;
        showModalProject.value = true;
    };

    const closeModal = () => {
        showModalProject.value = false;
    };

    const handleProjectCreate = (newProject) => {
    projects.value.push(newProject);
    closeModal();
    };

    const handleProjectUpdate = (updatedProject) => {
    const index = projects.value.findIndex(p => p.project_id === updatedProject.project_id);
    if (index !== -1) {
        projects.value[index] = updatedProject;
    }
    closeModal();
    };

    // data pour l'overview cards (il faudra les récupérer depuis l'api)
    const date = new Date();
    const projectsActive = ref(5);
    const tasksInProgress = ref(3);
    const tasksCompletedThisMonth = ref(18);
    const tasksOverdue = ref(2);

    // Récupérer les projets depuis l'API
    const projects = ref([]);
    const projectsFiltered = ref([]);
    const controller = new AbortController();

    const fetchProjects = async () => {

        try {
            const response = await fetch('http://localhost:8000/api/projects/', { 
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: controller.signal });

            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status}`);
            }
            const data = await response.json();
            projects.value = data;
            projectsFiltered.value = [...data];
        } catch (error) {
            console.error('Erreur lors du fetch des projets:', error);
        }
    };

    // récupérer les tâches depuis l'API fetch /api/tasks/
    const tasks = ref([]);
    const fetchTasks = async () => {
        
        try{
            const response = await fetch('http://localhost:8000/api/tasks/', { 
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: controller.signal });
            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status}`);
            }
            const data = await response.json();
            tasks.value = data;
        } catch (error) {
            console.error('Erreur lors du fetch des tâches:', error);   
        }
    };
    

    onMounted(() => {
        fetchProjects();
        fetchTasks();
    });

    onUnmounted(() => {
        controller.abort(); // Annule le fetch si on quitte
    });

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


    

    const getProjectTasks = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id);
        return found ? found.length : 0;
    };

    const getProjectTasksDone = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column === 3);
        return found ? found.length : 0;
    };

    const getProjectProgress = (project_id) => {
        const totalTasks = getProjectTasks(project_id);
        const completedTasks = getProjectTasksDone(project_id);
        return totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    };
    
    const getProjectColor = (project_id) => {
        const projectColor = colors.value[project_id > colors.value.length ? (project_id - colors.value.length - 1) : (project_id - 1)];
        return projectColor;
    };

    const getProjectProgressColor = (project_id) => {
        const projectProgressColor = progressColors.value[project_id > progressColors.value.length ? (project_id - progressColors.value.length - 1) : (project_id - 1)];
        return projectProgressColor;
    };

    const filterProjects = (event) => {
        const searchTerm = event.target.value.toLowerCase();
        projectsFiltered.value = projects.value.filter(project => project.project_name.toLowerCase().includes(searchTerm));
    };

</script>

<template>
    <main class="text-white min-h-screen">
        <!-- Nav bar -->
        <div id="header-row" class="flex flex-wrap gap-4 items-center justify-between">
            <div id="header-col">
                <Header />
            </div>
            <div id="search-col" class="ml-10">
                <input class="w-full rounded-md px-4 py-2 text-gray-400 border border-gray-500" 
                style="background-color: var(--input-bg);" 
                type="text" placeholder="&#128269; Rechercher..."  
                @input="filterProjects"
                />
            </div>
            <DeconnexionBtn />
        </div>    
        <hr class="mb-10 border-gray-500" />
        <div id="layout-dashboard" class="mx-10">
            <!-- greetings + Nouveau projet -->
            <div id="first-row" class="flex flex-wrap gap-4 items-center justify-between">
                <div id="greeting-col" class="col-span-1">
                    <!-- date en français (samedi 8 aout 2026)-->
                    <p id="date">
                        {{ date.toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
                    </p>
                    <h1 id="greeting" class="text-3xl font-bold">Bonjour, Julien &#128075;</h1>
                    <p id="welcome-message">
                        Vous avez 
                        <span class="text-purple-500">{{ tasksInProgress }} tâches en cours</span>
                         aujourd'hui.
                    </p>
                </div>
                <div class="col-span-1 flex justify-end">
                    <button 
                    class="bg-purple-500 hover:bg-purple-700 text-white rounded-md p-2"
                    @click="openAddProjectModal"
                    >
                        + Nouveau projet
                    </button>
                </div>
            </div>
            <!-- OVERVIEW -->
            <div id="overview" class="flex flex-wrap gap-4 mt-10">
                <OverviewCards label="Projet Actifs" :value="projectsActive"></OverviewCards>
                <OverviewCards label="Tâches en cours" :value="tasksInProgress"></OverviewCards>
                <OverviewCards label="Terminées ce mois" :value="tasksCompletedThisMonth"></OverviewCards>
                <OverviewCards label="En retard" :value="tasksOverdue"></OverviewCards>
            </div>
            <!-- MES PROJETS -->
            <div id="mes_projets" class="mt-10">
                <p class="text-xl font-bold">Mes Projets</p>
                <div class="flex flex-wrap gap-4">
                    <div id="project-card" 
                    v-for="project in projectsFiltered" 
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
                        @click="openEditProjectModal(project)"
                        >
                            Modifier
                        </button>
                    </div>
                </div>
                
            </div>
        </div>
        <ModalProject 
        v-if="showModalProject" 
        :mode="modalMode" 
        :project="selectedProject" 
        @create="handleProjectCreate" 
        @update="handleProjectUpdate" 
        @cancel="closeModal" 
        />
    </main>

</template>

<style>
    main{
        background-color: var(--main-bg);
    }
</style>