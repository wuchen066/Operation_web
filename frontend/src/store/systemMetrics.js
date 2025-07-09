import { defineStore } from 'pinia';

export const useSystemMetricsStore = defineStore('systemMetrics', {
  state: () => ({ cpuUsage: 0, memoryUsage: 0, diskUsage: 0 }),
  actions: {
    updateMetrics(newMetrics) {
      this.cpuUsage = newMetrics.cpu;
      this.memoryUsage = newMetrics.memory;
      this.diskUsage = newMetrics.disk;
    }
  }
});