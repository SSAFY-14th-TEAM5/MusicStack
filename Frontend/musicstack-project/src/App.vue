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
          >MusicStack
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
  /* ===== Navbar 배경 - 다크 테마 ===== */
  .navbar-custom {
    background: linear-gradient(180deg, #0d0d0d 0%, rgba(13, 13, 13, 0.95) 100%);
    backdrop-filter: blur(12px);
    height: 72px;
    border-bottom: 1px solid rgba(212, 255, 0, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
  }

  /* ===== 브랜드 ===== */
  .navbar-brand-custom {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .brand-link {
    color: #D4FF00;
    font-family: 'Bebas Neue', sans-serif;
    font-weight: 400;
    font-size: 1.6rem;
    text-decoration: none;
    letter-spacing: 2px;
    transition: all 0.25s ease;
    text-shadow: 0 0 20px rgba(212, 255, 0, 0.4);
  }

  .brand-link:hover {
    text-shadow: 0 0 30px rgba(212, 255, 0, 0.7);
    transform: scale(1.02);
  }

  /* ===== 메뉴 링크 ===== */
  .nav-link-custom {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    position: relative;
    padding: 6px 4px;
    transition: color 0.25s ease;
  }

  .nav-link-custom:hover {
    color: #D4FF00;
  }

  /* hover underline 효과 */
  .nav-link-custom::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0%;
    height: 2px;
    background: linear-gradient(90deg, #D4FF00, #E6FF33);
    transition: width 0.25s ease;
    box-shadow: 0 0 10px rgba(212, 255, 0, 0.5);
  }

  .nav-link-custom:hover::after {
    width: 100%;
  }

  /* ===== 로그아웃 버튼 ===== */
  .logout-btn {
    background: transparent;
    border: 1px solid rgba(212, 255, 0, 0.4);
    color: #D4FF00;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.25s ease;
    cursor: pointer;
  }

  .logout-btn:hover {
    background: #D4FF00;
    color: #0a0a0a;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(212, 255, 0, 0.3);
  }

  /* ===== 현재 페이지(active) 강조 ===== */
  .router-link-exact-active {
    color: #D4FF00 !important;
    font-weight: 600;
  }

  /* underline을 항상 보이게 */
  .router-link-exact-active::after {
    width: 100%;
  }

  /* ===== 페이지 전환 애니메이션 ===== */
  .page-enter-active,
  .page-leave-active {
    transition: opacity 0.4s ease, transform 0.4s ease;
  }

  /* 들어올 때 */
  .page-enter-from {
    opacity: 0;
    transform: translateY(16px);
  }

  /* 나갈 때 */
  .page-leave-to {
    opacity: 0;
    transform: translateY(-16px);
  }

</style>

