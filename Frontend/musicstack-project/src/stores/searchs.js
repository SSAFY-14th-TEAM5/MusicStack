import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const API_URL = 'http://127.0.0.1:8000/api/v1'

  const loading = ref(false)
  const success = ref(false)
  const artist = ref(null)
  const tracks = ref([])
  const errorMessage = ref(null)
  const cache = ref({}) // (검색 결과 캐시)

  const normalize = (str) =>
    str.trim().toLowerCase()

  const search = async (keyword) => {
    const normalized = normalize(keyword)

    // 캐시에 있으면 API 호출 X
    if (cache.value[normalized]) {
      console.log('캐시 사용 → API 호출 스킵')

      const cached = cache.value[normalized]
      success.value = cached.success
      artist.value = cached.artist
      tracks.value = cached.tracks
      return
    }

    loading.value = true
    errorMessage.value = null

    try {
      const res = await axios.post(`${API_URL}/tracks/search/`, {
        user_input: keyword, //  핵심
      })

      success.value = res.data.success
      artist.value = res.data.artist
      tracks.value = res.data.tracks

      // 2. 결과 캐시에 저장
      cache.value[normalized] = {
        success: success.value,
        artist: artist.value,
        tracks: tracks.value,
      }
    } catch (err) {
      errorMessage.value = '검색에 실패했습니다.'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    success,
    artist,
    tracks,
    errorMessage,
    cache,
    search,
  }
}, { persist: true })