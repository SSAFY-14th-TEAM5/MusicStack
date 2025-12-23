<template>
  <div>
    <textarea v-model="content" placeholder="댓글을 입력하세요" />
    <button @click="submitComment">댓글 작성</button>
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

</style>