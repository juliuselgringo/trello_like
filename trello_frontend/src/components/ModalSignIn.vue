<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        user_name: String,
        user_email: String,
        user_password: String,
    });

    const emit = defineEmits(['create', 'cancel']);

    const password_confirmation = ref('');

    const isPasswordConfirmed = computed(() => formData.value.user_password === password_confirmation.value);

    const formData = ref({
        user_name: props.user_name || '',
        user_email: props.user_email || '',
        user_password: props.user_password || '',
    });

    const handleSubmit = () => {
        if (isPasswordConfirmed.value) {
            emit("create", formData.value);
        } else {
            alert("Les mots de passe ne correspondent pas");
        }
    };

</script>

<template>
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white rounded-lg p-6 w-96">
            <h2 class="text-xl text-gray-900 font-bold mb-4">
                Créer un compte
            </h2>
            <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                    <label for="name" class="block text-gray-700">
                        Nom
                    </label>
                    <input 
                    v-model="formData.user_name" 
                    type="text" id="name" 
                    class="w-full border border-gray-300 rounded-md p-2" required 
                    />
                </div>
                <div class="mb-4">
                    <label for="email" class="block text-gray-700">Email</label>
                    <input v-model="formData.user_email" type="email" id="email" class="w-full border border-gray-300 rounded-md p-2" required />
                </div>
                <div class="mb-4">
                    <label for="password" class="block text-gray-700">Mot de passe</label>
                    <input v-model="formData.user_password" type="password" id="password" class="w-full border border-gray-300 rounded-md p-2" required />
                </div>
                <div class="mb-4">
                    <label for="password_confirmation" class="block text-gray-700">
                        Confirmer le mot de passe
                    </label>
                    <input v-model="password_confirmation" type="password" id="password_confirmation" class="w-full border border-gray-300 rounded-md p-2" required />
                </div>
                <button
                type="submit"
                class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
                >
                    Enregistrer
                </button>
                <button
                type="button"
                class="ml-2 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                @click="emit('cancel')"
                >
                    Annuler
                </button>

            </form>
        </div>
    </div>
</template>