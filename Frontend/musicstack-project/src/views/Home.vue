<template>
  <section class="hero">
    <!-- 배경 오버레이 -->
    <div class="overlay"></div>

    <!-- 중앙 콘텐츠 -->
    <div class="hero-content">
      <p class="hero-subtitle">DISCOVER YOUR SOUND</p>
      <h1 class="hero-title">MusicStack</h1>

      <!-- 재사용 검색창 -->
      <SearchBar
        v-model="keyword"
        @search="onSearch"
      />
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'

const router = useRouter()
const keyword = ref('')

const onSearch = (keyword) => {
  router.push({
    name: 'SearchView',
    query: { q: keyword },
  })
}
</script>

<style scoped>
/* ===== 전체 히어로 ===== */
.hero {
  position: relative;
  width: 100%;
  height: calc(100vh - 72px);
  background: #0a0a0a;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* ===== 어두운 오버레이 + 패턴 ===== */
.overlay {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(ellipse at 20% 80%, rgba(212, 255, 0, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(212, 255, 0, 0.05) 0%, transparent 50%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 1px,
      rgba(255, 255, 255, 0.02) 1px,
      rgba(255, 255, 255, 0.02) 2px
    );
  z-index: 1;
}

/* 움직이는 그라디언트 원 */
.overlay::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(212, 255, 0, 0.1) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: pulse-bg 4s ease-in-out infinite;
}

@keyframes pulse-bg {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.8;
  }
}

/* ===== 중앙 콘텐츠 ===== */
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: 0 24px;
  animation: fadeUp 1s ease-out forwards;
}

/* ===== 서브타이틀 ===== */
.hero-subtitle {
  font-size: 0.85rem;
  letter-spacing: 6px;
  color: #D4FF00;
  margin-bottom: 16px;
  font-weight: 500;
  text-transform: uppercase;
  opacity: 0;
  animation: fadeUp 0.8s ease-out 0.2s forwards;
}

/* ===== 메인 타이틀 ===== */
.hero-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 6rem;
  font-weight: 400;
  margin-bottom: 48px;
  color: #ffffff;
  letter-spacing: 8px;
  text-shadow: 0 0 60px rgba(212, 255, 0, 0.3);
  opacity: 0;
  animation: fadeUp 0.8s ease-out 0.4s forwards;
}

/* 타이틀 강조 효과 */
.hero-title::after {
  content: '';
  display: block;
  width: 80px;
  height: 4px;
  background: #D4FF00;
  margin: 24px auto 0;
  border-radius: 2px;
  box-shadow: 0 0 20px rgba(212, 255, 0, 0.6);
}

/* ===== 애니메이션 ===== */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== 반응형 ===== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 3.5rem;
    letter-spacing: 4px;
    margin-bottom: 36px;
  }

  .hero-subtitle {
    font-size: 0.75rem;
    letter-spacing: 4px;
  }

  .overlay::before {
    width: 300px;
    height: 300px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }
}
</style>
