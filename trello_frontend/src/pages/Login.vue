<script setup>
    import ModalSignIn from '@/components/ModalSignIn.vue';
    import Header from '../components/Header.vue';
    import { ref, computed, onUnmounted } from 'vue';

    // logique sign in modal
    const controller = new AbortController();

    const showModalSignIn = ref(false);

    const openModalSignIn = () => {
        showModalSignIn.value = true;
    };

    // POST /api/users/ pour créer un nouvel utilisateur
    const handleUserCreate = async (newUser) => {
            try {
                const response = await fetch('http://localhost:8000/api/auth/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newUser),
                    signal: controller.signal,
                });
                if (!response.ok) {
                    throw new Error('Erreur lors de la création de l\'utilisateur');
                }
                const data = await response.json();
                console.log('Utilisateur créé:', data);
            } catch (error) {
                console.error(error);
            } finally {
                showModalSignIn.value = false;
            }

    };

    // logique login
    const formData = ref({
        user_name: '',
        user_password: '',
    });

    const handleLogin = async () => {
        const user = formData.value;
        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(user),
                signal: controller.signal,
            });
            if (!response.ok) {
                throw new Error('Erreur lors de la connexion');
            }
            const data = await response.json();
            console.log('Utilisateur connecté:', data);
            //rediriger vers dashboard
            window.location.href = '/dashboard';
        } catch (error) {
            console.error(error);
        }
    };

    onUnmounted(() => {
        controller.abort();
    });

</script>

<template>
    <main class="text-white h-screen"> 
        <Header />        
        <div id="layout-login" class="grid grid-cols-2 mx-20 gap-60">
            <div id="presentation" class="mt-24 col-span-1">
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

            <form class="mt-24 col-span-1 space-y-5" @submit.prevent="handleLogin">
                <h2 class="font-bold text-2xl">Bon retour &#x1F44B;</h2>
                <p>Connectez-vous à votre espace de travail.</p>
                <label>
                    <span class="block">Nom d'utilisateur</span>
                    <input 
                    class="rounded-md w-full h-10 border border-gray-700" 
                    type="text" 
                    name="user_name"
                    v-model="formData.user_name">
                </label>
                <label>
                    <span class="mt-6 block">
                        Mot de passe
                    </span>
                    <input 
                    class="rounded-md w-full h-10 border border-gray-700" 
                    type="password" 
                    name="user_password"
                    v-model="formData.user_password">
                    
                </label>
                <div class="text-right">
                    <a class="text-purple-500" href="" target="blank">
                        Mot de passe oublié?
                    </a>
                </div>
                <!-- ATTENTION LIEN POUR LE DEV A MODIFIER -->
                <button class="py-2 bg-purple-500 rounded-md w-full" type="submit">
                    Se Connecter ->
                </button>
                <p class="text-center">
                    Pas encore de compte ? 
                    <button class="text-purple-500" @click="openModalSignIn">
                        S'enregistrer
                    </button>
                </p>
            </form>

        </div>

        <ModalSignIn 
            v-if="showModalSignIn"
            @create="handleUserCreate"
            @cancel="showModalSignIn = false" 
        />

        <footer class="ml-20 mt-50 text-gray-400">
            <p>
                &copy; 2026 Taskflow. Tous droits réservés.
            </p> 
        </footer>
        
    </main>

</template>

<style>
    main{
        background-image: var(--main-bg-login);
    }

    input {
        background-color: var(--input-bg);
        color: var(--input-color);
    }
</style>