<template>
  <div>
    <h1>Detail</h1>
    <div v-if="article">
      <p>글 번호: {{ article.id }}</p>
      <!-- 수정 모드 -->
      <div v-if="isEdit">
        <input v-model="editTitle" />
        <textarea v-model="editContent"></textarea>

        <button @click="submitEdit">저장</button>
        <button @click="cancelEdit">취소</button>
      </div>

      <!-- 일반 보기 모드 -->
      <p>제목: {{ article.title }}</p>
      <p>내용: {{ article.content }}</p>
      <p>작성시간: {{ article.created_at }}</p>
      <p>수정시간: {{ article.updated_at }}</p>
      
      <div v-if="isAuthor" class="author-actions">
        <button @click="goEdit">수정</button>
        <button @click="removeArticle">삭제</button>
      </div>

      <!-- DetailView.vue 하단 -->
      <CommentCreate :articleId="articleId" @created="loadComments" />
      <CommentList
        :comments="comments"
        :articleId="articleId"
        @updated="loadComments"
      />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import CommentList from '@/components/comments/CommentList.vue'
import CommentCreate from '@/components/comments/CommentCreate.vue'
import { useCommentStore } from '@/stores/comments'

const store = useArticleStore()
const route = useRoute()
const article = ref(null)
const articleId = Number(route.params.id)
const router = useRouter()
const accountStore = useAccountStore()

// 로그인 (작성자 계정) 관련  
const isEdit = ref(false)
const editTitle = ref('')
const editContent = ref('')

// 댓글 관련
const commentStore = useCommentStore()
const comments = ref([])

/* 🔹 작성자 여부 */
const isAuthor = computed(() => {
  if (!article.value) return false
  return article.value.author === accountStore.userPk
})

// 게시글 상세 조회
onMounted(() => {
  store.getArticleDetail(articleId)
    .then(res => {
      article.value = res.data
    })
    .catch(err => {
      console.log(err)
    })
})

/* 수정 시작 */
const startEdit = () => {
  isEdit.value = true
  editTitle.value = article.value.title
  editContent.value = article.value.content
}

/* 수정 취소 */
const cancelEdit = () => {
  isEdit.value = false
}

/* 수정 저장 */
const submitEdit = () => {
  store.updateArticle(articleId, {
    title: editTitle.value,
    content: editContent.value,
  })
    .then(res => {
      article.value = res.data
      isEdit.value = false
    })
    .catch(err => console.log(err))
}

/* 게시글 삭제 */
const deleteThisArticle = () => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  store.deleteArticle(articleId)
    .then(() => {
      alert('삭제되었습니다.')
      router.push({ name: 'ArticleView' })
    })
    .catch(err => console.log(err))
}

// 댓글 연결
const loadComments = () => {
  commentStore.getComments(articleId)
    .then(res => {
      comments.value = res.data.results
    })
    .catch(err => console.log(err))
}

onMounted(() => {
  loadComments()
})
</script>

<style>

</style>
