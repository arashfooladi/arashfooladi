import { createSeaRenderer } from './sea-renderer.js';

// Pages stay readable without JavaScript. Only the decorative scene animates.
const canvas = document.querySelector('.sea-canvas');
const poster = document.querySelector('.sea-poster');
const sea = document.querySelector('.sea');

if (canvas && poster && sea) {
  const sceneLoaders = {
    'cloud-sea': () => import('./vendor/cloud-sea.js'),
    'night-coast': () => import('./vendor/night-coast.js'),
    'edge-orbit': () => import('./vendor/edge-orbit.js'),
  };
  const sceneName = sceneLoaders[sea.dataset.scene] ? sea.dataset.scene : 'cloud-sea';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = true;
  let visible = false;
  let frame = null;
  let worker = null;
  let pendingFrame = false;
  let colors = null;
  let palette = [];
  let loading = null;
  let animationId = 0;
  let lastPaint = 0;
  let sceneTime = 0;
  const offscreen = typeof Worker === 'function' && typeof canvas.transferControlToOffscreen === 'function';
  const context = offscreen ? null : canvas.getContext('2d', { alpha: false });
  const canAnimate = offscreen || context;
  let paint = null;

  function stop() {
    cancelAnimationFrame(animationId);
    animationId = 0;
    lastPaint = 0;
  }

  function tick(now) {
    if (paused || !visible || document.hidden) {
      stop();
      return;
    }
    if (!lastPaint) lastPaint = now;
    const elapsed = now - lastPaint;
    if (elapsed >= 1000 / 12) {
      sceneTime += Math.min(elapsed, 150) / 1000;
      if (worker) {
        if (!pendingFrame) {
          pendingFrame = true;
          worker.postMessage(sceneTime);
        }
      } else {
        paint(frame(sceneTime, { color: colors }), colors);
      }
      lastPaint = now;
    }
    animationId = requestAnimationFrame(tick);
  }

  async function loadScene() {
    if (!canAnimate) return false;
    if (loading) return loading;
    if (frame || worker) return true;
    const initialize = typeof Worker === 'function'
      ? new Promise((resolve, reject) => {
        worker = new Worker(new URL('./scene-worker.js', import.meta.url), { type: 'module' });
        worker.onerror = event => {
          event.preventDefault();
          reject(new Error('Scene worker unavailable'));
        };
        worker.onmessage = event => {
          if (event.data.error) {
            reject(new Error(event.data.error));
            return;
          }
          const { characters, colorBuffer, scenePalette, ground } = event.data;
          pendingFrame = false;
          if (scenePalette) {
            palette = scenePalette;
            if (!offscreen) {
              paint = createSeaRenderer(context, palette, canvas.width, canvas.height, ground);
              paint(characters, new Uint8Array(colorBuffer));
            }
            resolve();
          } else if (!offscreen && !paused && visible && !document.hidden) {
            paint(characters, new Uint8Array(colorBuffer));
          }
        };
        if (offscreen) {
          const surface = canvas.transferControlToOffscreen();
          worker.postMessage({ canvas: surface, sceneName }, [surface]);
        } else {
          worker.postMessage({ canvas: null, sceneName });
        }
      })
      : sceneLoaders[sceneName]().then(module => {
        frame = module.default();
        palette = module.meta.palette;
        colors = new Uint8Array(module.meta.cols * module.meta.rows);
        paint = createSeaRenderer(context, palette, canvas.width, canvas.height, module.meta.ground);
        paint(frame(sceneTime, { color: colors }), colors);
      });
    loading = initialize.then(() => {
      canvas.hidden = false;
      poster.hidden = true;
      return true;
    }).catch(() => {
      // Keep the local still image if the animation cannot load.
      worker?.terminate();
      worker = null;
      return false;
    });
    return loading;
  }

  async function sync() {
    if (paused || !visible || document.hidden) {
      stop();
      return;
    }
    if (await loadScene() && !animationId && !paused && visible && !document.hidden) {
      animationId = requestAnimationFrame(tick);
    }
  }

  if (canAnimate) {
    paused = reducedMotion.matches;
    reducedMotion.addEventListener('change', event => {
      paused = event.matches;
      sync();
    });
    document.addEventListener('visibilitychange', sync);
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      sync();
    }, { threshold: .05 }).observe(sea);
    window.addEventListener('pagehide', stop);
    window.addEventListener('pageshow', sync);
  }
}
