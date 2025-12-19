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
  import { RouterView } from 'vue-router'


</script>

<style scoped>

</style>