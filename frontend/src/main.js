import { createApp } from 'vue';
import 'font-awesome/css/font-awesome.min.css';
import { createPinia } from 'pinia'
import './style.css'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import System from './views/System.vue'
import Commands from './views/Commands.vue'
import Settings from './views/Settings.vue'

// 配置路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: Dashboard },
    { path: '/system', name: 'System', component: System },
    { path: '/commands', name: 'Commands', component: Commands },
    { path: '/settings', name: 'Settings', component: Settings }
  ]
})

// 创建并挂载应用实例
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.mount('#app')