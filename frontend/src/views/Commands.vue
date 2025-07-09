<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-gray-800">命令执行</h2>
      <div class="flex space-x-2">
        <button @click="clearTerminal" class="bg-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-gray-50 transition-colors">
          <i class="fa fa-trash text-gray-500"></i>
          <span class="text-sm">清空终端</span>
        </button>
        <button @click="toggleFullscreen" class="bg-white shadow-sm rounded-lg px-4 py-2 flex items-center space-x-2 hover:bg-gray-50 transition-colors">
          <i class="fa fa-expand text-gray-500"></i>
          <span class="text-sm">全屏</span>
        </button>
      </div>
    </div>

    <!-- 常用命令 -->
    <div class="bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-shadow">
      <h3 class="font-semibold text-gray-800 mb-3">常用命令</h3>
      <div class="flex flex-wrap gap-2">
        <button @click="selectCommand('ls -l')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">ls -l</button>
        <button @click="selectCommand('df -h')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">df -h</button>
        <button @click="selectCommand('top')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">top</button>
        <button @click="selectCommand('free -h')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">free -h</button>
        <button @click="selectCommand('ps aux')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">ps aux</button>
        <button @click="selectCommand('netstat -tuln')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">netstat -tuln</button>
        <button @click="selectCommand('ifconfig')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">ifconfig</button>
        <button @click="selectCommand('help')" class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">help</button>
      </div>
    </div>

    <!-- 终端界面 -->
    <div class="bg-gray-900 rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow">
      <div class="bg-gray-800 px-4 py-2 flex items-center space-x-3">
        <div class="flex space-x-2">
          <div class="w-3 h-3 rounded-full bg-red-500"></div>
          <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div class="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
        <div class="text-gray-400 text-sm">终端</div>
      </div>
      <div id="terminal-output" class="p-4 text-green-400 font-mono text-sm h-80 overflow-y-auto space-y-2">
        <div v-for="(output, index) in terminalOutput" :key="index" class="whitespace-pre-wrap">
          <span class="text-yellow-400">{{ output.prompt }}</span> {{ output.command }}
          <div v-if="output.result" class="text-green-400 mt-1">{{ output.result }}</div>
          <div v-if="output.error" class="text-red-400 mt-1">{{ output.error }}</div>
        </div>
        <div v-if="isExecuting" class="flex items-center">
          <div class="animate-pulse mr-2">●</div>
          <span>执行中...</span>
        </div>
      </div>
      <div class="p-4 border-t border-gray-800">
        <div class="flex items-center">
          <span class="text-yellow-400 mr-2">{{ prompt }}</span>
          <input
            v-model="commandInput"
            @keydown.enter="executeCommand"
            class="bg-transparent text-green-400 w-full outline-none"
            placeholder="输入命令并按回车执行..."
            :disabled="isExecuting"
          >
        </div>
      </div>
    </div>

    <!-- 命令历史 -->
    <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-semibold text-gray-800">命令历史</h3>
        <button @click="clearHistory" class="text-sm text-red-500 hover:text-red-700">
          <i class="fa fa-trash mr-1"></i>清空历史
        </button>
      </div>
      <div class="overflow-x-auto">
        <el-table :data="commandHistory" stripe border class="w-full">
          <el-table-column prop="id" label="序号" width="60"></el-table-column>
          <el-table-column prop="command" label="命令"></el-table-column>
          <el-table-column prop="time" label="执行时间" width="180"></el-table-column>
          <el-table-column prop="status" label="状态" width="80">
            <template #default="scope">
              <span :class="scope.row.status === '成功' ? 'text-green-600' : 'text-red-600'">
                {{ scope.row.status }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="right">
            <template #default="scope">
              <button @click="reExecuteCommand(scope.row.command)" class="text-primary hover:text-primary/80 mr-3">
                <i class="fa fa-repeat"></i>重新执行
              </button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { ElTable, ElTableColumn } from 'element-plus';
import moment from 'moment';

// 状态数据
const commandInput = ref('');
const terminalOutput = ref([]);
const commandHistory = ref([]);
const isExecuting = ref(false);
const prompt = ref('root@localhost:~# ');
let historyId = 1;

// 选择常用命令
function selectCommand(command) {
  commandInput.value = command;
  nextTick(() => {
    const input = document.querySelector('input');
    input && input.focus();
  });
}

// 执行命令
function executeCommand() {
  if (!commandInput.value.trim() || isExecuting.value) return;

  const command = commandInput.value.trim();
  const outputEntry = {
    prompt: prompt.value,
    command: command,
    result: null,
    error: null
  };

  terminalOutput.value.push(outputEntry);
  commandInput.value = '';
  isExecuting.value = true;

  // 滚动到底部
  scrollToBottom();

  // 移除模拟执行延迟
  setTimeout(() => {
    let result = '';
    let error = null;
    let status = '成功';

    // 移除命令模拟输出
    result = '命令已执行，无模拟数据';

    // 更新输出结果
    const index = terminalOutput.value.length - 1;
    if (result) terminalOutput.value[index].result = result;
    if (error) terminalOutput.value[index].error = error;

    // 添加到历史记录
    commandHistory.value.unshift({
      id: historyId++,
      command: command,
      time: moment().format('YYYY-MM-DD HH:mm:ss'),
      status: status
    });

    isExecuting.value = false;
    scrollToBottom();
  }, 0); // 立即执行
}

// 重新执行历史命令
function reExecuteCommand(command) {
  commandInput.value = command;
  executeCommand();
}

// 清空终端
function clearTerminal() {
  terminalOutput.value = [];
}

// 清空历史
function clearHistory() {
  commandHistory.value = [];
  historyId = 1;
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    const terminal = document.getElementById('terminal-output');
    if (terminal) {
      terminal.scrollTop = terminal.scrollHeight;
    }
  });
}

// 切换全屏
function toggleFullscreen() {
  const terminal = document.querySelector('.bg-gray-900');
  if (!terminal) return;

  if (!document.fullscreenElement) {
    terminal.requestFullscreen().catch(err => {
      console.error(`全屏请求失败: ${err.message}`);
    });
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}

// 组件挂载时初始化
onMounted(() => {
  // 自动聚焦到输入框
  nextTick(() => {
    const input = document.querySelector('input');
    input && input.focus();
  });

  // 添加初始欢迎信息
  terminalOutput.value.push({
    prompt: '',
    command: '',
    result: '欢迎使用服务器管理终端\n输入命令并按回车执行，输入 help 查看可用命令',
    error: null
  });
});
</script>

<style scoped>
/* 自定义终端滚动条样式 */
#terminal-output::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

#terminal-output::-webkit-scrollbar-track {
  background: #1a1a1a;
}

#terminal-output::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

#terminal-output::-webkit-scrollbar-thumb:hover {
  background: #444;
}
</style>