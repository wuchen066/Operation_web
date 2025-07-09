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
logDirectory: '',
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
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
      <h2 class="text-xl sm:text-2xl font-bold dark:text-black">系统设置</h2>
      <button @click="saveSettings" class="w-full sm:w-auto bg-primary text-white dark:text-black px-6 py-3 rounded-md hover:bg-primary/90 transition-all duration-300 shadow-sm hover:shadow text-center font-medium">
        保存设置
      </button>
    </div>

    <ElTabs v-model="activeTab" class="settings-tabs">
      <!-- 基本设置 -->
      <ElTabPane label="基本设置" label-class="dark:text-black" name="basic">
        <div class="settings-card p-8 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
            <div class="setting-item">
              <label class="block text-gray-700 dark:text-black mb-2 font-medium">面板别名</label>
              <ElInput v-model="settings.displayName" placeholder="给面板取个别的名称，用于网页标题" class="w-full" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 dark:text-black mb-2 font-medium">刷新频率 (秒)</label>
              <ElInput v-model.number="settings.refreshRate" type="number" min="1" max="60" class="w-full" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 dark:text-black mb-2 font-medium">默认日志目录</label>
              <ElInput v-model="settings.logDirectory" placeholder="请输入日志目录路径" class="w-full" />
            </div>

            <div class="setting-section-divider md:col-span-2"></div>

            <div class="setting-item md:col-span-2 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg mt-4">
              <label class="block text-gray-700 dark:text-black mb-3 font-medium">显示选项</label>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 sm:gap-6">
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showCpuUsage" />
                  <span class="ml-2 dark:text-black">CPU使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showMemoryUsage" />
                  <span class="ml-2 dark:text-black">内存使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showDiskUsage" />
                  <span class="ml-2 dark:text-black">磁盘使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showNetworkUsage" />
                  <span class="ml-2 dark:text-black">网络使用率</span>
                </label>
                <label class="flex items-center">
                  <ElSwitch v-model="settings.showProcessList" />
                  <span class="ml-2 dark:text-black">进程列表</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </ElTabPane>

      <!-- 服务器配置 -->
      <ElTabPane label="服务器配置" label-class="dark:text-black" name="server">
        <div class="settings-card p-8 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
              <div class="setting-item">
                <label class="block text-gray-700 dark:text-black mb-2 font-medium">服务器IP</label>
                <ElInput v-model="settings.serverHost" placeholder="请输入服务器IP地址" class="w-full" />
              </div>

              <div class="setting-item">
                <label class="block text-gray-700 dark:text-black mb-2 font-medium">端口号</label>
                <ElInput v-model.number="settings.serverPort" type="number" min="1" max="65535" class="w-full" />
              </div>

              <div class="setting-item md:col-span-2">
                <label class="block text-gray-700 dark:text-black mb-2 font-medium">连接超时 (秒)</label>
                <ElSlider v-model="settings.timeout" :min="1" :max="30" :step="1" class="w-full" />
                <div class="text-right text-sm text-gray-500 dark:text-black mt-2">{{ settings.timeout }} 秒</div>
              </div>

              <div class="setting-section-divider md:col-span-2"></div>

              <div class="setting-item md:col-span-2 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <label class="block text-gray-700 dark:text-black mb-3 font-medium">高级选项</label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-6">
                  <label class="flex items-center">
                    <ElSwitch v-model="settings.enableCompression" />
                    <span class="ml-2 dark:text-black">启用数据压缩</span>
                  </label>
                  <label class="flex items-center">
                    <ElSwitch v-model="settings.enableCache" />
                    <span class="ml-2 dark:text-black">启用缓存</span>
                  </label>
                  <label class="flex items-center">
                    <ElSwitch v-model="settings.autoReconnect" />
                    <span class="ml-2 dark:text-black">自动重连</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
      </ElTabPane>

      <!-- 关于 -->
      <ElTabPane label="关于" label-class="dark:text-black" name="about">
        <div class="settings-card p-4 bg-white rounded-lg shadow-sm">
          <div class="text-center">
            <div class="text-2xl  dark:text-black font-bold mb-2">{{ settings.displayName }}</div>
            <div class="text-gray-500 dark:text-black mb-4">版本 v1.0.0</div>
            <div class="text-gray-600 dark:text-black ">服务器运维监控工具</div>
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
  transition: all 0.3s ease;
}

.setting-item label {
  font-size: 0.95rem;
}

.setting-item input {
  min-height: 42px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
  transition: border-color 0.2s;
}

.setting-item input:focus {
  border-color: #165DFF;
  outline: none;
  box-shadow: 0 0 0 2px rgba(22, 93, 255, 0.2);
}

.setting-item {
  margin-bottom: 2rem;
}

.setting-section-divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 1.5rem 0;
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
    margin-bottom: 1rem;
  }

  .el-tabs__item {
    transition: all 0.2s ease;
  }

  .el-tabs__item:hover {
    color: #165DFF;
  }

  .el-tabs__item.is-active {
    color: #165DFF;
    font-weight: 500;
    border-bottom: 2px solid #165DFF;
  }

  .el-tabs__item {
    flex-shrink: 0;
  }
}
</style>