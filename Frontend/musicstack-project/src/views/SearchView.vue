<template>
  <div class="search-page">
    <SearchBar
      v-model="keyword"
      placeholder="Search again..."
      @search="search"
    />

    <!-- 로딩 -->
    <!-- <p v-if="searchStore.loading">LLM 분석 중...</p> -->
    <Transition name="fade">
      <LLMLoading v-if="searchStore.loading" />
    </Transition>

    <!-- 실패 -->
    <p v-if="!searchStore.loading && !searchStore.success" class="empty-text">
      찾고 있는 노래가 없어요 😢 <br />
      다른 아티스트로 다시 검색해볼까요?
    </p>


    <!-- 성공 -->
    <div v-if="searchStore.success">
      <h2>{{ searchStore.artist[0] }}</h2>
    
      <div class="track-info">
        <div v-for="track in visibleTracks" :key="track.id" class="track-card">
          <img :src="track.album_image" alt="앨범 이미지">
          <p class="track-title">{{ track.track_name }}</p>
          <p class="track-year">{{ track.release_year }}</p>
          <button @click="favoriteStore.saveFavorite(track)"
            class="like-btn">
            ❤️ 좋아요
          </button>
        </div>
      </div>

      <!-- 더보기 버튼 -->
      <button
        v-if="visibleCount < searchStore.tracks.length"
        class="load-more"
        @click="loadMore"
      >
        {{ searchStore.tracks.length - visibleCount > 3
          ? '다른 노래는 어때요?'
          : '마지막 곡 보기' }}
      </button>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'
import LLMLoading from '@/components/LLMLoading.vue'
import { useAccountStore } from '@/stores/accounts'
import { useSearchStore } from '@/stores/searchs'
import { useFavoriteStore } from '@/stores/favorite'

const route = useRoute()
const router = useRouter()
const keyword = ref(route.query.q || '')
const accountStore = useAccountStore()
const searchStore = useSearchStore()
const favoriteStore = useFavoriteStore()

const likeTrack = (track) => {
  if (!accountStore.userPk) {
    alert('로그인이 필요합니다.')
    return
  }

  favoriteStore.saveFavorite(track)
}

/* 🔹 몇 개까지 보여줄지 */
const visibleCount = ref(1)

/* 🔹 실제 화면에 보여줄 트랙 */
const visibleTracks = computed(() =>
  searchStore.tracks.slice(0, visibleCount.value)
)

/* 검색 */
const search = (value) => {
  visibleCount.value = 1 // 검색 바뀌면 초기화
  router.push({
    name: 'SearchView',
    query: { q: value },
  })
}

// onMounted(async () => {
//   // persist 복원 대기
//   await nextTick()

//   const q = route.query.q
//   if (q) {
//     searchStore.search(q)
//   }
// })

/* URL 변경 감지 */
watch(
  () => route.query.q,
  (newQ) => {
    if (!newQ) return
    visibleCount.value = 1
    searchStore.search(newQ)
  }
)

/* 더 보기 버튼 */
const loadMore = () => {
  visibleCount.value = Math.min(
    visibleCount.value + 3,
    searchStore.tracks.length
  )
}
</script>

<style>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.25s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  .search-page {
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }

  .search-page h2 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 36px 0 24px;
  }
  .track-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
  }
  .track-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    cursor: pointer;
  }

  .track-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.15);
  }
  .track-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
  }
  .track-info {
  padding: 14px 16px 18px;
}

  .track-title {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 6px;
  }

  .track-year {
    font-size: 0.8rem;
    color: #888;
  }
  .like-btn {
    margin-top: 10px;
    width: 100%;
    border: none;
    padding: 10px;
    border-radius: 20px;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    font-weight: 600;
    cursor: pointer;
    opacity: 0;
    transform: translateY(6px);
    transition: all 0.2s ease;
  }

  .track-card:hover .like-btn {
    opacity: 1;
    transform: translateY(0);
  }
  .load-more {
    display: block;
    margin: 48px auto 0;
    padding: 14px 36px;
    border-radius: 30px;
    border: none;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .load-more:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.25);
  }
  .empty-text {
    margin-top: 40px;
    text-align: center;
    color: #888;
    font-size: 0.95rem;
  }



</style>