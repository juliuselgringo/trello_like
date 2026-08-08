<script setup>
    import Header from '../components/Header.vue';
    import OverviewCards from '../components/OverviewCards.vue';

    const date = new Date();
</script>

<template>
    <main class="text-white h-screen">
        <Header />
        <hr class="mb-10 border-gray-500" />
        <div id="greetings">
            <!-- date en français (samedi 8 aout 2026)-->
            <p id="date">{{ date.toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
            <h1 id="greeting" class="text-3xl font-bold">Bonjour, Julien &#128075;</h1>
        </div>
        <div id="overview" class="grid grid-cols-4">
            <OverviewCards label="Projet Actifs" />
            <OverviewCards label="Tâches en cours" />
            <OverviewCards label="Terminées ce mois" />
            <OverviewCards label="En retard" />
        </div>
    </main>

</template>

<style>
    main{
        background-image: var(--gradient-main);
    }
</style>