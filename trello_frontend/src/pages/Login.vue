<script setup>

</script>

<template>
    <main class="text-white h-screen"> 
        <h1 class="font-bold text-3xl flex items-center p-6"><img class="m-2 h-10 w-10 rounded" id="logo" src="../../img/Capture d'écran 2026-08-07 084620.png">Taskflow</h1>
        <div id="layout" class="grid grid-cols-2 mx-20 gap-60">
            <div class="mt-24 col-span-1" id="presentation">
                <div id="accroche" class="text-5xl">
                    <p>Organisez.</p>
                    <p class="text-purple-500">Collaborez.</p>
                    <p>Livrez.</p>
                </div>
            
                <p class="mt-10">Gérez vos projets avec une clarté absolue. Kanban, deadlines, et suivi en temps réel - tout au même endroit.</p>
            
                <ul class="mt-10 list-inside space-y-2">
                    <li>✅ Tableau Kanban illimités</li>
                    <li>✅ Collaboration en temps réel</li>
                    <li>✅ Statistiques avancées</li>
                </ul>
        
            </div>

            <form class="mt-24 col-span-1 space-y-5" action="">
                <h2 class="font-bold text-2xl">Bon retour &#x1F44B;</h2>
                <p>Connectez-vous à votre espace de travail.</p>
                <label>
                    <span class="block">Adresse Mail</span>
                    <input class="rounded-md w-full h-10 border border-gray-700" type="email">
                </label>
                <label>
                    <span class="mt-6 block">Mot de passe</span>
                    <input class="rounded-md w-full h-10 border border-gray-700" type="password">
                    
                </label>
                <div class="text-right">
                    <a class="text-purple-500" href="" target="blank">Mot de passe oublié?</a>
                </div>
                <button class="py-2 bg-purple-500 rounded-md w-full">Se Connecter -> </button>
                <p class="text-center">Pas encore de compte ? <a class="text-purple-500" href="" target="blank">S'inscrire</a></p>
            </form>

        </div>
        <footer class="ml-20 mt-50 text-gray-400">
            <p>&copy; 2026 Taskflow. Tous droits réservés.</p> 
        </footer>
    </main>

</template>

<style>
    main{
        background-image: linear-gradient(135deg, purple 10%, black 50%);
        min-height: 100vh;
    }

    input {
        background-color: rgb(48, 46, 46);
        color: white;
    }
</style>