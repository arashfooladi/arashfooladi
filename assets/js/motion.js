// One preference for the decorative scenes, shared between pages and tabs.
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const key = 'portfolio-motion';
let preference = null;
try { preference = localStorage.getItem(key); } catch { /* Storage is optional. */ }
const listeners = new Set();
export const isPaused = () => preference === 'paused' || (preference !== 'playing' && reduced.matches);
function notify() {
  document.documentElement.dataset.motion = isPaused() ? 'paused' : 'playing';
  for (const listener of listeners) listener();
}
export function toggleMotion() {
  preference = isPaused() ? 'playing' : 'paused';
  try { localStorage.setItem(key, preference); } catch { /* Keep the in-page choice. */ }
  notify();
}
export function observeMotion(listener) { listeners.add(listener); listener(); }
reduced.addEventListener('change', () => {
  preference = null;
  try { localStorage.removeItem(key); } catch { /* Keep the system preference in memory. */ }
  notify();
});
addEventListener('storage', event => {
  if (event.key === key || event.key === null) { preference = event.newValue; notify(); }
});
notify();
