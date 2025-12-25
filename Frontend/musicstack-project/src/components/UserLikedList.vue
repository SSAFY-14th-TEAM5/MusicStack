<template>
  <div class="liked-page">

    <p v-if="favoriteStore.loading" class="loading">
      불러오는 중...
    </p>

    <p
      v-if="!favoriteStore.loading && favoriteStore.favorites.length === 0"
      class="empty"
    >
      아직 좋아요한 곡이 없습니다.
    </p>

    <div class="liked-grid">
      <div
        v-for="track in favoriteStore.favorites"
        :key="track.track_id"
        class="liked-card"
        @click="goDetail(track.track_id)"
      >
        <img
          :src="track.track_image_link"
          alt="album cover"
          class="album-img"
        />
        <p class="title">{{ track.track_name }}</p>
        <p class="artist">
          {{ track.artist.map(a => a.name).join(', ') }}
        </p>
        <p class="year">{{ track.release_year }}</p>
      </div>
    </div>

    <!-- <YoutubeTrackCard
      :track="latestFavTrack"
      title="최근 좋아요한 곡"
    /> -->


  </div>
</template>


<script setup>
import { onMounted, watch } from 'vue'
import { useFavoriteStore } from '@/stores/favorite'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'
import YoutubeTrackCard from './YoutubeTrackCard.vue'

const favoriteStore = useFavoriteStore()
const accountStore = useAccountStore()
const router = useRouter()

// const latestFavTrack = ref(null)

// // axios로 받아온 response.data 그대로 넣으면 됨
// latestFavTrack.value = response.data


onMounted(() => {
  // 1️⃣ 이미 userPk가 있으면 바로 호출
  if (accountStore.userPk) {
    favoriteStore.fetchFavorites(accountStore.userPk)
    return
  }

  // 2️⃣ 새로고침 직후 persist 복원 타이밍 대비
  const stop = watch(
    () => accountStore.userPk,
    (pk) => {
      if (!pk) return
      favoriteStore.fetchFavorites(pk)
      stop() // 🔥 한 번 실행 후 watch 종료
    }
  )
})

const goDetail = (trackId) => {
  // console.log('클릭된 trackId:', trackId)
  // console.log(track)
  router.push({
    name: 'UserLikedItem',
    params: { trackId }
  })
}
</script>


<style scoped>
/* 전체 영역 */
.liked-page {
  margin-top: 16px;
}

/* 로딩 / 빈 상태 */
.loading,
.empty {
  text-align: center;
  color: #666666;
  margin: 28px 0;
  font-size: 0.95rem;
}

/* Grid */
.liked-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 22px;
}

/* 카드 */
.liked-card {
  background: #1e1e1e;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  padding: 14px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  transition: all 0.25s ease;
  cursor: pointer;
}

.liked-card:hover {
  transform: translateY(-6px);
  border-color: rgba(212, 255, 0, 0.3);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.4), 0 0 20px rgba(212, 255, 0, 0.05);
}

/* 앨범 이미지 */
.album-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 12px;
  transition: transform 0.25s ease;
}

.liked-card:hover .album-img {
  transform: scale(1.03);
}

/* 제목 */
.title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #ffffff;
  margin: 8px 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 아티스트 */
.artist {
  font-size: 0.8rem;
  color: #888888;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 연도 */
.year {
  font-size: 0.75rem;
  color: #555555;
}
</style>
