import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import System from '../views/System.vue';
import Commands from '../views/Commands.vue';
import Settings from '../views/Settings.vue';
import axios from 'axios';

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/system', name: 'System', component: System, meta: { requiresAuth: true } },
  { path: '/commands', name: 'Commands', component: Commands, meta: { requiresAuth: true } },
  { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫：检查登录状态
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      // 检查localStorage缓存
      const cachedStatus = localStorage.getItem('loginStatus');
      if (cachedStatus) {
        const { loggedIn, timestamp } = JSON.parse(cachedStatus);
        const now = Date.now();
        // 检查缓存是否在30分钟内
        if (now - timestamp < 30 * 60 * 1000 && loggedIn) {
          next();
          return;
        }
      }
      // 缓存不存在或已过期，调用API
      const response = await axios.get('/api/login', { withCredentials: true });
      if (response.data.logged_in) {
        // 更新缓存
        localStorage.setItem('loginStatus', JSON.stringify({
          loggedIn: true,
          timestamp: Date.now()
        }));
        next();
      } else {
        localStorage.removeItem('loginStatus');
        next('/login');
      }
    } catch (error) {
      localStorage.removeItem('loginStatus');
      next('/login');
    }
  } else {
    next();
  }
});

export default router;