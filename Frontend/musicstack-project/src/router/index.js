import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import Home from '@/views/Home.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SearchView from '@/views/SearchView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreate from '@/components/ArticleCreate.vue'
import DetailView from '@/views/DetailView.vue'

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
    {
      path: '/profile',
      name: 'ProfileView',
      component : ProfileView
    },
    {
      path: '/search',
      name: 'SearchView',
      component : SearchView
    },
    {
      path: '/article',
      name: 'ArticleView',
      component : ArticleView
    },
    {
      path: '/article/create',
      name: 'ArticleCreate',
      component : ArticleCreate
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/liked/:trackId',
      name: 'UserLikedItem',
      component: () => import('@/components/UserLikedItem.vue'),
    },
    {
      path: '/tracks/:trackId',
      name: 'UserLikedItem',
      component: () => import('@/components/UserLikedItem.vue'),
    },

  ],
})

// to.name 수정 필요
router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  if (to.name === 'ProfileView' && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'Home' }
  }
})

export default router
