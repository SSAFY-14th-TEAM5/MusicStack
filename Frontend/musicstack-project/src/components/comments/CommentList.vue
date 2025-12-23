<template>
  <div>
    <h3>댓글</h3>
    <CommentItem
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      :articleId="articleId"
      @updated="$emit('updated')"
    />
  </div>
</template>

<script setup>
import CommentItem from './CommentItem.vue'

defineProps({
  comments: Array,
  articleId: Number,
})
</script>


<style scoped>

</style>