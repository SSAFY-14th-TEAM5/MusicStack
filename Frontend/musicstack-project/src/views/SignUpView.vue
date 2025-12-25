<template>
  <div class="signup-wrapper">
    <div class="signup-card">
      <h2 class="signup-title">Sign Up</h2>

      <form @submit.prevent="signUp">

        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model.trim="username" />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model.trim="password1" />
        </div>

        <div class="form-group">
          <label>Password Confirmation</label>
          <input type="password" v-model.trim="password2" />
        </div>

        <div class="form-group">
          <label>Nickname</label>
          <input type="text" v-model.trim="nickname" />
        </div>

        <!-- 장르 선택 -->
        <!-- <div class="genre-section">
          <p class="genre-title">🎧 좋아하는 장르 (다중 선택)</p>
          <div class="genre-list">
            <button
              v-for="genre in allGenres"
              :key="genre.id"
              type="button"
              class="genre-chip"
              :class="{ active: selectedGenres.includes(genre.id) }"
              @click="toggleGenre(genre.id)"
            >
              {{ genre.name }}
            </button>
          </div>
        </div> -->

        <button class="signup-btn" type="submit">
          Create Account
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts'
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  // const allGenres = ref([])

  // onMounted(() => {
  //   getGenres()
  // })

  // const getGenres = function() {
  //   axios({
  //     method: 'get',
  //     url: 'http://127.0.0.1:8000/api/v1/tracks/genres/'
  //   }).then((res) => {
  //     allGenres.value = res.data
  //   }).catch((err) => {
  //     console.log('장르 목록 로드 실패', err)
  //   })
  // }

  const accountStore = useAccountStore()

  const username = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  const nickname = ref(null)
  // const selectedGenres = ref([])

//   const toggleGenre = (genreId) => {
//   if (selectedGenres.value.includes(genreId)) {
//     // 이미 선택되어 있으면 제거
//     selectedGenres.value = selectedGenres.value.filter(id => id !== genreId)
//   } else {
//     // 선택 안 되어 있으면 추가
//     selectedGenres.value.push(genreId)
//   }
// }

  const signUp = function () {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      nickname: nickname.value,
      // fav_genres: selectedGenres.value,
    }
    accountStore.signUp(payload)
    
  }

</script>

<style scoped>
.signup-wrapper {
  min-height: 100vh;
  background: #0a0a0a;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
}

/* 배경 그라디언트 효과 */
.signup-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at center, rgba(212, 255, 0, 0.05) 0%, transparent 50%);
  animation: rotate-bg 25s linear infinite reverse;
}

@keyframes rotate-bg {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.signup-card {
  width: 440px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  padding: 44px 40px;
  border-radius: 24px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

.signup-title {
  text-align: center;
  font-family: 'Bebas Neue', sans-serif;
  font-weight: 400;
  font-size: 2rem;
  letter-spacing: 4px;
  margin-bottom: 36px;
  color: #D4FF00;
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 8px;
  color: #a0a0a0;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.25s ease;
}

.form-group input::placeholder {
  color: #555555;
}

.form-group input:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

/* 장르 섹션 */
.genre-section {
  margin: 28px 0;
}

.genre-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 14px;
  color: #ffffff;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.genre-chip {
  padding: 10px 18px;
  border-radius: 24px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #a0a0a0;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.25s ease;
}

.genre-chip:hover {
  border-color: #D4FF00;
  color: #D4FF00;
}

/* 선택된 장르 */
.genre-chip.active {
  background: #D4FF00;
  color: #0a0a0a;
  border-color: #D4FF00;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(212, 255, 0, 0.3);
}

/* 회원가입 버튼 */
.signup-btn {
  width: 100%;
  margin-top: 28px;
  padding: 16px;
  border: none;
  border-radius: 30px;
  background: #D4FF00;
  color: #0a0a0a;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.25s ease;
}

.signup-btn:hover {
  background: #E6FF33;
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(212, 255, 0, 0.3);
}
</style>
