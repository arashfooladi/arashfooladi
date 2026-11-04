// Decorative scenes follow the system setting without on-page controls.
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const listeners = new Set();
export const isPaused = () => reduced.matches;
function notify() {
  document.documentElement.dataset.motion = isPaused() ? 'paused' : 'playing';
  for (const listener of listeners) listener();
}
// Older cached scene scripts can still import this until their HTML expires.
export const toggleMotion = notify;
export function observeMotion(listener) { listeners.add(listener); listener(); }
reduced.addEventListener('change', notify);
notify();
