import { ref, onMounted, onUnmounted } from 'vue';

export function useSystemMonitoring(refreshRate = 5000) {
  const metrics = ref({ cpu: 0, memory: 0, disk: 0 });
  let interval;

  const fetchMetrics = () => {
    // Replace with actual API call
    metrics.value = {
      cpu: Math.floor(Math.random() * 100),
      memory: Math.floor(Math.random() * 100),
      disk: Math.floor(Math.random() * 100)
    };
  };

  onMounted(() => {
    fetchMetrics();
    interval = setInterval(fetchMetrics, refreshRate);
  });

  onUnmounted(() => clearInterval(interval));

  return { metrics };
}