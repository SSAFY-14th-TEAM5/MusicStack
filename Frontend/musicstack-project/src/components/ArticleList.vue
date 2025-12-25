<template>
  <div class="article-list">
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
  import { useArticleStore } from '@/stores/articles'
  import ArticleListItem from '@/components/ArticleListItem.vue'

  const store = useArticleStore()

</script>

<style scoped>
/* 게시글 리스트 전체 레이아웃 */
.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>