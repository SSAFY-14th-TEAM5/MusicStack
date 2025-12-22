<template>
  <div class="loading-wrapper">
    <div class="pulse-circle"></div>

    <p class="loading-text">
      LLM이 음악을 분석하고 있어요<span class="dots">...</span>
    </p>
  </div>
</template>

<script setup>
</script>

<style scoped>
.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #555;
}

/* 원형 펄스 */
.pulse-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  animation: pulse 1.6s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.15);
    opacity: 1;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.7;
  }
}

/* 텍스트 */
.loading-text {
  font-size: 0.95rem;
  letter-spacing: 1px;
}

/* 점점점 애니메이션 */
.dots::after {
  content: '';
  animation: dots 1.5s steps(3, end) infinite;
}

@keyframes dots {
  0%   { content: ''; }
  33%  { content: '.'; }
  66%  { content: '..'; }
  100% { content: '...'; }
}
</style>
