<template>
  <div class="liked-page">
    <h2>❤️ 내가 좋아요한 노래</h2>

    <p v-if="favoriteStore.loading">불러오는 중...</p>

    <p v-if="!favoriteStore.loading && favoriteStore.favorites.length === 0">
      아직 좋아요한 곡이 없습니다.
    </p>

    <div class="liked-grid">
      <div
        v-for="track in favoriteStore.favorites"
        :key="track.track_name"
        class="liked-card"
      >
        <img :src="track.track_image_link" />
        <p class="title">{{ track.track_name }}</p>
        <p class="artist">
          {{ track.artist.map(a => a.name).join(', ') }}
        </p>
        <p class="year">{{ track.release_year }}</p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, watch } from 'vue'
import { useFavoriteStore } from '@/stores/favorite'
import { useAccountStore } from '@/stores/accounts'

const favoriteStore = useFavoriteStore()
const accountStore = useAccountStore()

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
</script>


<style scoped>

</style>