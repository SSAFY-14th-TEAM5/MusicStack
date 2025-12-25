<template>
  <div class="detail-page">
    <div v-if="article" class="detail-card">
      <h2 class="detail-title">{{ article.title }}</h2>

      <div class="detail-meta">
        <span>작성일 {{ formatDate(article.created_at) }}</span>
        <span v-if="article.updated_at">
          · 수정 {{ formatDate(article.updated_at) }}
        </span>
      </div>

      <!-- 수정 모드 -->
      <div v-if="isEdit" class="edit-box">
        <input v-model="editTitle" class="edit-input" />
        <textarea v-model="editContent" class="edit-textarea"></textarea>

        <div class="edit-actions">
          <button class="primary-btn" @click="submitEdit">저장</button>
          <button class="ghost-btn" @click="cancelEdit">취소</button>
        </div>
      </div>

      <!-- 일반 보기 -->
      <p v-else class="detail-content">
        {{ article.content }}
      </p>

      <!-- 작성자 액션 -->
      <div v-if="isAuthor && !isEdit" class="author-actions">
        <button class="ghost-btn" @click="startEdit">수정</button>
        <button class="danger-btn" @click="deleteThisArticle">삭제</button>
      </div>

      <!-- 댓글 영역 -->
      <div class="comment-section">
        <CommentCreate :articleId="articleId" @created="loadComments" />
        <CommentList
          :comments="comments"
          :articleId="articleId"
          @updated="loadComments"
        />
      </div>
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

// 날짜 포맷 함수 추가
const formatDate = (isoString) => {
  if (!isoString) return ''

  const date = new Date(isoString)

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

</script>

<style scoped>
.detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.detail-card {
  background: white;
  border-radius: 18px;
  padding: 32px;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.1);
}

/* 제목 */
.detail-title {
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 12px;
}

/* 날짜 */
.detail-meta {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 24px;
}

/* 본문 */
.detail-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #333;
  white-space: pre-line;
}

/* 수정 영역 */
.edit-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-input,
.edit-textarea {
  width: 100%;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 0.95rem;
}

.edit-textarea {
  min-height: 140px;
  resize: vertical;
}

.edit-actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

/* 버튼 */
.primary-btn {
  padding: 10px 20px;
  border-radius: 20px;
  border: none;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.ghost-btn {
  padding: 10px 18px;
  border-radius: 20px;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
}

.danger-btn {
  padding: 10px 18px;
  border-radius: 20px;
  border: none;
  background: #ff4d4f;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

/* 작성자 버튼 */
.author-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}

/* 댓글 */
.comment-section {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}
</style>
