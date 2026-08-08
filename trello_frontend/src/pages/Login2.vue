<script setup>

</script>

<template>
    <main class="bg-gradient-to-br from-purple-600 to-black text-white min-h-screen flex flex-col">
        <!-- Header avec logo -->
        <header class="p-6">
            <h1 class="font-bold text-3xl flex items-center gap-3">
                <img class="h-10 w-10 rounded" id="logo" src="../../img/Capture d'écran 2026-08-07 084620.png">
                <span>Taskflow</span>
            </h1>
        </header>

        <!-- Main content -->
        <div class="flex-1 grid grid-cols-2 mx-20 gap-16 items-center py-20">
            <!-- Left: Présentation -->
            <div class="space-y-8">
                <div class="space-y-4">
                    <h2 class="text-6xl font-bold leading-tight">
                        <span>Organisez.</span><br>
                        <span class="text-purple-400">Collaborez.</span><br>
                        <span>Livrez.</span>
                    </h2>
                </div>
                
                <p class="text-lg text-gray-300">
                    Gérez vos projets avec une clarté absolue. Kanban, deadlines, et suivi en temps réel - tout au même endroit.
                </p>
                
                <ul class="space-y-3">
                    <li class="flex items-center gap-3">
                        <span class="text-2xl">✅</span>
                        <span>Tableaux Kanban illimités</span>
                    </li>
                    <li class="flex items-center gap-3">
                        <span class="text-2xl">✅</span>
                        <span>Collaboration en temps réel</span>
                    </li>
                    <li class="flex items-center gap-3">
                        <span class="text-2xl">✅</span>
                        <span>Statistiques avancées</span>
                    </li>
                </ul>
            </div>

            <!-- Right: Formulaire -->
            <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-8 border border-white border-opacity-10">
                <h2 class="font-bold text-3xl mb-2">Bon retour 👋</h2>
                <p class="text-gray-400 mb-6">Connectez-vous à votre espace de travail.</p>
                
                <form class="space-y-5">
                    <div>
                        <label class="block text-sm font-medium mb-2">Adresse Mail</label>
                        <input 
                            type="email"
                            placeholder="example@email.com"
                            class="w-full bg-gray-800 text-white rounded-lg px-4 py-3 border border-gray-700 focus:outline-none focus:border-purple-500"
                        >
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">Mot de passe</label>
                        <input 
                            type="password"
                            class="w-full bg-gray-800 text-white rounded-lg px-4 py-3 border border-gray-700 focus:outline-none focus:border-purple-500"
                        >
                    </div>

                    <div class="text-right">
                        <a href="#" class="text-purple-400 hover:text-purple-300 text-sm">Mot de passe oublié?</a>
                    </div>

                    <button type="submit" class="w-full bg-purple-600 hover:bg-purple-700 font-bold py-3 rounded-lg transition duration-200">
                        Se connecter →
                    </button>
                </form>

                <p class="text-center text-gray-400 mt-6">
                    Pas encore de compte? 
                    <a href="#" class="text-purple-400 hover:text-purple-300 font-medium">S'inscrire</a>
                </p>
            </div>
        </div>
    </main>
</template>

<style scoped>

</style>