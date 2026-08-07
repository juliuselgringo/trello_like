import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
    history: createWebHistory(),
    routes:[
        {path:'/login', name: 'login', component: () => import('../pages/Login.vue')},
    ]
})