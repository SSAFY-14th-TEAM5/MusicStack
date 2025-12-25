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
          <div v-for="(song, index) in recommendations.recommended" :key="index" class="song-card">
            <div class="song-info">
              <span class="rank">{{ index + 1 }}</span>
              <div class="text">
                <p class="title">{{ song.track }}</p>
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
  const userPk = accountStore.userPk // 1 대신 실제 pk 사용

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
/* ================================================
   MUSIC STACK - RECOMMEND VIEW 스타일
   다크 테마 + 형광 노란색 포인트 적용
   ================================================ */

.recommend-container {
  max-width: 800px;
  margin: 60px auto;
  text-align: center;
  padding: 0 20px;
  color: #ffffff;
}

/* 제목 영역 */
h1 {
  font-size: 2.2rem;
  font-weight: 800;
  margin-bottom: 12px;
  color: #ffffff;
}

.subtitle {
  color: #888888;
  font-size: 1rem;
  margin-bottom: 40px;
}

/* 공통 박스 스타일 */
.locked-section, .intro-box, .loading-box {
  padding: 48px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 24px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
}

/* 잠금 상태 */
.lock-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.locked-section h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #ffffff;
}

.locked-section p {
  color: #888888;
  margin-bottom: 24px;
}

/* 프로그레스 바 */
.progress-bar-container {
  width: 100%;
  height: 12px;
  background: #333333;
  border-radius: 6px;
  margin: 0 auto 16px;
  max-width: 400px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #D4FF00; /* 포인트 컬러 */
  border-radius: 6px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(212, 255, 0, 0.5);
}

.count-text {
  font-weight: 700;
  color: #D4FF00;
  margin-bottom: 32px;
}

/* 버튼 스타일 */
.btn-go-tracks, .btn-recommend, .btn-retry {
  display: inline-block;
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 700;
  background: #D4FF00;
  color: #0a0a0a;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.25s ease;
}

.btn-go-tracks:hover, .btn-recommend:hover, .btn-retry:hover {
  background: #E6FF33;
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(212, 255, 0, 0.3);
}

/* 추천 시작 문구 */
.intro-box p {
  font-size: 1.1rem;
  color: #cccccc;
  margin-bottom: 32px;
  line-height: 1.6;
}

/* 로딩 상태 */
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #333333;
  border-top: 4px solid #D4FF00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

.loading-box p {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
}

.loading-box .small {
  font-size: 0.9rem;
  font-weight: 400;
  color: #888888;
}

/* 결과 리스트 */
.results-box h3 {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 32px;
  color: #D4FF00;
}

.song-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 40px;
}

.song-card {
  background: #1e1e1e;
  border: 1px solid #2a2a2a;
  padding: 24px;
  border-radius: 18px;
  text-align: left;
  transition: all 0.2s ease;
}

.song-card:hover {
  border-color: rgba(212, 255, 0, 0.3);
  transform: translateX(4px);
}

.song-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.rank {
  font-size: 1.2rem;
  font-weight: 800;
  color: #D4FF00;
  background: rgba(212, 255, 0, 0.1);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 4px 0;
}

.artist {
  font-size: 0.95rem;
  color: #888888;
  margin: 0;
}

.reason {
  font-size: 0.95rem;
  color: #cccccc;
  line-height: 1.5;
  background: #141414;
  padding: 16px;
  border-radius: 12px;
  margin: 0;
}

.btn-retry {
  background: transparent;
  border: 1px solid #D4FF00;
  color: #D4FF00;
}

.btn-retry:hover {
  background: #D4FF00;
  color: #0a0a0a;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 모바일 대응 */
@media (max-width: 600px) {
  .intro-box, .loading-box, .locked-section {
    padding: 32px 20px;
  }
  
  h1 { font-size: 1.8rem; }
  
  .song-info {
    flex-direction: row;
    align-items: center;
  }
}
</style>