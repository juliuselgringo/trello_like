<script setup>

</script>

<template>
    <main class="bg-gradient-to-br from-purple-500 to-black text-white h-screen">
        <h1 class="font-bold text-3xl flex items-center"><img class="m-2 h-8 w-8" id="logo" src="../../img/Capture d'écran 2026-08-07 084620.png">Taskflow</h1>
        <div id="layout" class="grid grid-cols-2 mx-20 gap-60">
            <div class="mt-24 col-span-1" id="presentation">
                <div id="accroche" class="text-5xl">
                    <p>Organisez.</p>
                    <p class="text-purple-500">Collaborez.</p>
                    <p>Livrez.</p>
                </div>
            
                <p class="mt-10">Gérez vos projets avec une clarté absolue. Kanban, deadlines, et suivi en temps réel - tout au même endroit.</p>
            
                <ul class="mt-10 list-inside">
                    <li>✅Tableau Kanban illimités</li>
                    <li>✅Collaboration en temps réel</li>
                    <li>✅Statistiques avancées</li>
                </ul>
        
            </div>

            <form class="mt-24 col-span-1" action="">
                <h2 class="font-bold text-2xl">Bon retour &#x1F44B;</h2>
                <p>Connectez-vous à votre espace de travail.</p>
                <label>
                    <span class="block">Adresse Mail</span>
                    <input  class="bg-white text-black rounded-md w-full">
                </label>
                <label>
                    <span class="block">Mot de passe</span>
                    <input class="bg-white text-black rounded-md w-full">
                    
                </label>
                <div class="text-right">
                    <a class="text-purple-500" href="" target="blank">Mot de passe oublié?</a>
                </div>
                <button class="py-2 bg-purple-500 rounded-md w-full">Se Connecter -> </button>
                <p>Pas encore de compte ? <a class="text-purple-500" href="" target="blank">S'inscrire</a></p>
            </form>

        </div>
        
        
    </main>

</template>

<style>

</style>