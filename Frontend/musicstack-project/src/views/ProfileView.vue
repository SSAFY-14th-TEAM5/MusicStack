<template>
  <div>
    <h1>Profile Page</h1>
    <MainProfile />
    <UserLikedList />
    <UserRecommendList />
  </div>
</template>

<script setup>
  import MainProfile from '@/components/MainProfile.vue'
  import UserLikedList from '@/components/UserLikedList.vue'
  import UserRecommendList from '@/components/UserRecommendList.vue'
  import { onMounted } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useFavoriteStore } from '@/stores/favorite'

  const accountStore = useAccountStore()
  const favoriteStore = useFavoriteStore()

  onMounted(() => {
    if (accountStore.userPk) {
      favoriteStore.fetchFavorites(accountStore.userPk)
    }
  })


</script>

<style scoped>

</style>