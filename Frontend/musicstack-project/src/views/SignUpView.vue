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
  background-color: #f5f6fa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.signup-card {
  width: 420px;
  background: white;
  padding: 36px;
  border-radius: 18px;
  box-shadow: 0 14px 34px rgba(0,0,0,0.12);
}

.signup-title {
  text-align: center;
  font-weight: 700;
  margin-bottom: 28px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 6px;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 11px 14px;
  border-radius: 10px;
  border: 1px solid #ddd;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus {
  border-color: #2575fc;
  box-shadow: 0 0 0 2px rgba(37,117,252,0.15);
}

/* 장르 섹션 */
.genre-section {
  margin: 22px 0;
}

.genre-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.genre-chip {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.genre-chip:hover {
  background-color: #f0f0f0;
}

/* 선택된 장르 */
.genre-chip.active {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  border: none;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* 회원가입 버튼 */
.signup-btn {
  width: 100%;
  margin-top: 20px;
  padding: 14px;
  border: none;
  border-radius: 26px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.signup-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}
</style>
