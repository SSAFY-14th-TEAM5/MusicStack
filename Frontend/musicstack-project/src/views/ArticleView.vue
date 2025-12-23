<template>
  <div>
    <h1>Article</h1>
      <RouterLink 
        :to="{ name: 'ArticleCreate' }"
      >
        <button>New</button>
    </RouterLink>
    
    <ArticleList />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useArticleStore } from '@/stores/articles'
 import ArticleList from '@/components/ArticleList.vue'
const store = useArticleStore()
// const articles = ref([])  // 로컬 테스트용 코드 (향후 삭제)

onMounted(() => {
  store.getArticles() // DB에 저장된 게시글 불러오기
  // articles.value = [  // 로컬 테스트용 코드 (향후 삭제)
  //   { pk: 1, title: '로컬 테스트', content: '백엔드 없음' },
  //   { pk: 2, title: '로컬 테스트2', content: '백엔드 없음2' },
  //   { pk: 3, title: '로컬 테스트3', content: '백엔드 없음3' },
  // ]
})
</script>

<style scoped>

</style>