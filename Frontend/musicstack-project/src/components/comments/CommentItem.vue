<template>
  <div>
    <div v-if="isEdit">
      <input v-model="editContent" />
      <button @click="saveEdit">저장</button>
      <button @click="cancelEdit">취소</button>
    </div>

    <div v-else>
      <p>{{ comment.content }}</p>
      <small>{{ comment.created_at }}</small>

      <div v-if="isAuthor">
        <button @click="startEdit">수정</button>
        <button @click="removeComment">삭제</button>
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
  return props.comment.author === accountStore.userPk
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
</script>


<style scoped>

</style>