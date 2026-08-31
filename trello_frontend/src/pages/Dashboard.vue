<script setup>
    import DeconnexionBtn from '../components/DeconnexionBtn.vue';
    import Header from '../components/Header.vue';
    import OverviewCards from '../components/OverviewCards.vue';
    import ModalProject from '../components/ModalProject.vue';
    
    import { ref, onMounted, onUnmounted, computed } from 'vue';

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

    const handleProjectCreate = async (newProject) => {
        projects.value.push(newProject);
        projectsFiltered.value.push(newProject);
        closeModal();

        try{
            const response = await fetch('http://localhost:8000/api/projects/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(newProject),
            });

            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status}`);
            }

            const createdProject = await response.json();
            // remplacer le projet temporaire par celui créé par l'API
            // on recherche l'index du projet temporaire dans la liste des projets
            const index = projects.value.findIndex(p => p === newProject);
            // si on le trouve, on le remplace par le projet créé par l'API
            if (index !== -1) {
                projects.value[index] = createdProject;
            }

        } catch (error) {
            console.error('Erreur lors de la création du projet:', error);
            projects.value.pop(); // retirer le projet temporaire de la liste
            alert('Erreur lors de la création du projet. Veuillez réessayer.');
        }
    };

    const handleProjectUpdate = async (updatedProject) => {
        const index = projects.value.findIndex(p => p.project_id === updatedProject.project_id);
        if (index !== -1) {
            projects.value[index] = updatedProject;
        }
        closeModal();

        try{
            const response = await fetch(`http://localhost:8000/api/projects/${updatedProject.project_id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(updatedProject),
            });

            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status}`);
            }

            const updatedProjectFromAPI = await response.json();
            const index = projects.value.findIndex(p => p.project_id === updatedProjectFromAPI.project_id);
            if (index !== -1) {
                projects.value[index] = updatedProjectFromAPI;
            }
        } catch (error) {
            console.error('Erreur lors de la mise à jour du projet:', error);
            alert('Erreur lors de la mise à jour du projet. Veuillez réessayer.');
        }
    };

    

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

    // récupérer l'utilisateur courant depuis l'API
    const currentUser = ref(null);
    const fetchCurrentUser = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/user/me/', {
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
            currentUser.value = data;
        } catch (error) {
            console.error('Erreur lors du fetch de l\'utilisateur courant:', error);
        }
    };
    

    // fonction appelée à l'affichage du composant
    onMounted(() => {
        fetchProjects();
        fetchTasks();
        fetchCurrentUser();
    });

    // fonction appelée à la destruction du composant
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

    // récupérer les tâches d'un projet spécifique
    const getProjectTasks = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id);
        return found ? found.length : 0;
    };

    // récupérer les tâches terminées d'un projet spécifique
    const getProjectTasksDone = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column === 3);
        return found ? found.length : 0;
    };

    // récupérer les tâches à faire d'un projet spécifique
    const getProjectTasksToDo = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column === 1);
        return found ? found.length : 0;
    };

    // récupérer les tâches en retard d'un projet spécifique
    const getProjectTasksOverdue = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column !== 3 && new Date(t.task_dead_line) < Date.now());
        return found ? found.length : 0;
    };

    // récupérer le pourcentage de progression d'un projet spécifique
    const getProjectProgress = (project_id) => {
        const totalTasks = getProjectTasks(project_id);
        const completedTasks = getProjectTasksDone(project_id);
        return totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    };
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

    // filtrer les projets en fonction de la recherche
    const filterProjects = (event) => {
        const searchTerm = event.target.value.toLowerCase();
        projectsFiltered.value = projects.value.filter(project => project.project_name.toLowerCase().includes(searchTerm));
    };

    // data pour l'overview cards (il faudra les récupérer depuis l'api)
    // nombre de projets actifs
    // nombre de tâches en cours
    // nombre de tâches terminées
    // nombre de tâches en retard
    const date = new Date();
    const projectsActive = computed(() => (projects.value.length));

    const tasksInProgress = computed(() => {
        return projects.value.reduce((total, project) => total + (getProjectTasks(project.project_id) - getProjectTasksDone(project.project_id) - getProjectTasksToDo(project.project_id)), 0);
    });

    const tasksCompleted = computed(() => (
        projects.value.reduce((total, project) => total + getProjectTasksDone(project.project_id), 0)
    ));

    const tasksOverdue = computed(() => (
        projects.value.reduce((total, project) => total + getProjectTasksOverdue(project.project_id), 0)
    ));

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
                    <h1 id="greeting" class="text-3xl font-bold">Bonjour, {{ currentUser?.user_name }} &#128075;</h1>
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
                <OverviewCards label="Tâches terminées" :value="tasksCompleted"></OverviewCards>
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