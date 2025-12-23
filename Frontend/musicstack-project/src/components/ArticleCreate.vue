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
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px;
}

/* 페이지 제목 */
.page-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 36px;
  color: #222;
}

/* 폼 카드 */
.create-form {
  background: #ffffff;
  padding: 36px 32px 40px;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* 입력 그룹 */
.form-group {
  margin-bottom: 26px;
}

/* 라벨 */
label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #444;
}

/* input, textarea 공통 */
input,
textarea {
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 0.95rem;
  outline: none;
  resize: none;
  transition: border 0.2s ease, box-shadow 0.2s ease;
}

/* textarea 높이 */
textarea {
  min-height: 160px;
}

/* 포커스 효과 */
input:focus,
textarea:focus {
  border-color: #6a11cb;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.15);
}

/* 제출 버튼 */
.submit-btn {
  width: 100%;
  margin-top: 10px;
  padding: 14px 0;
  border-radius: 28px;
  border: none;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* 버튼 hover */
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
}

/* 모바일 대응 */
@media (max-width: 480px) {
  .create-form {
    padding: 28px 20px 32px;
  }

  .page-title {
    font-size: 1.5rem;
  }
}

</style>