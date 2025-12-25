<template>
  <div class="comment-card">
    <!-- 수정 모드 -->
    <div v-if="isEdit" class="edit-box">
      <input
        v-model="editContent"
        class="edit-input"
      />
      <div class="edit-actions">
        <button class="save-btn" @click="saveEdit">저장</button>
        <button class="cancel-btn" @click="cancelEdit">취소</button>
      </div>
    </div>

    <!-- 일반 보기 -->
    <div v-else>
      <p class="comment-content">{{ comment.content }}</p>
      <span class="comment-author">
        {{ comment.author.nickname }}
      </span>
      <small class="comment-date">{{ formatDate(comment.created_at) }}</small>

      <div v-if="isAuthor" class="comment-actions">
        <button class="edit-btn" @click="startEdit">수정</button>
        <button class="delete-btn" @click="removeComment">삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCommentStore } from '@/stores/comments'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps({
  comment: Object,
  articleId: Number,
})
const emit = defineEmits(['updated'])

const store = useCommentStore()
const accountStore = useAccountStore()

const isEdit = ref(false)
const editContent = ref(props.comment.content)

/* 작성자 여부 */
const isAuthor = computed(() => {
  return props.comment.author.id === accountStore.userPk
})

const startEdit = () => {
  isEdit.value = true
}

const cancelEdit = () => {
  isEdit.value = false
}

const saveEdit = () => {
  store.updateComment(props.articleId, props.comment.id, editContent.value)
    .then(() => {
      isEdit.value = false
      emit('updated')
    })
    .catch(err => console.log(err))
}

const removeComment = () => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return

  store.deleteComment(props.articleId, props.comment.id)
    .then(() => emit('updated'))
    .catch(err => console.log(err))
}

// 날짜 포맷 함수
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
/* 댓글 카드 */
.comment-card {
  background: #1e1e1e;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  transition: all 0.25s ease;
}

.comment-card:hover {
  transform: translateY(-2px);
  border-color: rgba(212, 255, 0, 0.2);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
}

/* 댓글 내용 */
.comment-content {
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 8px;
  color: #e0e0e0;
}

/* 날짜 */
.comment-date {
  font-size: 0.75rem;
  color: #555555;
}

/* 수정/삭제 버튼 */
.comment-actions {
  margin-top: 10px;
  display: flex;
  gap: 12px;
}

.edit-btn,
.delete-btn {
  border: none;
  background: none;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.2s ease;
}

.edit-btn {
  color: #D4FF00;
}

.edit-btn:hover {
  color: #E6FF33;
}

.delete-btn {
  color: #888888;
}

.delete-btn:hover {
  color: #ff4757;
}

/* 수정 모드 */
.edit-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-input {
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.25s ease;
}

.edit-input:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

/* 수정 버튼 영역 */
.edit-actions {
  display: flex;
  gap: 12px;
}

.save-btn {
  background: #D4FF00;
  color: #0a0a0a;
  border: none;
  border-radius: 18px;
  padding: 8px 18px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.save-btn:hover {
  background: #E6FF33;
}

.cancel-btn {
  background: #252525;
  color: #a0a0a0;
  border: none;
  border-radius: 18px;
  padding: 8px 18px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.25s ease;
}

.cancel-btn:hover {
  background: #2a2a2a;
  color: #ffffff;
}
</style>