import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
    history: createWebHistory(),
    routes:[
        {path:'/', redirect:'/login'},
        {path:'/login', name: 'login', component: () => import('../pages/Login.vue')},
        {path:'/dashboard', name: 'dashboard', component: () => import('../pages/Dashboard.vue')},
        {path:'/kanban', name: 'kanban', component: () => import('../pages/Kanban.vue')},
    ]
})