import { defineStore } from 'pinia';

export const useSystemMetricsStore = defineStore('systemMetrics', {
  state: () => ({ cpuUsage: 0, memoryUsage: 0, diskUsage: 0, networkUsage: 0, networkUp: '0', networkDown: '0' }),

  actions: {
    updateMetrics(metrics) {
      this.cpuUsage = metrics.cpu;
      this.memoryUsage = metrics.memory;
      this.diskUsage = metrics.disk;
      this.networkUsage = metrics.networkUsage;
      this.networkUp = metrics.networkUp;
      this.networkDown = metrics.networkDown;
    }
  }
});