<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 初始化标签页状态和设置数据对象
const activeTab = ref('basic');

// 初始化设置数据对象，与API返回结构对应
const settings = ref({
  display_name: '',
  refresh_rate: 0,
  serverIp: '127.0.0.1',
  serverPort: 0,
  timeout: 0,
  logDirectory: '/var/log/operation_log',
  enableCompression: false,
  enableCache: false,
  autoReconnect: false
});

// 加载时获取设置数据并填充表单
onMounted(async () => {
  try {
    const response = await axios.get('/api/settings');
    const data = response.data;
    
    // 将API返回数据映射到表单字段
    settings.value = {
      display_name: data.display_name || '',
      refresh_rate: data.refresh_rate || 0,
      serverIp: data.serverIp || '',
      serverPort: data.serverPort || 8080,
      timeout: data.timeout || 10,
      logDirectory: data.logDirectory || '',
      enableCompression: data.enableCompression || false,
      enableCache: data.enableCache || false,
      autoReconnect: data.autoReconnect || false,
      showCpuUsage: data.showCpuUsage || false,
      showMemoryUsage: data.showMemoryUsage || false,
      showDiskUsage: data.showDiskUsage || false,
      showNetworkUsage: data.showNetworkUsage || false,
      showProcessList: data.showProcessList || false, 
    };
    // 自动保存display_name到localStorage
    localStorage.setItem('display_name', settings.value.display_name);
  } catch (error) {
    ElMessage.error('获取设置数据失败，请刷新页面重试');
    console.error('Failed to fetch settings:', error);
  }
});

// 保存设置的方法
const saveSettings = async () => {
  try {
    const response = await axios.post('/api/settings', settings.value);
    ElMessage.success(response.data.message);
    // 更新localStorage缓存
    localStorage.setItem('settings', JSON.stringify({
      data: settings.value,
      timestamp: Date.now()
    }));
    // 保存display_name到localStorage
    localStorage.setItem('display_name', settings.value.display_name);
    // 触发displayName更新事件
    window.dispatchEvent(new Event('displayNameUpdated'));
    // 更新displayName状态
    // 保存成功后1秒刷新页面
    // setTimeout(() => window.location.reload(), 1000);
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '保存设置失败');
  }
};
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
              <ElInput v-model="settings.display_name" placeholder="给面板取个别的名称，用于网页标题" class="w-full" />
            </div>

            <div class="setting-item">
              <label class="block text-gray-700 dark:text-black mb-2 font-medium">刷新频率 (秒)</label>
              <ElInput v-model.number="settings.refresh_rate" type="number" min="1" max="60" class="w-full" />
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
                <ElInput v-model="settings.serverIp" placeholder="请输入服务器IP地址" class="w-full" />
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
            <div class="text-2xl  dark:text-black font-bold mb-2">服务器运维面板</div>
            <div class="text-gray-500 dark:text-black mb-4">版本 {{ version }}</div>
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