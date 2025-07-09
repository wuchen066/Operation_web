import { createApp } from 'vue';
import 'font-awesome/css/font-awesome.min.css';
import { createPinia } from 'pinia'
import './style.css'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

// 创建并挂载应用实例
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.mount('#app')