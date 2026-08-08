import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
    history: createWebHistory(),
    routes:[
        {path:'/', redirect:'/login'},
        {path:'/login', name: 'login', component: () => import('../pages/Login.vue')},
        {path:'/login2', name: 'login2', component: () => import('../pages/Login2.vue')},
        {path:'/dashboard', name: 'dashboard', component: () => import('../pages/Dashboard.vue')},
        {path:'/kanban', name: 'kanban', component: () => import('../pages/Kanban.vue')},
    ]
})