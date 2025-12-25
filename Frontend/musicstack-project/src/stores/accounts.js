import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {

  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const user = ref(null)  // 유저 정보 조회시 사용
  const userPk = computed(() => {
    return user.value?.id ?? user.value?.pk ?? null
  })

  const router = useRouter()
  const profileMusic = ref(null)

  // 회원 가입
  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const nickname = payload.nickname
    // const fav_genres = payload.fav_genres
    
    // const { username, password1, password2, nickname } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, 
        nickname,
        // fav_genres,
      }
    })
      .then(res => {
        // console.log('회원 가입이 완료되었습니다.')
        // console.log(res.data)
        const password = password1
        logIn({ username, password })
      })
      .catch(err => console.log(err))
  }

  // 유저 로그인
  const logIn = function (payload) {
  //   const username = payload.username
  //   const password = payload.password
    const { username, password } = payload
    return axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        // console.log('로그인이 완료되었습니다.')
        // console.log(res.data)
        token.value = res.data.key
        router.push({ name: 'Home' })
        return getUserInfo()
      })
      .catch(err => {
        console.log(err)
        throw err // LogInView에 err 전달
      })
  }


  const isLogin = computed(() => {
    return token.value ? true : false
  })

  // 유저 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
      Authorization: `Token ${token.value}`, // 토큰 정보도 같이 넘김
      },
    })
      .then(res => {
        token.value = null
        user.value = null
        profileMusic.value = null 
        router.push({ name: 'LogInView' })
      })
      .catch(err => console.log(err))
  }

  // 유저 정보 조회
  const getUserInfo = function () {
  return axios({
    method: 'get',
    url: `${API_URL}/accounts/user/`,
    headers: { Authorization: `Token ${token.value}` },
  })
  .then(res => {
    user.value = res.data
    return user.value
  })
}

  // 프로필 뮤직 상태 추가

  const setProfileMusic = (track) => {
    profileMusic.value = {
      track_id: track.track_id,
      track_name: track.track_name,
      artist: track.artist,
      image: track.track_image_link,
      video_id: track.video_id,
    }
  }



  return {
    signUp,
    logIn,
    token,
    user,
    userPk,
    isLogin,
    logOut,
    getUserInfo,
    profileMusic,
    setProfileMusic,
  }
}, { persist: true })