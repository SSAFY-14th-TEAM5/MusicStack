import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000/api/v1'

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/articles/`,
    })
    .then(res => articles.value = res.data)
  }

  const createArticle = function ({ title, content }) {
    axios({
      method: 'post',
      url: `${API_URL}/articles/`,
      data: {
        title,
        content
      }
    })
    .then(res => console.log(res))
  }

  return { articles, getArticles, createArticle }
}, { persist: true })
