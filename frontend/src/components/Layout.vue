<template>
  <div class="min-h-screen flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-white dark:bg-black shadow-md z-10 sticky top-0">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <button @click="toggleSidebar" class="md:hidden p-2 rounded-md hover:bg-gray-100">
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
          <span class="text-gray-700 dark:text-white font-medium flex items-center">
            <i class="fa fa-user-circle mr-2"></i>admin
          </span>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-1 flex overflow-hidden">
      <!-- 侧边栏导航 -->
      <aside :class="['bg-white dark:bg-black shadow-md h-full flex-shrink-0 overflow-y-auto transition-all duration-300', isSidebarOpen ? 'translate-x-0 w-64' : '-translate-x-full w-0 md:translate-x-0 md:w-64']" id="sidebar">
        <nav class="py-4">
          <div class="px-4 mb-4">
            <div class="bg-primary/10 dark:bg-black rounded-lg p-4">
              <div class="text-primary dark:text-white font-medium mb-2">不知道写什么</div>
              <div class="flex items-center justify-between">
                <!-- <div class="flex flex-col">
                  <span class="text-xs text-gray-500">IP地址：</span>
                  <span class="text-lg font-semibold">{{ ipAddress }}</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-xs text-gray-500">内存使用率</span>
                  <span class="text-lg font-semibold">{{ memUsage }}%</span>
                </div> -->
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
          <!-- <div class="mt-8 px-4">
            <div class="text-xs font-medium text-gray-400 uppercase mb-2">服务器</div>
            <div class="space-y-1">
              <a href="#" class="flex items-center px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors">
                <span class="inline-block w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                <span>localhost</span>
              </a>
              <a href="#" class="flex items-center px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors">
                <span class="inline-block w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                <span>web-server-01</span>
              </a>
              <a href="#" class="flex items-center px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors">
                <span class="inline-block w-2 h-2 rounded-full bg-gray-300 mr-2"></span>
                <span>db-server-01</span>
              </a>
            </div>
          </div> -->
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
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const displayName = ref('服务器管理系统');
const cpuUsage = ref('0');
const memUsage = ref('0');
const isSidebarOpen = ref(true);
const route = useRoute();

// 移动端自动关闭侧边栏
watch(route, () => {
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
  // // 模拟 CPU 数据
  // const cpu = Math.floor(Math.random() * 30) + 10;
  // cpuUsage.value = cpu;

  // // 模拟内存数据
  // const mem = Math.floor(Math.random() * 40) + 30;
  // memUsage.value = mem;
}

// 主题切换

const theme = ref('light');

function toggleTheme() {
  // 切换主题模式
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  
  // 更新DOM类名
  if (theme.value === 'dark') { document.documentElement.classList.add('dark'); } else { document.documentElement.classList.remove('dark'); }
  
  // 保存到本地存储
  localStorage.setItem('theme', theme.value);
}

// 初始化主题
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    theme.value = savedTheme;
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  } else if (prefersDark) {
    theme.value = 'dark';
    document.documentElement.classList.add('dark');
  }
})

onMounted(() => {
  // 初始化侧边栏状态
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
      isSidebarOpen.value = true;
    } else {
      isSidebarOpen.value = false;
    }
  });
  
  // 初始化数据
  simulateSystemDataLoading();
  // 定时更新数据
  setInterval(simulateSystemDataLoading, 5000);
});
</script>