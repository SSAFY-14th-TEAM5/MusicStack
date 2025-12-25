import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

export const useFavoriteStore = defineStore('favorite', () => {
  const API_URL = 'http://127.0.0.1:8000/api/v1/tracks'

  const favorites = ref([])
  const loading = ref(false)
  const errorMessage = ref(null)
  const router = useRouter()

  // ✅ 좋아요 목록 조회
  const fetchFavorites = async (userPk) => {
    if (!userPk) return
    loading.value = true
    errorMessage.value = null

    try {
      const res = await axios.get(`${API_URL}/${userPk}/fav/`)
      // 페이지네이션 응답이면 results로
      favorites.value = res.data.results ?? res.data
    } catch (err) {
      console.error(err)
      errorMessage.value = '좋아요 목록을 불러오지 못했습니다.'
    } finally {
      loading.value = false
    }
  }

  // ✅ 좋아요 저장
  const saveFavorite = async (track) => {
    const accountStore = useAccountStore()
    if (!accountStore.token) {
      alert('로그인이 필요합니다.')
      return
    }

    //  검색 결과(track)를 백엔드 TrackSerializer가 받는 형태로 변환
    const payloadTrack = {
      track_name: track.track_name,                 // 검색결과 name → track_name
      track_id: track.track_id,                     // 검색결과 id → track_id
      track_image_link: track.album_image,    // album_image → track_image_link
      release_date_text: track.release_date,  // release_date → release_date_text
      release_year: track.release_year,                   
      artist_id: track.artist_id ? [...track.artist_id] : [],        // views.py에서 artist_name을 따로 읽고 있으니 보내주기 
      //  artist_id 제거 (중요)
      // artist_id: [],
    }

    // console.log(payloadTrack)

    try {
      await axios.post(
        `${API_URL}/fav/create/`,
        { track: payloadTrack },
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        }
      )

      // ✅ 저장 후 내 좋아요 목록 즉시 갱신
      await fetchFavorites(accountStore.userPk)
    } catch (err) {
      console.error(err)
      alert('좋아요 저장에 실패했습니다. (콘솔 확인)')
    }
  }

  // 노래 상세 페이지로 이동
  const goDetail = (track) => {
    router.push({
      name: 'UserLikedItem',
      params: { trackId: track.track_id }, // ✅ track_id 사용
    })
  }

  // 1. State: 숫자만 저장
  const likedTracksCount = ref(0)

  // 2. Action: 백엔드에서 숫자만 받아오기
  const fetchLikedCount = async (userPk) => {
    const accountStore = useAccountStore()
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/v1/tracks/fav/count/`,
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        }
      )
      // 백엔드에서 {'count': 15} 형태로 준다고 가정
      likedTracksCount.value = response.data.count
    } catch (error) {
      console.error('좋아요 개수를 가져오지 못했습니다:', error)
    }
  }

  // 3. 만약 사용자가 '좋아요' 버튼을 누를 때마다 숫자를 실시간으로 바꾸고 싶다면?
  const incrementCount = () => {
    likedTracksCount.value++
  }
  const decrementCount = () => {
    if (likedTracksCount.value > 0) likedTracksCount.value--
  }

  // 좋아요 삭제
  const deleteFavorite = async (trackId) => {
    const accountStore = useAccountStore()
    if (!accountStore.token) return

    try {
      await axios.delete(
        `${API_URL}/fav/delete/`,
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
          data: {
            track_id: trackId,
          },
        }
      )

      // 서버 성공 후 로컬 상태 반영
      favorites.value = favorites.value.filter(
        fav => fav.track_id !== trackId
      )

      decrementCount()
    } catch (err) {
      console.error(err)
      alert('좋아요 취소 실패')
    }
  }


  return {
    favorites,
    loading,
    errorMessage,
    fetchFavorites,
    saveFavorite,
    goDetail,
    likedTracksCount, 
    fetchLikedCount,
    incrementCount,
    decrementCount,
    deleteFavorite,
  }
}, { persist: true })
