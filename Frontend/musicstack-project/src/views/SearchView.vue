<template>
  <div class="search-page">
    <SearchBar
      v-model="keyword"
      placeholder="Search again..."
      @search="search"
    />

    <p class="result-text">
      "{{ keyword }}" 검색 결과
    </p>

    <!-- 🔥 LLM 로딩 애니메이션
    <LLMLoading v-if="searchStore.isLoading" /> -->

    <!-- 검색 결과 리스트 -->
     
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'

const route = useRoute()
const keyword = ref(route.query.q || '')

/* 검색 실행 */
const search = (value) => {
  keyword.value = value
  console.log('검색 실행:', value)
  // axios 검색 API 호출 자리
}

/* URL 쿼리 바뀔 때 대응 */
watch(
  () => route.query.q,
  (newQ) => {
    if (newQ) {
      keyword.value = newQ
      search(newQ)
    }
  },
  { immediate: true }
)
</script>

<style>
  
</style>