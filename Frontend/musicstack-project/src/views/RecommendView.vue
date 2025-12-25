<template>
  <div class="recommend-container">
    <div v-if="favoriteStore.likedTracksCount < 10" class="locked-section">
      <div class="lock-icon">🔒</div>
      <h2>AI 추천 기능이 잠겨 있습니다</h2>
      <p>
        회원님의 음악 취향을 분석하기 위해서는 최소 <strong>10개</strong>의 좋아요가 필요합니다.
      </p>
      <div class="progress-bar-container">
        <div 
          class="progress-bar" 
          :style="{ width: (favoriteStore.likedTracksCount * 10) + '%' }"
        ></div>
      </div>
      <p class="count-text">현재 좋아요: {{ favoriteStore.likedTracksCount }} / 10</p>
      <router-link :to="{ name: 'Home' }" class="btn-go-tracks">노래 구경하러 가기</router-link>
    </div>

    <div v-else class="active-section">
      <h1>AI 맞춤 음악 추천</h1>
      <p class="subtitle">회원님이 좋아하신 {{ favoriteStore.likedTracksCount }}곡을 분석하여 최적의 음악을 찾아드립니다.</p>

      <div v-if="!recommendations && !isLoading" class="intro-box">
        <p>"최신 트렌드와 회원님의 고유한 취향을 결합한 결과를 확인해보세요."</p>
        <button @click="getRecommendation" class="btn-recommend">추천 시작하기</button>
      </div>

      <div v-if="isLoading" class="loading-box">
        <div class="spinner"></div>
        <p>AI가 회원님의 취향 리스트 30곡을 분석하고 있습니다...</p>
        <p class="small">잠시만 기다려주세요 (약 5~10초 소요)</p>
      </div>

      <div v-if="recommendations && !isLoading" class="results-box">
        <h3>✨ AI 추천 결과</h3>
        <div class="song-list">
          <div v-for="(song, index) in recommendations" :key="index" class="song-card">
            <div class="song-info">
              <span class="rank">{{ index + 1 }}</span>
              <div class="text">
                <p class="title">{{ song.title }}</p>
                <p class="artist">{{ song.artist }}</p>
              </div>
            </div>
            <p class="reason">{{ song.reason }}</p>
          </div>
        </div>
        <button @click="recommendations = null" class="btn-retry">다시 추천받기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useFavoriteStore } from '@/stores/favorite'
import { useAccountStore } from '@/stores/accounts'

// 스토어 연결
const favoriteStore = useFavoriteStore()
const accountStore = useAccountStore()

onMounted(() => {
  // 앱이 켜질 때 로그인이 되어 있다면 미리 개수를 채워둠
  if (accountStore.isLogin) {
    favoriteStore.fetchLikedCount(accountStore.userId)
  }
})

// 로컬 상태 관리
const isLoading = ref(false)
const recommendations = ref(null)

const getRecommendation = async () => {
  isLoading.value = true
  // 실제 유저 PK를 스토어나 인증 정보에서 가져오세요
  const userPk = 1 

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/v1/tracks/recommend/${userPk}/`)
    
    // 백엔드에서 JSON 문자열로 넘어올 경우 파싱 (이미 객체면 생략 가능)
    const rawData = response.data
    const parsedData = typeof rawData === 'string' ? JSON.parse(rawData) : rawData
    
    // AI 응답의 'recommendations' 배열을 저장
    recommendations.value = parsedData

    console.log(recommendations.value)
  } catch (error) {
    console.error("추천 로직 에러:", error)
    alert("AI 서버와 통신 중 문제가 발생했습니다.")
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 디자인은 프로젝트 스타일에 맞게 수정하세요 */
.recommend-container {
  max-width: 800px;
  margin: 50px auto;
  text-align: center;
}

.locked-section, .loading-box {
  padding: 40px;
  background: #f8f9fa;
  border-radius: 15px;
}

.progress-bar-container {
  width: 100%;
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  margin: 20px 0;
}

.progress-bar {
  height: 100%;
  background: #007bff;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.song-card {
  background: white;
  border: 1px solid #eee;
  padding: 20px;
  margin-bottom: 15px;
  border-radius: 10px;
  text-align: left;
}

.title { font-weight: bold; font-size: 1.1em; margin: 0; }
.artist { color: #666; margin: 5px 0; }
.reason { font-size: 0.9em; color: #888; border-top: 1px solid #f0f0f0; padding-top: 10px; margin-top: 10px; }

.btn-recommend {
  padding: 15px 40px;
  font-size: 1.2em;
  background: #000;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>