import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useArticleStore = defineStore('article', () => {
  const API_URL = 'http://127.0.0.1:8000/api/v1'
  const accountStore = useAccountStore()
  const router = useRouter()
  
  const articles = ref([])
  // 페이지네이션 코드
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const currentPage = ref(1)
  const pageSize = 5

  // 페이지 계산
  const totalPages = computed(() =>
    Math.ceil(count.value / pageSize)
  )

  // 게시글 조회
  const getArticles = function (page = 1) {
    axios({
      method: 'get',
      url: `${API_URL}/articles/?page=${page}`,
    })
    .then(res => {
      // console.log(res.data)
      articles.value = res.data.results
      count.value = res.data.count
      next.value = res.data.next
      previous.value = res.data.previous
      currentPage.value = page
    })
    .catch(err => {
      console.log(err)
    })
  }

  // 게시글 생성
  const createArticle = function ({ title, content }) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/`,
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${accountStore.token}`
      },
    })
    .then(res => {
      // console.log(res)
      router.push({ name: 'ArticleView' })
    })
  }

  // 게시글 상세 조회
  const getArticleDetail = function (articleId) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/`,
    })
    // .then(res => {
    //   console.log(res.data)
    //   return res.data })
    // .catch(err => {
    //   console.log(err)
    // })
  }

  /* 🔹 게시글 수정 */
  const updateArticle = function (articleId, payload) {
    return axios({
      method: 'patch',
      url: `${API_URL}/articles/${articleId}/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  /* 🔹 게시글 삭제 */
  const deleteArticle = function (articleId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }


  return {
    articles,
    count,
    next,
    previous,
    currentPage,
    router,
    totalPages,
    getArticles,
    createArticle,
    getArticleDetail,
    updateArticle,
    deleteArticle,
  }
}, { persist: true })
