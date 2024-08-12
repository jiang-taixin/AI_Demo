import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Edit from '@/views/Edit.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path:'/',
      name:'login',
      component: Login
    },
    {
      path:'/register',
      name:'register',
      component: Register
    },
    {
      path:'/edit',
      name:'edit',
      component: Edit
    }
  ]
})

export default router
