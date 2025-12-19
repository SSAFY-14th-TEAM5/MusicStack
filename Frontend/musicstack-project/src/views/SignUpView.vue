<template>
  <div>
    <h1>SignUp Page</h1>
    <form @submit.prevent="signUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username">
      <br>
      <label for="password1">password: </label>
      <input type="password" id="password1" v-model.trim="password1">
      <br>
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2">
      <br>
      <label for="nickname">nickname: </label>
      <input type="text" id="nickname" v-model.trim="nickname">
      <br>
      
      <div class="genre-selection">
        <p>좋아하는 장르를 선택해주세요 (다중 선택 가능)</p>
        <div class="genre-list">
          <button
            v-for="genre in allGenres" 
            :key="genre.id"
            :class="{ active: selectedGenres.includes(genre.id) }"
            @click="toggleGenre(genre.id)"
            type="button"
          >
            {{ genre.name }}
          </button>
        </div>
      </div>

      <input type="submit" value="signup">
    </form>
  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts'
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  const allGenres = ref([])

  onMounted(() => {
    getGenres()
  })

  const getGenres = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/tracks/genres/'
    }).then((res) => {
      allGenres.value = res.data
    }).catch((err) => {
      console.log('장르 목록 로드 실패', err)
    })
  }

  const accountStore = useAccountStore()

  const username = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  const nickname = ref(null)
  const selectedGenres = ref([])

  const toggleGenre = (genreId) => {
  if (selectedGenres.value.includes(genreId)) {
    // 이미 선택되어 있으면 제거
    selectedGenres.value = selectedGenres.value.filter(id => id !== genreId)
  } else {
    // 선택 안 되어 있으면 추가
    selectedGenres.value.push(genreId)
  }
}

  const signUp = function () {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      nickname: nickname.value,
      fav_genres: selectedGenres.value,
    }
    accountStore.signUp(payload)
    
  }

</script>

<style scoped>
  .genre-list {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
  }

  /* 기본 버튼 스타일 */
  button {
    padding: 10px 20px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 20px; /* 둥근 버튼 */
    cursor: pointer;
    transition: all 0.2s ease; /* 부드러운 변화 */
    color: #555;
  }

  /* 마우스를 올렸을 때 */
  button:hover {
    background-color: #f0f0f0;
  }

  /* ✅ 선택되었을 때 (Active 상태) */
  button.active {
    background-color: #42b983; /* 포인트 컬러 (초록색 계열) */
    color: white;
    border-color: #42b983;
    font-weight: bold;
    transform: scale(1.05); /* 약간 커지는 효과 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
</style>