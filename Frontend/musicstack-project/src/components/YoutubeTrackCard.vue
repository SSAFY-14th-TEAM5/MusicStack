<template>
  <div class="fav-track-container">
    <!-- 트랙 있음 -->
    <div v-if="track" class="track-card">
      <h3 class="section-title">
        {{ title }}
      </h3>

      <!-- 유튜브 영상 -->
      <div v-if="track.video_id" class="video-wrapper">
        <iframe
          :src="youtubeUrl"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>

      <!-- 곡 정보 -->
      <div class="track-info">
        <p class="title-text">{{ track.track_name }}</p>
        <p class="artist-text">
          {{ artistText }}
        </p>
      </div>
    </div>

    <!-- 트랙 없음 -->
    <div v-else class="no-data">
      {{ emptyMessage }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

/* ===== props ===== */
const props = defineProps({
  track: {
    type: Object,
    default: null,
  },
  title: {
    type: String,
    default: '최근 좋아요한 곡',
  },
  emptyMessage: {
    type: String,
    default: '좋아요한 트랙이 없습니다.',
  },
})

/* ===== computed ===== */
const youtubeUrl = computed(() => {
  if (!props.track?.video_id) return ''
  return `https://www.youtube.com/embed/${props.track.video_id}`
})

const artistText = computed(() => {
  // artist 배열 형태 (현재 프로젝트 기준)
  if (Array.isArray(props.track?.artist)) {
    return props.track.artist.map(a => a.name).join(', ')
  }

  // 문자열 형태도 대응
  return props.track?.artist_name || ''
})
</script>

<style scoped>
.fav-track-container {
  margin-bottom: 32px;
}

/* 카드 */
.track-card {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
}

/* 제목 */
.section-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 12px;
}

/* 유튜브 */
.video-wrapper {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 12px;
}

.video-wrapper iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* 정보 */
.track-info {
  margin-top: 12px;
}

.title-text {
  font-weight: 800;
  font-size: 1.05rem;
}

.artist-text {
  font-size: 0.85rem;
  color: #666;
}

/* 빈 상태 */
.no-data {
  text-align: center;
  color: #777;
  padding: 20px 0;
}
</style>
