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
  height: 100vh;
  background-image: url('https://images.unsplash.com/photo-1511379938547-c1f69419868d');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* ===== 어두운 오버레이 ===== */
.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    120deg,
    rgba(20, 0, 40, 0.75),
    rgba(0, 0, 0, 0.85)
  );
  z-index: 1;
}

/* ===== 중앙 콘텐츠 ===== */
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 720px;
  padding: 0 24px;

  /* 등장 애니메이션 */
  animation: fadeUp 0.9s ease-out forwards;
}

/* ===== 텍스트 ===== */
.hero-subtitle {
  font-size: 0.9rem;
  letter-spacing: 4px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 12px;
}

.hero-title {
  font-size: 3.8rem;
  font-weight: 800;
  margin-bottom: 36px;
  color: white;
}

/* ===== 애니메이션 ===== */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== 반응형 ===== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.6rem;
    margin-bottom: 28px;
  }

  .hero-subtitle {
    font-size: 0.8rem;
  }
}
</style>
