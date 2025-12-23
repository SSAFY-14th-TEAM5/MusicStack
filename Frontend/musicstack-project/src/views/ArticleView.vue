Community
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
        @click="store.getArticles(store.currentPage - 1)"
      >
        ← 이전
      </button>

      <!-- 숫자 버튼 -->
      <button
        v-for="page in pageNumbers"
        :key="page"
        class="page-number"
        :class="{ active: page === store.currentPage }"
        @click="store.getArticles(page)"
      >
        {{ page }}
      </button>

      <!-- 다음 -->
      <button
        class="page-btn"
        :disabled="store.currentPage === store.totalPages"
        @click="store.getArticles(store.currentPage + 1)"
      >
        다음 →
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useArticleStore } from '@/stores/articles'
import ArticleList from '@/components/ArticleList.vue'
const store = useArticleStore()
// const articles = ref([])  // 로컬 테스트용 코드 (향후 삭제)

onMounted(() => {
  store.getArticles(1) // DB에 저장된 게시글 불러오기
  // articles.value = [  // 로컬 테스트용 코드 (향후 삭제)
  //   { pk: 1, title: '로컬 테스트', content: '백엔드 없음' },
  //   { pk: 2, title: '로컬 테스트2', content: '백엔드 없음2' },
  //   { pk: 3, title: '로컬 테스트3', content: '백엔드 없음3' },
  // ]
})

/* 🔹 현재 페이지 기준 ±2 페이지만 보여주기 */
const pageNumbers = computed(() => {
  const pages = []
  const start = Math.max(1, store.currentPage - 2)
  const end = Math.min(store.totalPages, store.currentPage + 2)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>

<style scoped>
  .article-page {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }

  /* 헤더 영역 */
  .article-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }

  .article-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #222;
  }

  /* New 버튼 */
  .new-btn {
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .new-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
  }
/* 페이지네이션 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  margin: 48px 0 20px;
}

/* 이전 / 다음 버튼 */
.page-btn {
  padding: 10px 18px;
  border-radius: 24px;
  border: none;
  font-size: 0.9rem;
  font-weight: 600;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* hover */
.page-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
}

/* 비활성 */
.page-btn.disabled {
  background: #e0e0e0;
  color: #999;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

/* 현재 페이지 */
.current-page {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: white;
  color: #2575fc;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 14px rgba(0,0,0,0.15);
}

/* 숫자 버튼 */
.page-number {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;

  background: white;
  color: #555;

  font-size: 0.9rem;
  font-weight: 600;

  cursor: pointer;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

/* hover */
.page-number:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15);
  color: #2575fc;
}

/* 활성 페이지 */
.page-number.active {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-weight: 700;

  box-shadow: 0 8px 20px rgba(106, 17, 203, 0.45);
  transform: translateY(-2px);
}

/* 활성 페이지 hover 방지 */
.page-number.active:hover {
  transform: translateY(-2px);
}
</style>