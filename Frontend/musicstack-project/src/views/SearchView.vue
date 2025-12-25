<template>
  <div class="search-page">
    <SearchBar
      v-model="keyword"
      placeholder="Search again..."
      @search="search"
    />

    <!-- 로딩 -->
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
    
      <TransitionGroup name="list" tag="div" class="track-grid">
        <div v-for="track in visibleTracks" :key="track.track_id" class="track-card-wrapper">
          <div class="track-card">
            <!-- CD 디스크 효과 -->
            <div class="cd-disk">
              <img :src="track.album_image" alt="앨범 이미지" class="album-cover">
              <div class="cd-hole"></div>
            </div>
            
            <div class="track-details">
              <p class="track-title">{{ track.track_name }}</p>
              <p class="track-year">{{ track.release_year }}</p>
            </div>

            <button @click="toggleLike(track)" class="like-btn" :class="{ 'active': isLiked(track) }">
              <!-- SVG 하트 아이콘 -->
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="heart-icon">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              Like
            </button>
          </div>
        </div>
      </TransitionGroup>

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
import { ref, watch, computed, nextTick } from 'vue'
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

/* 🔹 좋아요 여부 확인 */
const isLiked = (track) => {
  if (!favoriteStore.favorites) return false
  return favoriteStore.favorites.some(fav => fav.track_id === track.track_id)
}

const likeTrack = (track) => {
  if (!accountStore.userPk) {
    alert('로그인이 필요합니다.')
    return
  }

  favoriteStore.saveFavorite(track)
}

/* 🔹 몇 개까지 보여줄지 */
const visibleCount = ref(4)

/* 🔹 실제 화면에 보여줄 트랙 */
const visibleTracks = computed(() =>
  searchStore.tracks.slice(0, visibleCount.value)
)

/* 검색 */
const search = (value) => {
  visibleCount.value = 4 // 검색 바뀌면 초기화
  router.push({
    name: 'SearchView',
    query: { q: value },
  })
}

/* URL 변경 감지 */
watch(
  () => route.query.q,
  (newQ) => {
    if (!newQ) return
    visibleCount.value = 4
    //  기존 검색 결과 제거
    searchStore.reset()

    //  새 검색
    searchStore.search(newQ)
  },
  { immediate: true }
)

/* 더 보기 버튼 */
const loadMore = async () => {
  visibleCount.value = Math.min(
    visibleCount.value + 4,
    searchStore.tracks.length
  )

  await nextTick()
  
  // 부드럽게 스크롤 내리기 (약 한 화면 정도)
  window.scrollBy({
    top: 500,
    behavior: 'smooth'
  })
}

// 좋아요 토글
const toggleLike = (track) => {
  if (!accountStore.userPk) {
    alert('로그인이 필요합니다.')
    return
  }

  if (isLiked(track)) {
    // ✅ 서버에 좋아요 취소
    favoriteStore.deleteFavorite(track.track_id)
  } else {
    // ✅ 서버에 좋아요 저장
    favoriteStore.saveFavorite(track)
  }
}


</script>

<style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  .search-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 48px 24px 100px;
    min-height: 100vh;
  }

  .search-page h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    font-weight: 400;
    letter-spacing: 3px;
    margin: 48px 0 48px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .search-page h2::before {
    content: '';
    width: 4px;
    height: 32px;
    background: #D4FF00;
    border-radius: 2px;
    box-shadow: 0 0 15px rgba(212, 255, 0, 0.5);
  }

  /* 플렉스 레이아웃 (Grid 대신 Flex 사용) */
  .track-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 32px 24px;
    justify-content: flex-start;
  }

  /* 리스트 트랜지션 애니메이션 */
  .list-enter-active,
  .list-leave-active {
    transition: all 0.5s ease;
  }
  
  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: translateY(30px);
  }

  /* 카드 래퍼 (한 줄에 4개) */
  .track-card-wrapper {
    perspective: 1000px;
    /* 4개 배치: 100% / 4 = 25%. gap 고려하여 calc 사용 */
    width: calc((100% - (24px * 3)) / 4);
  }

  /* 반응형: 화면이 줄어들면 자동 조정 */
  @media (max-width: 1024px) {
    .track-card-wrapper {
      width: calc((100% - (24px * 2)) / 3); /* 3개 */
    }
  }

  @media (max-width: 768px) {
    .track-card-wrapper {
      width: calc((100% - 24px) / 2); /* 2개 */
    }
  }

  @media (max-width: 580px) {
    .track-card-wrapper {
      width: 100%; /* 1개 */
    }
  }

  /* 트랙 카드 (컨테이너) */
  .track-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    padding: 16px;
    border-radius: 20px;
    background: transparent;
    transition: transform 0.3s ease;
  }

  .track-card:hover {
    transform: translateY(-10px);
  }

  /* CD 디스크 효과 */
  .cd-disk {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    position: relative;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    transition: all 0.5s ease;
    background: #000;
    border: 4px solid #1a1a1a;
  }

  /* CD 회전 애니메이션 */
  .track-card:hover .cd-disk {
    animation: spin 4s linear infinite;
    box-shadow: 0 0 40px rgba(212, 255, 0, 0.2);
    border-color: #333;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  /* 앨범 커버 이미지 */
  .album-cover {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }

  /* CD 중앙 구멍 */
  .cd-hole {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 24px;
    height: 24px;
    background: #0a0a0a;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: inset 0 0 4px rgba(0,0,0,0.8);
    border: 2px solid #333;
  }

  /* 트랙 정보 */
  .track-details {
    margin-top: 20px;
    width: 100%;
  }

  .track-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .track-year {
    font-size: 0.8rem;
    color: #666666;
  }

  /* 좋아요 버튼 */
  .like-btn {
    margin-top: 12px;
    padding: 8px 16px;
    border-radius: 20px;
    border: 1px solid #333;
    background: #1a1a1a;
    color: #a0a0a0;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
  }

  .like-btn:hover {
    background: #D4FF00;
    color: #0a0a0a;
    border-color: #D4FF00;
    box-shadow: 0 0 15px rgba(212, 255, 0, 0.3);
  }

  /* 좋아요 활성 상태 */
  .like-btn.active {
    background: #D4FF00;
    color: #0a0a0a;
    border-color: #D4FF00;
    opacity: 1;
    transform: translateY(0);
  }

  .like-btn.active .heart-icon {
    fill: #0a0a0a;
    stroke: #0a0a0a;
  }

  /* 하트 아이콘 */
  .heart-icon {
    width: 16px;
    height: 16px;
    transition: all 0.2s ease;
  }

  .like-btn:hover .heart-icon {
    fill: #0a0a0a;
    stroke: #0a0a0a;
  }

  /* 더보기 버튼 */
  .load-more {
    display: block;
    margin: 60px auto 0;
    padding: 16px 44px;
    border-radius: 40px;
    border: 1px solid #D4FF00;
    background: transparent;
    color: #D4FF00;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .load-more:hover {
    background: #D4FF00;
    color: #0a0a0a;
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(212, 255, 0, 0.3);
  }

  .empty-text {
    margin-top: 80px;
    text-align: center;
    color: #666666;
    font-size: 1rem;
    line-height: 1.8;
  }
</style>