<template>
  <div class="loading-wrapper">
    <div class="pulse-circle"></div>

    <p class="loading-text">
      Analyzing your music taste<span class="dots">...</span>
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
  padding: 100px 20px;
  color: #a0a0a0;
}

/* 원형 펄스 */
.pulse-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #D4FF00;
  animation: pulse 1.8s ease-in-out infinite;
  margin-bottom: 28px;
  box-shadow: 0 0 40px rgba(212, 255, 0, 0.4);
}

@keyframes pulse {
  0% {
    transform: scale(0.9);
    opacity: 0.6;
    box-shadow: 0 0 30px rgba(212, 255, 0, 0.3);
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
    box-shadow: 0 0 60px rgba(212, 255, 0, 0.6);
  }
  100% {
    transform: scale(0.9);
    opacity: 0.6;
    box-shadow: 0 0 30px rgba(212, 255, 0, 0.3);
  }
}

/* 텍스트 */
.loading-text {
  font-size: 1rem;
  letter-spacing: 1px;
  color: #888888;
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
