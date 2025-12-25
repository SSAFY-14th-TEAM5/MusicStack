<template>
  <div class="comment-create">
    <textarea
      v-model="content"
      placeholder="댓글을 입력하세요"
      class="comment-input"
    />
    <div class="btn-wrapper">
      <button @click="submitComment" class="submit-btn">
        댓글 작성
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCommentStore } from '@/stores/comments'

const props = defineProps({
  articleId: Number,
})
const emit = defineEmits(['created'])

const content = ref('')
const store = useCommentStore()

const submitComment = () => {
  if (!content.value.trim()) return

  store.createComment(props.articleId, content.value)
    .then(() => {
      content.value = ''
      emit('created')
    })
    .catch(err => console.log(err))
}
</script>


<style scoped>
/* 전체 래퍼 */
.comment-create {
  margin-top: 36px;
  padding: 24px;
  border-radius: 18px;
  background: #1e1e1e;
  border: 1px solid #2a2a2a;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* textarea */
.comment-input {
  width: 100%;
  min-height: 100px;
  padding: 16px 18px;
  border-radius: 14px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.95rem;
  resize: vertical;
  outline: none;
  transition: all 0.25s ease;
}

.comment-input::placeholder {
  color: #555555;
}

.comment-input:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

/* 버튼 영역 */
.btn-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

/* 제출 버튼 */
.submit-btn {
  padding: 12px 26px;
  border-radius: 24px;
  border: none;
  background: #D4FF00;
  color: #0a0a0a;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.submit-btn:hover {
  background: #E6FF33;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(212, 255, 0, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}
</style>