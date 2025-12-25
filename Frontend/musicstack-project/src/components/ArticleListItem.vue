<template>
  <div class="article-card">
    <div class="card-header">
      <h3 class="title">
        {{ article.title }}
        <span class="comment-count">
        💬 {{ article.comment_count }}
      </span>
      </h3>
    </div>

    <p class="content">
      {{ article.content }}
    </p>

    <div class="card-footer">
      <RouterLink
        class="detail-link"
        :to="{ name: 'DetailView', params: { id: article.id } }"
      >
        자세히 보기 →
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
  import { RouterLink } from 'vue-router'
  defineProps({
    article: Object,
  })
</script>

<style scoped>
/* 카드 전체 */
.article-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* hover 효과 */
.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.15);
}

/* 제목 */
.title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #222;
}

/* 내용 미리보기 */
.content {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.5;
  margin-bottom: 16px;

  /* 2줄까지만 표시 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 하단 영역 */
.card-footer {
  display: flex;
  justify-content: flex-end;
}

/* 디테일 링크 */
.detail-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6a11cb;
  text-decoration: none;
  transition: color 0.2s ease;
}

.detail-link:hover {
  color: #2575fc;
}

/* 모바일 대응 */
@media (max-width: 480px) {
  .article-card {
    padding: 18px 16px;
  }

  .title {
    font-size: 1rem;
  }
}
</style>