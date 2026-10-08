<script setup>
    import DeconnexionBtn from '../components/DeconnexionBtn.vue';
    import Header from '../components/Header.vue';
    import OverviewCards from '../components/OverviewCards.vue';
    import ModalProject from '../components/ModalProject.vue';
    import ProjectsArray from '../components/ProjectsArray.vue';
    import { useProjectTasks } from '@/composables/useProjectTasks.js';
    
    
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
            // recharger la vue pour afficher le projet créé
            window.location.reload();

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

    // récupérer les tâches d'un projet spécifique via le composable useProjectTasks
    const { getProjectTasks, getProjectTasksDone, getProjectTasksToDo, getProjectTasksOverdue } = useProjectTasks(tasks);

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

    // booléen pour afficher le bouton de suppression d'un projet
    const showDeleteButton = ref(false);

    // fonction pour supprimer un projet
    const deleteProject = async (project) => {
        try {
            const response = await fetch(`http://localhost:8000/api/projects/${project.project_id}/`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                signal: controller.signal
            });

            if (!response.ok) {
                throw new Error("Erreur lors de la suppression du projet");
            } else {
                alert("Projet supprimé avec succès");
            }
            // mettre à jour la liste des projets après la suppression en rechargeant la vue
            window.location.reload();
        } catch (error) {
            console.error("Erreur lors de la suppression du projet :", error);
        }
    }

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
                <div id="new-project-col" class="col-span-1 flex justify-end">
                    <button 
                    class="bg-purple-500 hover:bg-purple-700 text-white rounded-md p-2"
                    @click="openAddProjectModal"
                    >
                        + Nouveau projet
                    </button>
                    <button
                    class="ml-4 bg-red-500 hover:bg-red-700 text-white rounded-md p-2"
                    @click="showDeleteButton = !showDeleteButton">
                        - Supprimer projet
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
            <ProjectsArray
                :projectsFiltered="projectsFiltered"
                :showDeleteButton="showDeleteButton"
                :tasks="tasks"
                @deleteProject="deleteProject"
                @openEditProjectModal="openEditProjectModal"
            />
            
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