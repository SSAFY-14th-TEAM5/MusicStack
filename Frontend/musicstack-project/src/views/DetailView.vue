<template>
  <div>
    <h1>Detail</h1>
    <div v-if="article">
      <p>글 번호: {{ article.id }}</p>
      <p>제목: {{ article.title }}</p>
      <p>내용: {{ article.content }}</p>
      <p>작성시간: {{ article.created_at }}</p>
      <p>수정시간: {{ article.updated_at }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/articles'

const store = useArticleStore()
const route = useRoute()
const article = ref(null)
const articleId = route.params.id

onMounted(() => {
  store.getArticleDetail(articleId)
    .then(res => {
      article.value = res.data
    })
    .catch(err => {
      console.log(err)
    })
})
</script>

<style>

</style>
