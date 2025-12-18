import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component : Home
    },
    {
      path: '/login',
      name: 'LogInView',
      component : LogInView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component : SignUpView
    },
  ],
})

export default router
