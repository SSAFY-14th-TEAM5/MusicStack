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
  background: #fff;
  border-radius: 14px;
  padding: 14px 16px;
  margin-bottom: 14px;
  box-shadow: 0 6px 14px rgba(0,0,0,0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.comment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(0,0,0,0.12);
}

/* 댓글 내용 */
.comment-content {
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 6px;
  color: #222;
}

/* 날짜 */
.comment-date {
  font-size: 0.75rem;
  color: #999;
}

/* 수정/삭제 버튼 */
.comment-actions {
  margin-top: 8px;
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  border: none;
  background: none;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 4px 6px;
}

.edit-btn {
  color: #2575fc;
}

.delete-btn {
  color: #e74c3c;
}

/* 수정 모드 */
.edit-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.edit-input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 0.9rem;
}

.edit-input:focus {
  outline: none;
  border-color: #2575fc;
}

/* 수정 버튼 영역 */
.edit-actions {
  display: flex;
  gap: 10px;
}

.save-btn {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  border: none;
  border-radius: 16px;
  padding: 6px 14px;
  font-size: 0.8rem;
  cursor: pointer;
}

.cancel-btn {
  background: #eee;
  border: none;
  border-radius: 16px;
  padding: 6px 14px;
  font-size: 0.8rem;
  cursor: pointer;
}
</style>