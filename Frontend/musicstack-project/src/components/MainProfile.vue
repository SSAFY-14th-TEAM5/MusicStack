<template>
  <div v-if="user" class="container my-5">

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

    <!-- 🔹 Liked Section -->
    <div class="card section-card p-4">
      <h5 class="fw-bold mb-3">❤️ 좋아요</h5>
      <UserLiked />
    </div>

  </div>

  <div v-else class="text-center mt-5">
    <p>유저 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
  import UserRecommend from '@/components/UserRecommend.vue'
  import UserLiked from '@/components/UserLiked.vue'
  import { RouterView } from 'vue-router'
  // Pinia state를 반응성 유지한 채로 구조 분해위해 사용
  import { storeToRefs } from 'pinia'
  import { useAccountStore } from '@/stores/accounts'
  import { onMounted } from 'vue'

  const accountStore = useAccountStore()
  const { user } = storeToRefs(accountStore)

  // 새로고침 대응
  onMounted(() => {
  if (!user.value) {
    accountStore.getUserInfo()
    }
  })

</script>

<style scoped>
  
</style>