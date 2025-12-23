import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000/api/v1'
  const accountStore = useAccountStore()

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/articles/`,
    })
    .then(res => {
      console.log(res.data)
      articles.value = res.data.results})
    .catch(err => {
      console.log(err)
    })
  }

  const createArticle = function ({ title, content }) {
    axios({
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
    .then(res => console.log(res))
  }

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

  return {
    articles,
    getArticles,
    createArticle,
    getArticleDetail,
  }
}, { persist: true })
