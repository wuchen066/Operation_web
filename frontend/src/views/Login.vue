<template>
  <div class="login-container dark:bg-black">
    <div class="login-card dark:bg-gray-800">
      <h2 class="login-title">服务器监控系统</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            class="form-control"
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="form-control"
            placeholder="请输入密码"
          />
        </div>
        <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>
        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="loading">登录中...</span>
          <span v-else>登录</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    // 获取CSRF令牌
    const getCsrfToken = () => {
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrf_token') {
          return value;
        }
      }
      return '';
    };

    const response = await axios.post('/api/login',
      { username: username.value, password: password.value },
      {
        withCredentials: true,
        headers: {
          'X-CSRFToken': getCsrfToken()
        }
      }
    );

    if (response.data.status === 'success') {
      router.push('/');
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '登录失败，请检查用户名和密码';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 1.25rem;
  color: #333;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 0.875rem;
}

label {
  display: block;
  margin-bottom: 0.375rem;
  color: #666;
}

.form-control {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn-login {
  width: 100%;
  padding: 0.625rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.btn-login:hover:not(:disabled) {
  background-color: #359469;
}

.btn-login:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.alert-error {
  color: #dc3545;
  padding: 0.5rem;
  margin-bottom: 0.875rem;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  font-size: 0.875rem;
}
</style>