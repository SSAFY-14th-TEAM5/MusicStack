<template>
  <div class="article-page">
    <div class="article-header">
      <h1>Community</h1>

      <RouterLink :to="{ name: 'ArticleCreate' }">
        <button class="new-btn">New</button>
      </RouterLink>
    </div>

    <ArticleList />

    <!-- 페이지네이션 -->
    <div class="pagination-wrapper">
      <!-- 이전 -->
      <button
        class="page-btn"
        :disabled="store.currentPage === 1"
        @click="goPage(store.currentPage - 1)"
      >
        ← 이전
      </button>

      <!-- 숫자 버튼 -->
      <button
        v-for="page in pageNumbers"
        :key="page"
        class="page-number"
        :class="{ active: page === store.currentPage }"
        @click="goPage(page)"
      >
        {{ page }}
      </button>

      <!-- 다음 -->
      <button
        class="page-btn"
        :disabled="store.currentPage === store.totalPages"
        @click="goPage(store.currentPage + 1)"
      >
        다음 →
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { RouterLink, useRouter, useRoute } from 'vue-router';
import { useArticleStore } from '@/stores/articles'
import ArticleList from '@/components/ArticleList.vue'
const store = useArticleStore()
const router = useRouter()
const route = useRoute()
// const articles = ref([])  // 로컬 테스트용 코드 (향후 삭제)

// onMounted(() => {
//   store.getArticles(1) // DB에 저장된 게시글 불러오기
//   // articles.value = [  // 로컬 테스트용 코드 (향후 삭제)
//   //   { pk: 1, title: '로컬 테스트', content: '백엔드 없음' },
//   //   { pk: 2, title: '로컬 테스트2', content: '백엔드 없음2' },
//   //   { pk: 3, title: '로컬 테스트3', content: '백엔드 없음3' },
//   // ]
// })

/*  URL(page) 변경 감지 → 게시글 다시 요청 */
watch(
  () => route.query.page,
  (newPage) => {
    const page = Number(newPage) || 1
    store.getArticles(page)

    // 페이지 변경 후 스크롤 맨 위로
    window.scrollTo({
      top: 0,
      behavior: 'smooth', // 부드러운 스크롤
    })
  },
  { immediate: true }
)

/* 현재 페이지 기준 ±2 페이지만 보여주기 */
const pageNumbers = computed(() => {
  const pages = []
  const start = Math.max(1, store.currentPage - 2)
  const end = Math.min(store.totalPages, store.currentPage + 2)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// 페이지 이동함수
const goPage = (page) => {
  router.push({
    name: 'ArticleView',
    query: { page }
  })
}
</script>

<style scoped>
  .article-page {
    max-width: 960px;
    margin: 0 auto;
    padding: 48px 24px 100px;
    min-height: 100vh;
  }

  /* 헤더 영역 */
  .article-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
  }

  .article-header h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    font-weight: 400;
    letter-spacing: 4px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .article-header h1::before {
    content: '';
    width: 4px;
    height: 32px;
    background: #D4FF00;
    border-radius: 2px;
    box-shadow: 0 0 15px rgba(212, 255, 0, 0.5);
  }

  /* New 버튼 */
  .new-btn {
    padding: 12px 28px;
    border-radius: 28px;
    border: 1px solid #D4FF00;
    background: transparent;
    color: #D4FF00;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .new-btn:hover {
    background: #D4FF00;
    color: #0a0a0a;
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(212, 255, 0, 0.3);
  }

  /* 페이지네이션 */
  .pagination-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    margin: 56px 0 24px;
  }

  /* 이전 / 다음 버튼 */
  .page-btn {
    padding: 12px 24px;
    border-radius: 28px;
    border: 1px solid #2a2a2a;
    font-size: 0.9rem;
    font-weight: 600;
    background: #1a1a1a;
    color: #a0a0a0;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  /* hover */
  .page-btn:hover:not(:disabled) {
    border-color: #D4FF00;
    color: #D4FF00;
    transform: translateY(-2px);
  }

  /* 비활성 */
  .page-btn:disabled {
    background: #141414;
    color: #444444;
    cursor: not-allowed;
    border-color: #1e1e1e;
  }

  /* 현재 페이지 */
  .current-page {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #D4FF00;
    color: #0a0a0a;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(212, 255, 0, 0.3);
  }

  /* 숫자 버튼 */
  .page-number {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: 1px solid #2a2a2a;
    background: #1a1a1a;
    color: #a0a0a0;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.25s ease;
  }

  /* hover */
  .page-number:hover {
    transform: translateY(-3px);
    border-color: #D4FF00;
    color: #D4FF00;
  }

  /* 활성 페이지 */
  .page-number.active {
    background: #D4FF00;
    color: #0a0a0a;
    border-color: #D4FF00;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(212, 255, 0, 0.4);
    transform: translateY(-3px);
  }

  /* 활성 페이지 hover 방지 */
  .page-number.active:hover {
    transform: translateY(-3px);
  }
</style>