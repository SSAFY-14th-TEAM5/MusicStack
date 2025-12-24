<template>
  <div v-if="user" class="container my-5">

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


    <!-- 🔹 Profile Card -->
    <div class="card profile-header p-4 mb-4">
      <div class="d-flex align-items-center">
        <div class="profile-avatar me-3">
          {{ user.nickname?.charAt(0) }}
        </div>
        <div>
          <h4 class="mb-0 fw-bold">닉네임: {{ user.nickname }}</h4>
          <small>@{{ user.username }}</small><hr>
          <button class="mdb-btn">팔로우</button>
        </div>
      </div>
    </div>

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
  grid-template-columns: 1fr 1.4fr;
  gap: 24px;
  margin-bottom: 36px;
  align-items: stretch;
}

/* 왼쪽 카드 */
.profile-music-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 22px;
  border-radius: 20px;
  background: linear-gradient(135deg, #f7f7ff, #eef2ff);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.12);
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
  width: 90px;
  flex-shrink: 0;
}

/* 정보 영역 */
.profile-music-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* 라벨 */
.profile-music-info .label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #6a11cb;
  margin-bottom: 2px;
}

/* 제목 */
.profile-music-info .title {
  font-size: 1.05rem;
  font-weight: 800;
  color: #222;
  line-height: 1.2;
}

/* 아티스트 */
.profile-music-info .artist {
  font-size: 0.85rem;
  color: #666;
}
</style>
