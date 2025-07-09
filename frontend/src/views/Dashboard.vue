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
            <h3 class="text-gray-500 text-sm font-medium">CPU 使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold">{{ cpuUsage }}%</span>
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
          <span class="text-xs text-gray-500">核心数: {{ cpuCores }}</span>
          <span class="text-xs text-gray-500">频率: {{ cpuFrequency }} GHz</span>
        </div>
      </div>

      <!-- 内存卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 text-sm font-medium">内存使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold">{{ memUsage }}%</span>
              <span class="text-gray-500 text-sm mb-1">%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center text-secondary">
            <i class="fa fa-memory"></i>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-secondary h-2.5 rounded-full" :style="{ width: memUsage + '%' }"></div>
        </div>
        <div class="flex justify-between mt-2">
          <span class="text-xs text-gray-500">已用: {{ memUsed }} GB</span>
          <span class="text-xs text-gray-500">总计: {{ memTotal }} GB</span>
        </div>
      </div>

      <!-- 磁盘卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 text-sm font-medium">磁盘使用率</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold">{{ diskUsage }}%</span>
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
          <span class="text-xs text-gray-500">已用: {{ diskUsed }} GB</span>
          <span class="text-xs text-gray-500">总计: {{ diskTotal }} GB</span>
        </div>
      </div>

      <!-- 网络卡片 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-gray-500 text-sm font-medium">网络流量</h3>
            <div class="flex items-end space-x-1">
              <span class="text-2xl font-bold">{{ networkUsage }}</span>
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
          <span class="text-xs text-gray-500">上传: {{ networkUp }} KB/s</span>
          <span class="text-xs text-gray-500">下载: {{ networkDown }} KB/s</span>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- CPU 使用率图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">CPU 使用率趋势</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">1小时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1天</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1周</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="cpuChart"></canvas>
        </div>
      </div>

      <!-- 内存使用图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">内存使用情况</h3>
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
          <h3 class="font-semibold text-gray-800">磁盘空间分布</h3>
          <div>
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">刷新</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="diskChart"></canvas>
        </div>
      </div>

      <!-- 磁盘 IO 图表 -->
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">磁盘 IO 速率</h3>
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
        <h3 class="font-semibold text-gray-800">最近操作日志</h3>
        <button class="text-primary text-sm hover:underline">查看全部</button>
      </div>
      <div class="overflow-x-auto">
        <el-table :data="operationLogs" stripe border class="w-full">
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
          <el-table-column prop="user" label="用户" width="120"></el-table-column>
          <el-table-column prop="operation" label="操作"></el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                {{ scope.row.status }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import { ElTable, ElTableColumn } from 'element-plus';

// 状态数据
const cpuUsage = ref(0);
const cpuCores = ref('12核');
const cpuFrequency = ref('3.7');
const memUsage = ref(0);
const memUsed = ref('0');
const memTotal = ref('16');
const diskUsage = ref(0);
const diskUsed = ref('0');
const diskTotal = ref('500');
const networkUsage = ref(0);
const networkUp = ref('0');
const networkDown = ref('0');

// 图表实例
let cpuChart = null;
let memoryChart = null;
let diskChart = null;
let diskIOChart = null;

// 操作日志数据
const operationLogs = ref([]);

// 生成时间标签（过去60分钟）
function generateTimeLabels() {
  return Array.from({ length: 60 }, (_, i) => {
    const date = new Date();
    date.setMinutes(date.getMinutes() - 59 + i);
    return `${date.getHours()}:${date.getMinutes() < 10 ? '0' : ''}${date.getMinutes()}`;
  });
}

// 生成静态数据
function generateStaticData(value, count) {
  return Array.from({ length: count }, () => value);
}

// 初始化图表
function initCharts() {
  const labels = generateTimeLabels();
  const cpuData = generateStaticData(0, 60);
  const memData = generateStaticData(0, 60);
  const diskIORead = generateStaticData(0, 60);
  const diskIOWrite = generateStaticData(0, 60);

  // CPU 使用率图表
  cpuChart = new Chart(document.getElementById('cpuChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ label: 'CPU 使用率 (%)', data: cpuData, borderColor: '#165DFF', backgroundColor: 'rgba(22, 93, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } } }
  });

  // 内存使用图表
  memoryChart = new Chart(document.getElementById('memoryChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ label: '内存使用 (%)', data: memData, borderColor: '#00B42A', backgroundColor: 'rgba(0, 180, 42, 0.1)', borderWidth: 2, tension: 0.3, fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } } }
  });

  // 磁盘使用图表
  diskChart = new Chart(document.getElementById('diskChart'), {
    type: 'doughnut',
    data: { labels: ['已使用', '空闲'], datasets: [{ data: [0, 0], backgroundColor: ['#FF7D00', '#F2F3F5'], borderWidth: 0 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, cutout: '70%' }
  });

  // 磁盘 IO 图表
  diskIOChart = new Chart(document.getElementById('diskIOChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { label: '读取 (KB/s)', data: diskIORead, borderColor: '#165DFF', backgroundColor: 'rgba(22, 93, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true },
        { label: '写入 (KB/s)', data: diskIOWrite, borderColor: '#FF7D00', backgroundColor: 'rgba(255, 125, 0, 0.1)', borderWidth: 2, tension: 0.3, fill: true }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { display: false }, y: { min: 0 } } }
  });
}

// 更新图表数据
function updateCharts() {
  if (!cpuChart || !memoryChart || !diskIOChart) return;

  // 停止更新图表数据
}

// 模拟系统数据加载
function simulateSystemDataLoading() {
  cpuUsage.value = 0;
  memUsage.value = 0;
  diskUsage.value = 0;
  networkUsage.value = 0;
  networkUp.value = '0';
  networkDown.value = '0';
}

// 刷新数据
function refreshData() {
  simulateSystemDataLoading();
  updateCharts();
}

// 组件挂载时初始化
onMounted(() => {
  initCharts();
  simulateSystemDataLoading();
  // 定时更新数据
  const interval = setInterval(() => {
    simulateSystemDataLoading();
    updateCharts();
  }, 5000);

  // 保存interval以便组件卸载时清除
  onUnmounted(() => {
    clearInterval(interval);
    // 销毁图表实例
    cpuChart.destroy();
    memoryChart.destroy();
    diskChart.destroy();
    diskIOChart.destroy();
  });
});
</script>