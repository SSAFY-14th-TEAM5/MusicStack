<template>
  <div class="create-page">
    <h1 class="page-title">게시글 생성</h1>

    <form class="create-form" @submit.prevent="submitData">
      <div class="form-group">
        <label for="title">제목</label>
        <input
          type="text"
          id="title"
          v-model="title"
          placeholder="제목을 입력해주세요"
        />
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model="content"
          placeholder="내용을 입력해주세요"
        ></textarea>
      </div>

      <button type="submit" class="submit-btn">
        게시글 작성
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useArticleStore } from '@/stores/articles.js'

const store = useArticleStore()

const title = ref('')
const content = ref('')

const submitData = function () {
  const article = {
    title: title.value,
    content: content.value
  }
  store.createArticle(article)
  title.value = ''
  content.value = ''
}

</script>

<style scoped>
/* 전체 페이지 */
.create-page {
  max-width: 760px;
  margin: 0 auto;
  padding: 60px 24px 100px;
  min-height: 100vh;
}

/* 페이지 제목 */
.page-title {
  text-align: center;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2rem;
  font-weight: 400;
  letter-spacing: 4px;
  margin-bottom: 40px;
  color: #D4FF00;
}

/* 폼 카드 */
.create-form {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  padding: 44px 40px 48px;
  border-radius: 24px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
}

/* 입력 그룹 */
.form-group {
  margin-bottom: 28px;
}

/* 라벨 */
label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #a0a0a0;
}

/* input, textarea 공통 */
input,
textarea {
  width: 100%;
  padding: 16px 20px;
  border-radius: 14px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.95rem;
  outline: none;
  resize: none;
  transition: all 0.25s ease;
}

input::placeholder,
textarea::placeholder {
  color: #555555;
}

/* textarea 높이 */
textarea {
  min-height: 180px;
}

/* 포커스 효과 */
input:focus,
textarea:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

/* 제출 버튼 */
.submit-btn {
  width: 100%;
  margin-top: 16px;
  padding: 16px 0;
  border-radius: 32px;
  border: none;
  background: #D4FF00;
  color: #0a0a0a;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

/* 버튼 hover */
.submit-btn:hover {
  background: #E6FF33;
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(212, 255, 0, 0.3);
}

/* 모바일 대응 */
@media (max-width: 480px) {
  .create-form {
    padding: 32px 24px 36px;
  }

  .page-title {
    font-size: 1.6rem;
  }
}

</style>