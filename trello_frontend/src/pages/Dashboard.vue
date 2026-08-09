<script setup>
    import Header from '../components/Header.vue';
    import OverviewCards from '../components/OverviewCards.vue';
    import { ref } from 'vue';

    const date = new Date();
    const projectsActive = ref(5);
    const tasksInProgress = ref(3);
    const tasksCompletedThisMonth = ref(18);
    const tasksOverdue = ref(2);

    // fetch /api/projects
    const projects = ref([
        { project_id: 1, project_name: "Projet 1", project_description: "Description du projet 1", project_creation_date: "01/01/2026" },
        { project_id: 2, project_name: "Trojet 2", project_description: "Description du projet 2", project_creation_date: "15/02/2026" },
        { project_id: 3, project_name: "Crojet 3", project_description: "Description du projet 3", project_creation_date: "20/03/2026" },
        { project_id: 4, project_name: "Frojet 4", project_description: "Description du projet 4", project_creation_date: "05/04/2026" },
        { project_id: 5, project_name: "Trojet 5", project_description: "Description du projet 5", project_creation_date: "10/05/2026" },
        { project_id: 6, project_name: "Projet 6", project_description: "Description du projet 6", project_creation_date: "15/06/2026" },
        { project_id: 7, project_name: "Projet 7", project_description: "Description du projet 7", project_creation_date: "20/07/2026" },
        { project_id: 8, project_name: "Projet 8", project_description: "Description du projet 8", project_creation_date: "25/08/2026" },
        { project_id: 9, project_name: "Projet 9", project_description: "Description du projet 9", project_creation_date: "30/09/2026" },
        { project_id: 10, project_name: "Projet 10", project_description: "Description du projet 10", project_creation_date: "05/10/2026" },
    ]);

    const projectsFiltered = ref([...projects.value]);

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

    // fetch /api/tasks/project_id/count
    const tasksByProject = ref([
        { project_id: 1, tasks: 5 },
        { project_id: 2, tasks: 3 },
        { project_id: 3, tasks: 8 },
        { project_id: 4, tasks: 2 },
        { project_id: 5, tasks: 6 },
        { project_id: 6, tasks: 6 },
        { project_id: 7, tasks: 4 },
        { project_id: 8, tasks: 7 },
        { project_id: 9, tasks: 5 },
        { project_id: 10, tasks: 3 },
    ]);

    // fetch /api/tasks/project_id/done/count
    const tasksDoneByProject = ref([
        { project_id: 1, tasks_done: 3 },
        { project_id: 2, tasks_done: 1 },
        { project_id: 3, tasks_done: 5 },
        { project_id: 4, tasks_done: 2 },
        { project_id: 5, tasks_done: 4 },
        { project_id: 6, tasks_done: 5 },
        { project_id: 7, tasks_done: 3 },
        { project_id: 8, tasks_done: 6 },
        { project_id: 9, tasks_done: 4 },
        { project_id: 10, tasks_done: 2 },
    ]);
    

    const getProjectTasks = (project_id) => {
        const found = tasksByProject.value.find(p => p.project_id === project_id);
        return found ? found.tasks : 0;
    };

    const getProjectTasksDone = (project_id) => {
        const found = tasksDoneByProject.value.find(p => p.project_id === project_id);
        return found ? found.tasks_done : 0;
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
        const projectColor = progressColors.value[project_id > progressColors.value.length ? (project_id - progressColors.value.length - 1) : (project_id - 1)];
        return projectColor;
    };

    const filterProjects = (event) => {
        const searchTerm = event.target.value.toLowerCase();
        projectsFiltered.value = projects.value.filter(project => project.project_name.toLowerCase().includes(searchTerm));
    };

</script>

<template>
    <main class="text-white min-h-screen">
        <div id="header-row" class="grid grid-cols-3">
            <div id="header-col" class="col-span-1">
                <Header />
            </div>
            <div id="search-col" class="col-span-1 items-center flex justify-center">
                <input class="w-full rounded-md px-4 py-2 text-gray-400 border border-gray-500" 
                style="background-color: var(--input-bg);" 
                type="text" placeholder="&#128269; Rechercher..."  
                @input="filterProjects"
                />
            </div>
            <div id="logout-col" class="col-span-1 flex items-center justify-end px-20">
                <a href="#" class="text-white">[→ Déconnexion</a>
            </div>
        </div>    
        <hr class="mb-10 border-gray-500" />
        <div id="layout-dashboard" class="mx-20">
            <div id="first-row" class="grid grid-cols-2">
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
                    <button class="bg-purple-500 text-white rounded-md px-4 h-10">+ Nouveau projet</button>
                </div>
            </div>
            <div id="overview" class="grid grid-cols-4 gap-4 mt-10">
                <OverviewCards label="Projet Actifs" :value="projectsActive"></OverviewCards>
                <OverviewCards label="Tâches en cours" :value="tasksInProgress"></OverviewCards>
                <OverviewCards label="Terminées ce mois" :value="tasksCompletedThisMonth"></OverviewCards>
                <OverviewCards label="En retard" :value="tasksOverdue"></OverviewCards>
            </div>
            <div id="mes_projets" class="mt-10">
                <p class="text-xl font-bold">Mes Projets</p>
                <div class="grid grid-cols-3 gap-4">
                    <div v-for="project in projectsFiltered" :key="project.project_id" class="border border-gray-500 rounded-md p-4"  style="background-color: var(--input-bg);">
                        <div :class="[`text-2xl font-bold mb-2 border rounded-md w-fit py-2 px-4`, getProjectColor(project.project_id)]">{{ project.project_name[0] }}</div>
                        <h2 class="text-lg font-bold">{{ project.project_name }}</h2>
                        <p>{{ project.project_description }}</p>
                        <!-- barre de progression -->
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
                    <!-- Ajout projet -->
                    <div id="add-project-div" class="border border-gray-500 rounded-md p-4 flex flex-col items-center justify-center"  style="background-color: var(--input-bg);">
                        <div class="text-lg font-bold border border-dashed text-center p-2 w-32 rounded-md">+</div>
                        <p class="text-center">Nouveau projet.</p>
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