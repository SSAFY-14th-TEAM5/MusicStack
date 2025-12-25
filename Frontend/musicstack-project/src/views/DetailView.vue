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
  max-width: 860px;
  margin: 0 auto;
  padding: 48px 24px 100px;
  min-height: 100vh;
}

.detail-card {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
}

/* 제목 */
.detail-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 14px;
  color: #ffffff;
}

/* 날짜 */
.detail-meta {
  font-size: 0.8rem;
  color: #666666;
  margin-bottom: 28px;
}

/* 본문 */
.detail-content {
  font-size: 1rem;
  line-height: 1.8;
  color: #a0a0a0;
  white-space: pre-line;
}

/* 수정 영역 */
.edit-box {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.edit-input,
.edit-textarea {
  width: 100%;
  padding: 14px 18px;
  border-radius: 12px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.25s ease;
}

.edit-input:focus,
.edit-textarea:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

.edit-textarea {
  min-height: 160px;
  resize: vertical;
}

.edit-actions {
  display: flex;
  gap: 14px;
  margin-top: 12px;
}

/* 버튼 */
.primary-btn {
  padding: 12px 26px;
  border-radius: 24px;
  border: none;
  background: #D4FF00;
  color: #0a0a0a;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.primary-btn:hover {
  background: #E6FF33;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(212, 255, 0, 0.3);
}

.ghost-btn {
  padding: 12px 22px;
  border-radius: 24px;
  border: 1px solid #2a2a2a;
  background: transparent;
  color: #a0a0a0;
  cursor: pointer;
  transition: all 0.25s ease;
}

.ghost-btn:hover {
  border-color: #D4FF00;
  color: #D4FF00;
}

.danger-btn {
  padding: 12px 22px;
  border-radius: 24px;
  border: none;
  background: rgba(255, 71, 87, 0.15);
  color: #ff4757;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.danger-btn:hover {
  background: #ff4757;
  color: #ffffff;
}

/* 작성자 버튼 */
.author-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 28px;
}

/* 댓글 */
.comment-section {
  margin-top: 48px;
  padding-top: 28px;
  border-top: 1px solid #2a2a2a;
}
</style>
