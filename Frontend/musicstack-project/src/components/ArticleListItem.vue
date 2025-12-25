<template>
  <div class="article-card">
    <div class="card-header">
      <h3 class="title">
        {{ article.title }}
        <span class="comment-count">
        💬 {{ article.comment_count }}
      </span>
      <span class="author">
        @{{ article.author.nickname }}
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
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 18px;
  padding: 24px 28px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.25s ease;
}

/* hover 효과 */
.article-card:hover {
  transform: translateY(-6px);
  border-color: rgba(212, 255, 0, 0.3);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4), 0 0 30px rgba(212, 255, 0, 0.05);
}

/* 헤더 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

/* 제목 */
.title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 댓글 카운트 */
.comment-count {
  font-size: 0.8rem;
  font-weight: 500;
  color: #666666;
  background: #252525;
  padding: 4px 10px;
  border-radius: 12px;
}

/* 내용 미리보기 */
.content {
  font-size: 0.9rem;
  color: #888888;
  line-height: 1.6;
  margin-bottom: 18px;

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
  color: #D4FF00;
  text-decoration: none;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-link:hover {
  color: #E6FF33;
  gap: 8px;
}

/* 모바일 대응 */
@media (max-width: 480px) {
  .article-card {
    padding: 20px 18px;
  }

  .title {
    font-size: 1rem;
  }
}
</style>