<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-custom px-4">
      <div class="container-fluid d-flex align-items-center">

        <!-- 좌측 메뉴 -->
        <div class="d-flex gap-3">
          <RouterLink
            class="nav-link-custom"
            :to="{ name: 'Home' }"
          >
            Home
          </RouterLink>

          <RouterLink
            v-if="accountStore.isLogin"
            class="nav-link-custom"
            :to="{ name: 'ArticleView' }"
            >
              Community
          </RouterLink>

          <RouterLink
            v-if="accountStore.isLogin"
            class="nav-link-custom"
            :to="{ name: 'RecommendView' }"
            >
              AI 추천
          </RouterLink>
            
        </div>

        <!-- 가운데 브랜드 -->
        <div class="mx-auto navbar-brand-custom">
          <RouterLink
            :to="{ name: 'Home' }"
            class="brand-link"
          >
            🎵 MusicStack
          </RouterLink>
        </div>

        <!-- 우측 메뉴 -->
        <div class="d-flex align-items-center gap-3">
          <RouterLink
            v-if="!accountStore.isLogin"
            class="nav-link-custom"
            :to="{ name: 'SignUpView' }"
          >
            Sign Up
          </RouterLink>

          <RouterLink
            v-if="!accountStore.isLogin"
            class="nav-link-custom"
            :to="{ name: 'LogInView' }"
          >
            Login
          </RouterLink>

          <RouterLink
            v-if="accountStore.isLogin"
            class="nav-link-custom"
            :to="{ name: 'ProfileView' }"
          >
            My Page
          </RouterLink>

          <button
            v-if="accountStore.isLogin"
            class="logout-btn"
            @click="logOut"
          >
            Logout
          </button>
        </div>

      </div>
    </nav>
  </header>
  <RouterView v-slot="{ Component }">
    <Transition name="page" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>

</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>


<style scoped>
  /* Navbar 배경 */
  .navbar-custom {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    height: 64px;
  }

  /* 브랜드 */
  .navbar-brand-custom {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .brand-link {
    color: white;
    font-weight: 700;
    font-size: 1.25rem;
    text-decoration: none;
    letter-spacing: 0.5px;
    transition: opacity 0.2s ease;
  }

  .brand-link:hover {
    opacity: 0.85;
  }

  /* 메뉴 링크 */
  .nav-link-custom {
    color: white;
    text-decoration: none;
    font-weight: 500;
    position: relative;
    padding: 4px 2px;
    transition: color 0.2s ease, opacity 0.2s ease;
  }

  .nav-link-custom:hover {
    opacity: 0.85;
  }

  /* hover underline 효과 */
  .nav-link-custom::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0%;
    height: 2px;
    background-color: white;
    transition: width 0.25s ease;
  }

  .nav-link-custom:hover::after {
    width: 100%;
  }

  /* 로그아웃 버튼 */
  .logout-btn {
    background: rgba(255, 255, 255, 0.15);
    border: none;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9rem;
    transition: background 0.2s ease, transform 0.2s ease;
    cursor: pointer;
  }

  .logout-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  /*  현재 페이지(active) 강조 */
  .router-link-exact-active {
    font-weight: 700;
    opacity: 1;
  }

  /* underline을 항상 보이게 */
  .router-link-exact-active::after {
    width: 100%;
  }

  /* 페이지 전환 기본 */
  .page-enter-active,
  .page-leave-active {
    transition: opacity 0.35s ease, transform 0.35s ease;
  }

  /* 들어올 때 */
  .page-enter-from {
    opacity: 0;
    transform: translateY(12px);
  }

  /* 나갈 때 */
  .page-leave-to {
    opacity: 0;
    transform: translateY(-12px);
  }

</style>

