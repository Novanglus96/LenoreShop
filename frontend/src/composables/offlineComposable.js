import { ref } from "vue";

export const isOffline = ref(!navigator.onLine);

window.addEventListener("online", () => {
  isOffline.value = false;
});
window.addEventListener("offline", () => {
  isOffline.value = true;
});

const STORAGE_KEY = "pendingListItemUpdates";

export function loadPendingUpdates() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

export function savePendingUpdate(listItem) {
  const pending = loadPendingUpdates();
  const idx = pending.findIndex((p) => p.id === listItem.id);
  if (idx !== -1) {
    pending[idx] = listItem;
  } else {
    pending.push(listItem);
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(pending));
}

export function removePendingUpdate(id) {
  const pending = loadPendingUpdates().filter((p) => p.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(pending));
}

export function clearPendingUpdates() {
  localStorage.removeItem(STORAGE_KEY);
}

export function useOffline() {
  return { isOffline };
}
