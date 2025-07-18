<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-gray-800">系统仪表盘</h2>
      <div class="flex space-x-2">
        <div class="relative">
          <button class="bg-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-gray-50 transition-colors">
            <i class="fa fa-calendar text-gray-500"></i>
            <span class="text-sm">今日</span>
            <i class="fa fa-angle-down text-gray-500"></i>
          </button>
        </div>
        <button @click="refreshData" class="bg-primary text-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-primary/90 transition-colors">
          <i class="fa fa-refresh"></i>
          <span class="text-sm">刷新</span>
        </button>
      </div>
    </div>

    <!-- 状态卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- CPU 卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 dark:text-black text-sm font-medium">CPU 使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold dark:text-black">{{ cpuUsage }}%</span>
              <span class="text-gray-500 text-sm mb-1">%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
            <i class="fa fa-microchip"></i>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-primary h-2.5 rounded-full" :style="{ width: cpuUsage + '%' }"></div>
        </div>
        <div class="flex justify-between mt-2">
          <span class="text-xs text-gray-500 dark:text-black">核心数: {{ cpuCores }}</span>
          <span class="text-xs text-gray-500 dark:text-black">频率: {{ cpuFrequency }} GHz</span>
        </div>
      </div>

      <!-- 内存卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 dark:text-black text-sm font-medium">内存使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold dark:text-black">{{ memoryUsage }}%</span>
              <span class="text-gray-500 text-sm mb-1">%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center text-secondary">
            <i class="fa fa-memory"></i>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-secondary h-2.5 rounded-full" :style="{ width: memoryUsage + '%' }"></div>
        </div>
        <div class="flex justify-between mt-2">
          <span class="text-xs text-gray-500 dark:text-black">已用: {{ memUsed }} GB</span>
          <span class="text-xs text-gray-500 dark:text-black">总计: {{ memTotal }} GB</span>
        </div>
      </div>

      <!-- 磁盘卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 dark:text-black text-sm font-medium">磁盘使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold dark:text-black">{{ diskUsage }}%</span>
              <span class="text-gray-500 text-sm mb-1">%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-full bg-warning/10 flex items-center justify-center text-warning">
            <i class="fa fa-hdd-o"></i>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-warning h-2.5 rounded-full" :style="{ width: diskUsage + '%' }"></div>
        </div>
        <div class="flex justify-between mt-2">
          <span class="text-xs text-gray-500 dark:text-black">已用: {{ diskUsed }} GB</span>
          <span class="text-xs text-gray-500 dark:text-black">总计: {{ diskTotal }} GB</span>
        </div>
      </div>

      <!-- 网络卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 dark:text-black text-sm font-medium">网络流量</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold dark:text-black">{{ networkUsage }}</span>
              <span class="text-gray-500 text-sm mb-1">KB/s</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-full bg-info/10 flex items-center justify-center text-info">
            <i class="fa fa-wifi"></i>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-info h-2.5 rounded-full" :style="{ width: Math.min(networkUsage / 1000 * 100, 100) + '%' }"></div>
        </div>
        <div class="flex justify-between mt-2">
          <span class="text-xs text-gray-500 dark:text-black">上传: {{ networkUp }} KB/s</span>
<span class="text-xs text-gray-500 dark:text-black">下载: {{ networkDown }} KB/s</span>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- CPU 使用率图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800 dark:text-black">CPU 使用率趋势</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">1小时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-black">1天</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-black">1周</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="cpuChart"></canvas>
        </div>
      </div>

      <!-- 内存使用图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800 dark:text-black">内存使用情况</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">1小时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1天</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1周</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="memoryChart"></canvas>
        </div>
      </div>

      <!-- 磁盘使用图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800 dark:text-black">磁盘空间分布</h3>
          <div>
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 dark:bg-primary/20 text-primary">刷新</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="diskChart"></canvas>
        </div>
      </div>

      <!-- 磁盘 IO 图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800 dark:text-black">磁盘 IO 速率</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">1小时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1天</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1周</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="diskIOChart"></canvas>
        </div>
      </div>
    </div>

    <!-- 最近操作日志 -->
    <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-semibold text-gray-800 dark:text-black">最近操作日志</h3>
        <button class="text-primary text-sm hover:underline">查看全部</button>
      </div>
      <div class="overflow-x-auto">
        <div class="text-center py-10 text-gray-500">
  <p>操作日志功能正在开发中</p>
</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';


// 状态数据
const cpuUsage = ref('0');
const memoryUsage = ref('0');
const diskUsage = ref('0');
const networkUsage = ref('0');
const networkUp = ref('0');
const networkDown = ref('0');
const cpuCores = ref('12核');
const memUsed = ref('0');
const memTotal = ref('0');

const diskTotal = ref('0');

// 获取系统监控数据
const fetchSystemData = async () => {
  try {
    const response = await axios.get('/api/system-metrics');
    const data = response.data;
    cpuUsage.value = data.cpuUsage;
    memoryUsage.value = data.memoryUsage;
    diskUsage.value = data.diskUsage;
    networkUsage.value = data.networkUsage;
    networkUp.value = data.networkUp;
    networkDown.value = data.networkDown;
    memUsed.value = data.memUsed;
    memTotal.value = data.memTotal;
    diskUsed.value = data.diskUsed;
    diskTotal.value = data.diskTotal;
  } catch (error) {
    console.error('获取系统数据失败:', error);
  }
};

  // 刷新数据
  const refreshData = async () => {
    await fetchSystemData();
  };

  onMounted(async () => {
    await fetchSystemData();
    initCharts();
    // 设置定时刷新
    const interval = setInterval(fetchSystemData, 5000);
    onUnmounted(() => clearInterval(interval));
  });
  const cpuFrequency = ref('3.7');
const diskUsed = ref('0');



// 图表实例
let cpuChart = null;
let memoryChart = null;
let diskChart = null;
let diskIOChart = null;

// 初始化图表
function initCharts() {
  const labels = ['实时'];

  // CPU 使用率图表
  cpuChart = new Chart(document.getElementById('cpuChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ label: 'CPU 使用率 (%)', data: [cpuUsage.value], borderColor: '#165DFF', backgroundColor: 'rgba(22, 93, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } } }
  });

  // 内存使用图表
  memoryChart = new Chart(document.getElementById('memoryChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ label: '内存使用 (%)', data: [memoryUsage.value], borderColor: '#00B42A', backgroundColor: 'rgba(0, 180, 42, 0.1)', borderWidth: 2, tension: 0.3, fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } } }
  });

  // 磁盘使用图表
  diskChart = new Chart(document.getElementById('diskChart'), {
    type: 'doughnut',
    data: { labels: ['已使用', '空闲'], datasets: [{ data: [diskUsage.value, 100 - diskUsage.value], backgroundColor: ['#FF7D00', '#F2F3F5'], borderWidth: 0 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, cutout: '70%' }
  });

  // 磁盘 IO 图表
  diskIOChart = new Chart(document.getElementById('diskIOChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { label: '读取 (KB/s)', data: [0], borderColor: '#165DFF', backgroundColor: 'rgba(22, 93, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true },
        { label: '写入 (KB/s)', data: [0], borderColor: '#FF7D00', backgroundColor: 'rgba(255, 125, 0, 0.1)', borderWidth: 2, tension: 0.3, fill: true }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { display: false }, y: { min: 0 } } }
  });
}

// 更新图表数据
function updateCharts() {
  if (!cpuChart || !memoryChart || !diskChart || !diskIOChart) return;

  // 更新CPU图表
  cpuChart.data.datasets[0].data = [cpuUsage.value];
  cpuChart.update();

  // 更新内存图表
  memoryChart.data.datasets[0].data = [memoryUsage.value];
  memoryChart.update();

  // 更新磁盘图表
  diskChart.data.datasets[0].data = [diskUsage.value, 100 - diskUsage.value];
  diskChart.update();

  // 磁盘IO图表可在后续添加真实数据更新逻辑
}

// 监听状态变化更新图表
watch(
  () => [cpuUsage.value, memoryUsage.value, diskUsage.value],
  () => updateCharts()
);


</script>