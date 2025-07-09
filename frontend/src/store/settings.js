import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    serverIp: '127.0.0.1',
    serverPort: 8080,
    timeout: 10,
    logDirectory: '/var/log/server-monitor',
    enableCompression: true,
    enableCache: false,
    autoReconnect: true
  }),
  actions: {
    setSettings(settings) {
      Object.assign(this, settings);
    }
  }
});