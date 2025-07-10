import { createApp } from 'vue';
import 'font-awesome/css/font-awesome.min.css';
import './style.css'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from 'axios'

// 配置Axios默认设置
axios.defaults.withCredentials = true

// 添加请求拦截器
axios.interceptors.request.use(config => {
  // 从cookie中安全获取CSRF令牌
  const cookie = document.cookie.split(';').find(c => c && c.trim().startsWith('csrf_token='));
  if (cookie) {
    const csrfToken = cookie.split('=')[1];
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

// 创建并挂载应用实例
const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')