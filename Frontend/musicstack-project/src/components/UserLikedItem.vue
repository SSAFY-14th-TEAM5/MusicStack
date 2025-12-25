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

    <!-- ✅ 유튜브 영상 -->
    <YoutubeTrackCard
      v-if="track.video_id"
      :track="track"
      title="🎬 뮤직 비디오"
    />
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
import YoutubeTrackCard from '@/components/YoutubeTrackCard.vue'

const route = useRoute()
const track = ref(null)

const favoriteStore = useFavoriteStore()
const accountStore = useAccountStore()



onMounted(() => {
  // 좋아요 목록에서 track_id 기준으로 찾기
  track.value = favoriteStore.favorites.find(
    t => t.track_id === route.params.trackId
  )
})

const setAsProfileMusic = () => {
  // accountStore.setProfileMusic(track.value)
  accountStore.setProfileMusic({
    track_id: track.value.track_id,
    track_name: track.value.track_name,
    artist: track.value.artist,
    track_image_link: track.value.track_image_link,
    video_id: track.value.video_id, // ⭐ 중요
  })
  alert('프로필 뮤직으로 설정되었습니다 🎶')
}
</script>

<style scoped>
.track-detail {
  max-width: 460px;
  margin: 60px auto;
  padding: 36px 32px 40px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
}

/* 앨범 이미지 */
.cover {
  margin-bottom: 24px;
  border-radius: 16px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);
}

/* 제목 */
h2 {
  font-size: 1.4rem;
  font-weight: 800;
  margin: 16px 0 8px;
  color: #ffffff;
}

/* 아티스트 */
.artist {
  font-size: 0.95rem;
  color: #888888;
  margin-bottom: 28px;
}

/* 프로필 뮤직 버튼 */
.profile-btn {
  margin-bottom: 36px;
  width: 100%;
  padding: 16px 0;
  border-radius: 30px;
  border: none;
  background: #D4FF00;
  color: #0a0a0a;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
}

.profile-btn:hover {
  background: #E6FF33;
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(212, 255, 0, 0.3);
}

/* 로딩 상태 */
.loading {
  margin-top: 100px;
  text-align: center;
  color: #666666;
  font-size: 0.95rem;
}
</style>
