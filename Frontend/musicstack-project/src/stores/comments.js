import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useCommentStore = defineStore('comment', () => {
  const API_URL = 'http://127.0.0.1:8000/api/v1'
  const accountStore = useAccountStore()

  /* 🔹 댓글 목록 조회 */
  const getComments = function (articleId) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/comments/`,
    })
  }

  /* 🔹 댓글 생성 */
  const createComment = function (articleId, content) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/${articleId}/comments/`,
      data: { content },
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  /* 🔹 댓글 수정 */
  const updateComment = function (articleId, commentId, content) {
    return axios({
      method: 'put',
      url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
      data: { content },
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  /* 🔹 댓글 삭제 */
  const deleteComment = function (articleId, commentId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  return {
    getComments,
    createComment,
    updateComment,
    deleteComment,
  }
})
