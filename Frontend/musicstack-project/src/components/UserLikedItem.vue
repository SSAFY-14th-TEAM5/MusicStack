<template>
  <div v-if="track" class="track-detail">
    <img
      :src="track.track_image_link"
      class="img-cover img-hover cover"
    />

    <h2>{{ track.track_name }}</h2>
    <p class="artist">
      {{ track.artist.map(a => a.name).join(', ') }}
    </p>

    <button
      class="profile-btn"
      @click="setAsProfileMusic"
    >
      🎵 프로필 뮤직으로 설정
    </button>
  </div>

  <div v-else class="loading">
    노래 정보를 불러오는 중입니다...
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useFavoriteStore } from '@/stores/favorite'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const track = ref(null)

const favoriteStore = useFavoriteStore()
const accountStore = useAccountStore()
const trackId = route.params.trackId


onMounted(() => {
  // 좋아요 목록에서 track_id 기준으로 찾기
  track.value = favoriteStore.favorites.find(
    t => t.track_id === route.params.trackId
  )
})

const setAsProfileMusic = () => {
  accountStore.setProfileMusic(track.value)
  alert('프로필 뮤직으로 설정되었습니다 🎶')
}
</script>

<style scoped>
.track-detail {
  max-width: 420px;
  margin: 60px auto;
  padding: 28px 24px 32px;
  background: #fff;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

/* 앨범 이미지 */
.cover {
  margin-bottom: 18px;
}

/* 제목 */
h2 {
  font-size: 1.3rem;
  font-weight: 800;
  margin: 12px 0 6px;
  color: #222;
}

/* 아티스트 */
.artist {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 22px;
}

/* 프로필 뮤직 버튼 */
.profile-btn {
  width: 100%;
  padding: 14px 0;
  border-radius: 26px;
  border: none;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
}

.profile-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
}

/* 로딩 상태 */
.loading {
  margin-top: 80px;
  text-align: center;
  color: #777;
  font-size: 0.95rem;
}
</style>
