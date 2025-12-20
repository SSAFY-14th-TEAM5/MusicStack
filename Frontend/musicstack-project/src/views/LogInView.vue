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
  background-color: #f5f6fa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 360px;
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}

.login-title {
  text-align: center;
  font-weight: 700;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 6px;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus {
  border-color: #2575fc;
  box-shadow: 0 0 0 2px rgba(37,117,252,0.15);
}

.login-btn {
  width: 100%;
  margin-top: 10px;
  padding: 12px;
  border: none;
  border-radius: 24px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

/* 에러 메시지 fade */
.error-fade-enter-active,
.error-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.error-fade-enter-from {
  opacity: 0;
  transform: translateY(-6px);
}

.error-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

</style>
