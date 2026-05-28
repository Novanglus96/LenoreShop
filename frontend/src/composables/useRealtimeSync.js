import { ref, onMounted, onUnmounted } from "vue";
import { useQueryClient } from "@tanstack/vue-query";

export function useRealtimeSync() {
  const queryClient = useQueryClient();
  const connected = ref(false);
  let ws = null;
  let reconnectTimer = null;

  function connect() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/sync/`);

    ws.onopen = () => {
      connected.value = true;
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
      }
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "invalidate" && Array.isArray(data.keys)) {
          data.keys.forEach((key) =>
            queryClient.invalidateQueries({ queryKey: [key] }),
          );
        }
      } catch {
        // ignore malformed messages
      }
    };

    ws.onclose = () => {
      connected.value = false;
      reconnectTimer = setTimeout(connect, 3000);
    };

    ws.onerror = () => ws.close();
  }

  onMounted(connect);

  onUnmounted(() => {
    if (reconnectTimer) clearTimeout(reconnectTimer);
    if (ws) {
      ws.onclose = null;
      ws.close();
    }
  });

  return { connected };
}
