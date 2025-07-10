<template>
  <div class="min-h-screen flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-white dark:bg-black shadow-md z-10 sticky top-0">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <button @click="toggleSidebar" class="md:hidden p-2 rounded-md hover:bg-gray-100" v-if="isLoggedIn">
            <i class="fa fa-bars"></i>
          </button>
          <i class="fa fa-server text-primary text-2xl"></i>
          <h1 class="text-xl font-bold text-primary hidden sm:block">{{ displayName }}</h1>
            <h1 class="text-lg font-bold text-primary sm:hidden truncate max-w-[150px]">{{ displayName }}</h1>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <button @click="toggleTheme" class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              <i class="fa" :class="theme === 'light' ? 'fa-sun-o text-yellow-500' : 'fa-moon-o text-blue-300'"></i>
            </button>
          </div>
          <span class="text-gray-700 dark:text-white font-medium flex items-center cursor-pointer" v-if="isLoggedIn" @click="logout" title="点击登出">
            <i class="fa fa-user-circle mr-2"></i>{{ username }}
          </span>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-1 flex overflow-hidden">
      <!-- 侧边栏导航 -->
      <aside v-if="isLoggedIn" :class="['bg-white dark:bg-black shadow-md h-full flex-shrink-0 overflow-y-auto transition-all duration-300', isSidebarOpen ? 'translate-x-0 w-64' : '-translate-x-full w-0 md:translate-x-0 md:w-64']" id="sidebar">
        <nav class="py-4">
          <div class="px-4 mb-4">
            <div class="bg-primary/10 dark:bg-black rounded-lg p-4">
              <div class="text-primary dark:text-white font-medium mb-2">不知道写什么</div>
              <div class="flex items-center justify-between">
                <!-- 服务器信息已注释 -->
              </div>
            </div>
          </div>

          <div class="space-y-1 px-2">
            <router-link to="/" :class="['flex items-center px-4 py-3 rounded-lg transition-colors', $route.path === '/' ? 'text-primary bg-primary/10 dark:bg-gray-800' : 'text-gray-600 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800']">
              <i class="fa fa-tachometer w-5 text-center mr-3"></i>
              <span>仪表盘</span>
            </router-link>
            <router-link to="/system" :class="['flex items-center px-4 py-3 rounded-lg transition-colors', $route.path === '/system' ? 'text-primary bg-primary/10 dark:bg-gray-800' : 'text-gray-600 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800']">
              <i class="fa fa-desktop w-5 text-center mr-3"></i>
              <span>系统监控</span>
            </router-link>
            <router-link to="/commands" :class="['flex items-center px-4 py-3 rounded-lg transition-colors', $route.path === '/commands' ? 'text-primary bg-primary/10 dark:bg-gray-800' : 'text-gray-600 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800']">
              <i class="fa fa-terminal w-5 text-center mr-3"></i>
              <span>命令执行</span>
            </router-link>
            <router-link to="/settings" :class="['flex items-center px-4 py-3 rounded-lg transition-colors', $route.path === '/settings' ? 'text-primary bg-primary/10 dark:bg-gray-800' : 'text-gray-600 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800']">
              <i class="fa fa-cog w-5 text-center mr-3"></i>
              <span>设置</span>
            </router-link>
          </div>

          <!-- 服务器列表已注释 -->
        </nav>
      </aside>

      <!-- 内容区域 -->
      <div class="flex-1 overflow-y-auto bg-gray-50 dark:bg-black p-4" id="content">
        <router-view />
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-white dark:bg-black border-t border-gray-200 dark:border-gray-800 py-4">
      <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
        <div class="text-sm text-gray-500 dark:text-white mb-2 md:mb-0">
          © 2025 服务器运维监控工具 | 版本 1.0.0
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const displayName = ref('服务器运维监控');
const cpuUsage = ref('0');
const memUsage = ref('0');
const isSidebarOpen = ref(true);
const route = useRoute();
const router = useRouter();
const theme = ref('light');
const isLoggedIn = ref(false);
const username = ref('');

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    // 检查localStorage缓存
    const cachedStatus = localStorage.getItem('loginStatus');
    if (cachedStatus) {
      const cachedData = JSON.parse(cachedStatus);
      const { loggedIn, username: cachedUsername, timestamp } = cachedData;
      const now = Date.now();
      // 检查缓存是否有效且包含用户名
      if (now - timestamp < 30 * 60 * 1000 && cachedUsername) {
        isLoggedIn.value = loggedIn;
        username.value = cachedUsername;
        return;
      }
    }
    // 缓存不存在或已过期，调用API
    const response = await axios.get('/api/login', { withCredentials: true });
    isLoggedIn.value = response.data.logged_in;
    username.value = response.data.username || '';
    // 更新缓存
    localStorage.setItem('loginStatus', JSON.stringify({
      loggedIn: isLoggedIn.value,
      username: username.value,
      timestamp: Date.now()
    }));
  } catch (error) {
    isLoggedIn.value = false;
    username.value = '';
    localStorage.removeItem('loginStatus');
  }
};

// 移动端自动关闭侧边栏
watch(route, async () => {
  await checkLoginStatus();
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }
});

// 切换侧边栏显示
function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value;
}

// 模拟系统数据加载
function simulateSystemDataLoading() {
  // 模拟 CPU 和内存数据逻辑保持不变
}

// 主题切换
function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.classList.toggle('dark', theme.value === 'dark');
  localStorage.setItem('theme', theme.value);
}

// 获取Cookie值
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// 用户登出
const logout = async () => {
  try {
    const csrfToken = getCookie('csrf_token');
    await axios.post('/api/logout', {}, {
      headers: {
        'X-CSRFToken': csrfToken
      },
      withCredentials: true
    });
    // 清除本地缓存
    localStorage.removeItem('loginStatus');
    isLoggedIn.value = false;
    username.value = '';
    // 重定向到登录页
    router.push('/login');
  } catch (error) {
    console.error('登出失败:', error);
    alert('登出失败，请重试');
  }
}

onMounted(async () => {
  await checkLoginStatus();
  // 初始化主题
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (savedTheme) {
    theme.value = savedTheme;
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  } else if (prefersDark) {
    theme.value = 'dark';
    document.documentElement.classList.add('dark');
  }

  // 初始化侧边栏状态
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }

  // 获取displayName和设置，添加缓存逻辑
  try {
    // 检查localStorage缓存
    const cachedSettings = localStorage.getItem('settings');
    if (cachedSettings) {
        const { data, timestamp } = JSON.parse(cachedSettings);
        const now = Date.now();
        // 缓存有效期10分钟
        if (now - timestamp < 10 * 60 * 1000) {
          displayName.value = data.display_name || '服务器运维监控';
        } else {
          // 缓存过期，重新请求
          const response = await axios.get('/api/settings');
          displayName.value = response.data.display_name || '服务器运维监控';
          // 更新缓存
          localStorage.setItem('settings', JSON.stringify({
            data: response.data,
            timestamp: Date.now()
          }));
        }
      } else {
        // 无缓存，请求API
        const response = await axios.get('/api/settings');
        displayName.value = response.data.display_name || '服务器运维监控';
        // 存入缓存，带时间戳
        localStorage.setItem('settings', JSON.stringify({
        data: response.data,
        timestamp: Date.now()
      }));
    }
  } catch (error) {
    console.error('Failed to fetch settings from cache:', error);
    // 尝试直接请求API，不依赖缓存
    try {
      const response = await axios.get('/api/settings');
      displayName.value = response.data.display_name || '服务器运维监控';
      localStorage.setItem('settings', JSON.stringify({
        data: response.data,
        timestamp: Date.now()
      }));
    } catch (fetchError) {
      console.error('Failed to fetch settings after cache error:', fetchError);
      displayName.value = '服务器运维监控';
    }
  }

  // 初始化数据
  simulateSystemDataLoading();
  // 定时更新数据
  setInterval(simulateSystemDataLoading, 5000);
});


</script>