<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElTabs, ElTabPane, ElInput, ElSlider, ElSwitch, ElSelect, ElOption } from 'element-plus';

// 状态数据 - 设置默认显示基本设置
const activeTab = ref('basic');

// 设置数据 - 移除主题相关配置
const settings = reactive({
  // 基本设置
  displayName: '服务器监控系统',
  refreshRate: '5',
  showCpuUsage: true,
  showMemoryUsage: true,
  showDiskUsage: true,
  showNetworkUsage: true,
  showProcessList: true,
  enableAlerts: true,
  alertOnHighCpu: true,
  alertOnHighMemory: true,
  alertOnHighDisk: true,

  // 服务器配置
  serverHost: 'localhost',
  serverPort: '15600',
  connectionTimeout: 30,
  maxConnections: 10,
  enableCompression: true,
  enableCache: true,
  autoReconnect: true
});

// 保存设置
function saveSettings() {
  ElMessage.success('设置已保存');
  // 保存后刷新页面
  setTimeout(() => {
    window.location.reload();
  }, 1000);
}

// 组件挂载时初始化
onMounted(() => {
  // 初始化设置（不再从localStorage加载）
});
</script>

<template>
  <div class="settings-container p-4 sm:p-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h2 class="text-xl sm:text-2xl font-bold">系统设置</h2>
      <button @click="saveSettings" class="w-full sm:w-auto bg-primary text-white px-4 py-3 rounded-md hover:bg-primary/90 transition-colors text-center">
        保存设置
      </button>
    </div>

    <ElTabs v-model="activeTab" class="settings-tabs">
      <!-- 基本设置 -->
      <ElTabPane label="基本设置" name="basic">
        <div class="settings-card p-4 bg-white rounded-lg shadow-sm">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="setting-item">
              <label class="block text-gray-700 mb-2">面板别名</label>
              <ElInput v-model="settings.displayName" placeholder="给面板取个别的名称，用于网页标题" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 mb-2">刷新频率 (秒)</label>
              <ElInput v-model.number="settings.refreshRate" type="number" min="1" max="60" />
            </div>

            <div class="setting-item md:col-span-2">
              <label class="block text-gray-700 mb-2">显示选项</label>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showCpuUsage" />
                  <span class="ml-2">CPU使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showMemoryUsage" />
                  <span class="ml-2">内存使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showDiskUsage" />
                  <span class="ml-2">磁盘使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showNetworkUsage" />
                  <span class="ml-2">网络使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showProcessList" />
                  <span class="ml-2">进程列表</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </ElTabPane>

      <!-- 服务器配置 -->
      <ElTabPane label="服务器配置" name="server">
        <div class="settings-card p-4 bg-white rounded-lg shadow-sm">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="setting-item">
              <label class="block text-gray-700 mb-2">服务器地址</label>
              <ElInput v-model="settings.serverHost" placeholder="请输入服务器地址" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 mb-2">端口号</label>
              <ElInput v-model="settings.serverPort" placeholder="请输入端口号" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 mb-2">连接超时 (秒)</label>
              <ElSlider v-model="settings.connectionTimeout" :min="5" :max="60" :step="1" />
              <div class="text-right text-sm text-gray-500">{{ settings.connectionTimeout }} 秒</div>
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 mb-2">最大连接数</label>
              <ElInput v-model.number="settings.maxConnections" type="number" min="1" max="100" />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-6">
            <label class="flex items-center">
              <ElSwitch v-model="settings.enableCompression" />
              <span class="ml-2">启用数据压缩</span>
            </label>
            <label class="flex items-center">
              <ElSwitch v-model="settings.enableCache" />
              <span class="ml-2">启用缓存</span>
            </label>
            <label class="flex items-center">
              <ElSwitch v-model="settings.autoReconnect" />
              <span class="ml-2">自动重连</span>
            </label>
          </div>
        </div>
      </ElTabPane>

      <!-- 关于 -->
      <ElTabPane label="关于" name="about">
        <div class="settings-card p-4 bg-white rounded-lg shadow-sm">
          <div class="text-center">
            <div class="text-2xl font-bold mb-2">{{ settings.displayName }}</div>
            <div class="text-gray-500 mb-4">版本 v1.0.0</div>
            <div class="text-gray-600">服务器运维监控工具</div>
          </div>
        </div>
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<style scoped>
.settings-container {
  max-width: 1000px;
  margin: 0 auto;
}

.settings-card {
  border: 1px solid #e5e7eb;
}

.setting-item {
  margin-bottom: 1.5rem;
}

/* 移动端优化 */
@media (max-width: 640px) {
  .setting-item {
    margin-bottom: 1rem;
  }

  .el-tabs__nav {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .el-tabs__item {
    flex-shrink: 0;
  }
}
</style>