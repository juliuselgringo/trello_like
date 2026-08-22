<script setup>
    const handleLogout = async () => {
        try {
            await fetch('http://localhost:8000/api/auth/logout/', {
                method: 'POST',
                credentials: 'include',
            });
            window.location.href = '/login';
        } catch (error) {
            console.error('Logout failed', error);
        }
    }
</script>

<template>
    <div id="logout-col" class="mx-20">
                <a href="#" @click.prevent="handleLogout" class="text-white">[→ Déconnexion</a>
            </div>
</template>