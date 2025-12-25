<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">Login</h2>

      <form @submit.prevent="logIn">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model.trim="username"
            placeholder="Enter username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model.trim="password"
            placeholder="Enter password"
          />
        </div>

        <button type="submit" class="login-btn">
          LogIn
        </button>
        <!-- 에러 메시지 -->
        <Transition name="error-fade">
          <div v-if="errorMessage" class="error-box">
            {{ errorMessage }}
          </div>
        </Transition>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts'

  const accountStore = useAccountStore()

  const username = ref(null)
  const password = ref(null)
  const errorMessage = ref(null)  // 로그인 오류 출력 메세지

  const logIn = async () => {
    errorMessage.value = ''

    try {
      await accountStore.logIn({
        username: username.value,
        password: password.value,
      })
    } catch (err) {
      errorMessage.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
    }
  }

</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background: #0a0a0a;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 배경 그라디언트 효과 */
.login-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at center, rgba(212, 255, 0, 0.05) 0%, transparent 50%);
  animation: rotate-bg 20s linear infinite;
}

@keyframes rotate-bg {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.login-card {
  width: 400px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  padding: 40px 36px;
  border-radius: 24px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

.login-title {
  text-align: center;
  font-family: 'Bebas Neue', sans-serif;
  font-weight: 400;
  font-size: 2rem;
  letter-spacing: 4px;
  margin-bottom: 32px;
  color: #D4FF00;
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 8px;
  color: #a0a0a0;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid #2a2a2a;
  background: #141414;
  color: #ffffff;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.25s ease;
}

.form-group input::placeholder {
  color: #555555;
}

.form-group input:focus {
  border-color: #D4FF00;
  box-shadow: 0 0 0 3px rgba(212, 255, 0, 0.15);
}

.login-btn {
  width: 100%;
  margin-top: 16px;
  padding: 14px;
  border: none;
  border-radius: 30px;
  background: #D4FF00;
  color: #0a0a0a;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.25s ease;
}

.login-btn:hover {
  background: #E6FF33;
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(212, 255, 0, 0.3);
}

/* 에러 메시지 */
.error-box {
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid rgba(255, 71, 87, 0.3);
  border-radius: 10px;
  color: #ff4757;
  font-size: 0.85rem;
  text-align: center;
}

/* 에러 메시지 fade */
.error-fade-enter-active,
.error-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.error-fade-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.error-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

</style>
