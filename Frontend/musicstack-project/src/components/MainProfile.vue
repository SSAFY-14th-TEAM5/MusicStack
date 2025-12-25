<template>
  <div v-if="user" class="container my-5">
    <!-- 🔹 Profile Card -->
    <div class="card profile-header p-4 mb-4">
      <div class="d-flex align-items-center">
        <div class="profile-avatar me-3">
          {{ user.nickname?.charAt(0) }}
        </div>
        <div>
          <h4 class="mb-0 fw-bold">{{ user.nickname }}</h4>
          <small>@{{ user.username }}</small><hr>
        </div>
      </div>
    </div>
    <!-- ✅ 프로필 뮤직 + 유튜브 가로 배치 -->
    <div
      v-if="profileMusic"
      class="profile-music-row"
    >
      <!-- 왼쪽: 프로필 뮤직 -->
      <div class="profile-music-card">
        <img
          :src="profileMusic.image"
          class="img-cover profile-music-cover"
        />

        <div class="profile-music-info">
          <p class="label">🎵 프로필 뮤직</p>
          <p class="title">{{ profileMusic.track_name }}</p>
          <p class="artist">
            {{ profileMusic.artist.map(a => a.name).join(', ') }}
          </p>
        </div>
      </div>

      <!-- 오른쪽: 유튜브 카드 -->
      <YoutubeTrackCard
        :track="profileMusic"
        title="🎬 뮤직 비디오"
        class="youtube-side"
      />
    </div>

    <!-- <pre style="background:#eee; padding:10px;">
    {{ profileMusic }}
    </pre> -->

    <!-- 🔹 Recommend Section -->
    <div class="card section-card p-4 mb-4">
      <h5 class="fw-bold mb-3">🎧 추천 음악</h5>
      <UserRecommend />
    </div>

    <!-- 🔹 UserLikedList Section -->
    <div class="card section-card p-4">
      <h5 class="fw-bold mb-3">❤️ 내가 좋아요한 노래</h5>
      <UserLikedList />
    </div>

  </div>

  <div v-else class="text-center mt-5">
    <p>유저 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
  import UserRecommend from '@/components/UserRecommend.vue'
  // import UserLiked from '@/components/UserLiked.vue'
  import UserLikedList from '@/components/UserLikedList.vue'
  import { RouterView } from 'vue-router'
  // Pinia state를 반응성 유지한 채로 구조 분해위해 사용
  import { storeToRefs } from 'pinia'
  import { useAccountStore } from '@/stores/accounts'
  import { onMounted } from 'vue'
  import YoutubeTrackCard from '@/components/YoutubeTrackCard.vue'
  

  const accountStore = useAccountStore()
  const { user } = storeToRefs(accountStore)
  const { profileMusic } = storeToRefs(accountStore)

  // 새로고침 대응
  onMounted(() => {
  if (!user.value) {
    accountStore.getUserInfo()
    }
  })

</script>

<style scoped>
/* ===== 프로필 뮤직 가로 배치 ===== */
.profile-music-row {
  display: grid;
  gap: 28px;
  margin-bottom: 40px;
  align-items: stretch;
}

/* 왼쪽 카드 */
.profile-music-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 22px 26px;
  border-radius: 22px;
  background: linear-gradient(135deg, #1e1e1e, #141414);
  border: 1px solid #2a2a2a;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
  transition: all 0.25s ease;
}

.profile-music-card:hover {
  border-color: rgba(212, 255, 0, 0.3);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5), 0 0 30px rgba(212, 255, 0, 0.05);
}

/* 오른쪽 유튜브 영역 */
.youtube-side {
  align-self: stretch;
}

/* 모바일 대응 */
@media (max-width: 900px) {
  .profile-music-row {
    grid-template-columns: 1fr;
  }
}

/* 이미지 */
.profile-music-cover {
  width: 100px;
  flex-shrink: 0;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

/* 정보 영역 */
.profile-music-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* 라벨 */
.profile-music-info .label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #D4FF00;
  margin-bottom: 2px;
  letter-spacing: 0.5px;
}

/* 제목 */
.profile-music-info .title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.3;
}

/* 아티스트 */
.profile-music-info .artist {
  font-size: 0.85rem;
  color: #888888;
}
</style>
