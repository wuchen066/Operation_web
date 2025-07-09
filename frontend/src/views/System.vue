<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-gray-800">系统监控</h2>
      <div class="flex space-x-2">
        <div class="relative">
          <button class="bg-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-gray-50 transition-colors">
            <i class="fa fa-calendar text-gray-500"></i>
            <span class="text-sm">刷新频率: <span>{{ refreshRate }}秒</span></span>
            <i class="fa fa-angle-down text-gray-500"></i>
          </button>
        </div>
        <button @click="refreshData" class="bg-primary text-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-primary/90 transition-colors">
          <i class="fa fa-refresh"></i>
          <span class="text-sm">立即刷新</span>
        </button>
      </div>
    </div>

    <!-- 系统监控卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">CPU 信息</h3>
          <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
            <i class="fa fa-microchip"></i>
          </div>
        </div>
        <div class="space-y-3">
          <div>
            <div class="text-sm text-gray-500 mb-1">型号</div>
            <div class="font-medium">{{ cpuModel }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">核心数</div>
            <div class="font-medium">{{ cpuCores }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">频率</div>
            <div class="font-medium">{{ cpuFrequency }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">当前使用率</div>
            <div class="flex items-center">
              <div class="font-medium mr-2">{{ cpuUsage }}%</div>
              <div class="w-full bg-gray-200 rounded-full h-2.5 flex-1">
                <div class="bg-primary h-2.5 rounded-full" :style="{ width: cpuUsage + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">内存信息</h3>
          <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center text-secondary">
            <i class="fa fa-memory"></i>
          </div>
        </div>
        <div class="space-y-3">
          <div>
            <div class="text-sm text-gray-500 mb-1">总内存</div>
            <div class="font-medium">{{ memTotal }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">已使用</div>
            <div class="font-medium">{{ memUsed }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">空闲</div>
            <div class="font-medium">{{ memFree }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">使用率</div>
            <div class="flex items-center">
              <div class="font-medium mr-2">{{ memUsage }}%</div>
              <div class="w-full bg-gray-200 rounded-full h-2.5 flex-1">
                <div class="bg-secondary h-2.5 rounded-full" :style="{ width: memUsage + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">系统信息</h3>
          <div class="w-8 h-8 rounded-full bg-info/10 flex items-center justify-center text-info">
            <i class="fa fa-info-circle"></i>
          </div>
        </div>
        <div class="space-y-3">
          <div>
            <div class="text-sm text-gray-500 mb-1">操作系统</div>
            <div class="font-medium">{{ osName }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">主机名</div>
            <div class="font-medium">{{ hostname }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">正常运行时间</div>
            <div class="font-medium">{{ uptime }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 mb-1">当前用户</div>
            <div class="font-medium">{{ currentUser }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细监控图表 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">CPU 核心使用率</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">实时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">10分钟</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1小时</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="cpuCoresChart"></canvas>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">内存使用趋势</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">实时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">10分钟</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1小时</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="memoryTrendChart"></canvas>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">磁盘空间</h3>
          <div>
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">刷新</button>
          </div>
        </div>
        <div id="disk-partitions" class="space-y-4">
          <div v-for="partition in diskPartitions" :key="partition.name" class="flex justify-between items-center">
            <div>
              <div class="font-medium">{{ partition.name }}</div>
              <div class="text-sm text-gray-500">{{ partition.type }}</div>
            </div>
            <div class="w-48">
              <div class="flex justify-between text-xs mb-1">
                <span>{{ partition.used }} / {{ partition.total }}</span>
                <span>{{ partition.usage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div :class="partition.colorClass" class="h-2 rounded-full" :style="{ width: partition.usage + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-semibold text-gray-800">网络流量</h3>
          <div class="flex space-x-2">
            <button class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary">实时</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">10分钟</button>
            <button class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-500">1小时</button>
          </div>
        </div>
        <div class="h-64">
          <canvas id="networkChart"></canvas>
        </div>
      </div>
    </div>

    <!-- 进程列表 -->
    <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-semibold text-gray-800">运行中的进程</h3>
        <div class="flex items-center space-x-2">
          <div class="relative">
            <input type="text" v-model="searchProcess" placeholder="搜索进程..." class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none">
            <i class="fa fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          </div>
          <button @click="refreshData" class="bg-primary text-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-primary/90 transition-colors">
            <i class="fa fa-refresh"></i>
            <span class="text-sm">刷新</span>
          </button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <el-table :data="filteredProcesses" stripe border class="w-full">
          <el-table-column prop="pid" label="PID" width="80"></el-table-column>
          <el-table-column prop="name" label="名称"></el-table-column>
          <el-table-column prop="user" label="用户" width="100"></el-table-column>
          <el-table-column prop="cpu" label="CPU %" width="80"></el-table-column>
          <el-table-column prop="mem" label="内存 %" width="80"></el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                {{ scope.row.status }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="uptime" label="运行时间" width="120"></el-table-column>
          <el-table-column label="操作" width="100" align="right">
            <template #default>
              <button class="text-red-600 hover:text-red-900">终止</button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="flex justify-between items-center mt-4 text-sm text-gray-500">
        <div>显示 1-10 条，共 <span>{{ processes.length }}</span> 条</div>
        <div class="flex space-x-1">
          <button class="px-3 py-1 rounded border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed" disabled>上一页</button>
          <button class="px-3 py-1 rounded border border-gray-300 bg-primary text-white">1</button>
          <button class="px-3 py-1 rounded border border-gray-300 bg-white hover:bg-gray-50">2</button>
          <button class="px-3 py-1 rounded border border-gray-300 bg-white hover:bg-gray-50">3</button>
          <button class="px-3 py-1 rounded border border-gray-300 bg-white hover:bg-gray-50">下一页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import { ElTable, ElTableColumn } from 'element-plus';

// 状态数据
const refreshRate = ref(5);
const cpuModel = ref('');
const cpuCores = ref('');
const cpuFrequency = ref('');
const cpuUsage = ref(0);
const memTotal = ref('0 GB');
const memUsed = ref('0 GB');
const memFree = ref('0 GB');
const memUsage = ref(0);
const osName = ref('');
const hostname = ref('');
const uptime = ref('');
const currentUser = ref('');
const searchProcess = ref('');

// 图表实例
let cpuCoresChart = null;
let memoryTrendChart = null;
let networkChart = null;

// 磁盘分区数据
const diskPartitions = ref([]);

// 进程数据
const processes = ref([]);

// 过滤后的进程列表
const filteredProcesses = ref([...processes.value]);

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
  const cpuCoresData = generateStaticData(0, 6);
  const memTotalData = Array(60).fill(0);
  const memUsedData = generateStaticData(0, 60);
  const memFreeData = generateStaticData(0, 60);
  const networkUpData = generateStaticData(0, 60);
  const networkDownData = generateStaticData(0, 60);

  // CPU 核心使用率图表
  cpuCoresChart = new Chart(document.getElementById('cpuCoresChart'), {
    type: 'bar',
    data: {
      labels: ['核心 1', '核心 2', '核心 3', '核心 4', '核心 5', '核心 6'],
      datasets: [{
        label: 'CPU 使用率 (%)',
        data: cpuCoresData,
        backgroundColor: [
          'rgba(22, 93, 255, 0.7)',
          'rgba(0, 180, 42, 0.7)',
          'rgba(255, 125, 0, 0.7)',
          'rgba(245, 63, 63, 0.7)',
          'rgba(134, 144, 156, 0.7)',
          'rgba(29, 33, 41, 0.7)'
        ],
        borderWidth: 0,
        borderRadius: 4
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } } }
  });

  // 内存趋势图表
  memoryTrendChart = new Chart(document.getElementById('memoryTrendChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { label: '已使用 (GB)', data: memUsedData, borderColor: '#FF7D00', backgroundColor: 'rgba(255, 125, 0, 0.1)', borderWidth: 2, tension: 0.3, fill: true },
        { label: '空闲 (GB)', data: memFreeData, borderColor: '#00B42A', backgroundColor: 'rgba(0, 180, 42, 0.1)', borderWidth: 2, tension: 0.3, fill: true }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { display: false }, y: { min: 0, ticks: { callback: v => v + ' GB' } } } }
  });

  // 网络流量图表
  networkChart = new Chart(document.getElementById('networkChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { label: '上传 (KB/s)', data: networkUpData, borderColor: '#165DFF', backgroundColor: 'rgba(22, 93, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true },
        { label: '下载 (KB/s)', data: networkDownData, borderColor: '#FF7D00', backgroundColor: 'rgba(255, 125, 0, 0.1)', borderWidth: 2, tension: 0.3, fill: true }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { display: false }, y: { min: 0, ticks: { callback: v => v + ' KB/s' } } } }
  });
}

// 更新图表数据
function updateCharts() {
  if (!cpuCoresChart || !memoryTrendChart || !networkChart) return;

  // 停止更新图表数据
}

// 模拟系统数据加载
function simulateSystemDataLoading() {
  cpuUsage.value = 0;
  memUsage.value = 0;
}

// 刷新数据
function refreshData() {
  simulateSystemDataLoading();
  updateCharts();
}

// 搜索进程
function searchProcesses() {
  if (!searchProcess.value) {
    filteredProcesses.value = [...processes.value];
    return;
  }
  const searchTerm = searchProcess.value.toLowerCase();
  filteredProcesses.value = processes.value.filter(p => 
    p.name.toLowerCase().includes(searchTerm) || 
    p.pid.includes(searchTerm) || 
    p.user.toLowerCase().includes(searchTerm)
  );
}

// 组件挂载时初始化
onMounted(() => {
  initCharts();
  simulateSystemDataLoading();
  // 监听搜索输入
  searchProcess.value && searchProcesses();
  searchProcess.value = '';
  // 移除定时更新
  const interval = setInterval(() => {
    simulateSystemDataLoading();
    updateCharts();
  }, refreshRate.value * 1000);

  // 保存interval以便组件卸载时清除
  onUnmounted(() => {
    clearInterval(interval);
    // 销毁图表实例
    cpuCoresChart.destroy();
    memoryTrendChart.destroy();
    networkChart.destroy();
  });
});
</script>