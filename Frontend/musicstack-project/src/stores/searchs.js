import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {

  const API_URL = 'http://127.0.0.1:8000/api/v1'

  // ===== state =====
  const keyword = ref('')
  const artist = ref(null)     // 가수 정보
  const tracks = ref([])       // 노래 리스트
  const isLoading = ref(false)
  const error = ref(null)

  // ===== actions =====
  const search = async (query) => {
    if (!query.trim()) return

    keyword.value = query
    isLoading.value = true
    error.value = null

    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/tracks/search/`,
        data: {
          user_input: query,   // 검색어 (LLM으로 전달)
        }
      })

      /**
       * 🔽 백엔드 응답 예시
       * {
       *   artist: { id, name, image, genre },
       *   tracks: [{ id, title, album, cover }]
       * }
       */

      artist.value = res.data.artist
      tracks.value = res.data.tracks

    } catch (err) {
      console.error('검색 실패', err)
      error.value = '검색에 실패했습니다.'
    } finally {
      isLoading.value = false
    }
  }

  // ===== reset (선택) =====
  const reset = () => {
    keyword.value = ''
    artist.value = null
    tracks.value = []
    error.value = null
  }

  return {
    keyword,
    artist,
    tracks,
    isLoading,
    error,
    search,
    reset,
  }
}, { persist: true })