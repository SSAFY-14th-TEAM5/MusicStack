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
  margin-top: 32px;
  padding: 20px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* textarea */
.comment-input {
  width: 100%;
  min-height: 90px;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 0.95rem;
  resize: vertical;
  outline: none;
  transition: border 0.2s ease, box-shadow 0.2s ease;
}

.comment-input::placeholder {
  color: #aaa;
}

.comment-input:focus {
  border-color: #2575fc;
  box-shadow: 0 0 0 3px rgba(37, 117, 252, 0.15);
}

/* 버튼 영역 */
.btn-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
}

/* 제출 버튼 */
.submit-btn {
  padding: 10px 22px;
  border-radius: 20px;
  border: none;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
}

.submit-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
</style>