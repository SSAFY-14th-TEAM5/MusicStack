<template>
  <div class="comment-list">
    <h3 class="comment-title">💬 댓글</h3>

    <CommentItem
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      :articleId="articleId"
      @updated="$emit('updated')"
    />

    <p v-if="comments.length === 0" class="empty-comment">
      아직 댓글이 없습니다.
    </p>
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
/* 전체 댓글 영역 */
.comment-list {
  margin-top: 48px;
  padding-top: 28px;
  border-top: 1px solid #e6e6e6;
}

/* 제목 */
.comment-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #222;
}

/* 댓글 없음 */
.empty-comment {
  text-align: center;
  color: #999;
  font-size: 0.9rem;
  margin-top: 20px;
}
</style>