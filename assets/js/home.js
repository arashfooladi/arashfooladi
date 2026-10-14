// The page stays readable without JavaScript. Only the decorative sea animates.
const canvas = document.querySelector('.sea-canvas');
const poster = document.querySelector('.sea-poster');
const toggle = document.querySelector('.motion-toggle');
const sea = document.querySelector('.sea');

if (canvas && poster && toggle && sea) {
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
  const context = canvas.getContext('2d', { alpha: false });
  const columns = 200;
  const rows = 100;
  const size = canvas.width / columns;
  const dotRadius = { '·': .65, '•': 1.4, '●': 2.35 };

  function paint(characters, cellColors) {
    const lines = characters.split('\n');
    context.fillStyle = '#0e0e0f';
    context.fillRect(0, 0, canvas.width, canvas.height);
    // One path per palette entry avoids thousands of separate canvas draws.
    for (let shade = 1; shade < palette.length; shade++) {
      context.beginPath();
      let populated = false;
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < columns; x++) {
          if (cellColors[y * columns + x] !== shade) continue;
          const radius = dotRadius[lines[y][x]];
          if (!radius) continue;
          const cx = (x + .5) * size;
          const cy = (y + .5) * size;
          context.moveTo(cx + radius, cy);
          context.arc(cx, cy, radius, 0, Math.PI * 2);
          populated = true;
        }
      }
      if (populated) {
        context.fillStyle = palette[shade];
        context.fill();
      }
    }
  }

  function updateButton() {
    toggle.setAttribute('aria-pressed', String(!paused));
    toggle.replaceChildren(
      document.createTextNode(paused ? 'پخش حرکت ' : 'توقف حرکت '),
      Object.assign(document.createElement('span'), { textContent: paused ? '[>]' : '[‖]', dir: 'ltr' }),
    );
    toggle.lastChild.setAttribute('aria-hidden', 'true');
  }

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
    if (!context) return false;
    if (loading) return loading;
    if (frame || worker) return true;
    const initialize = typeof Worker === 'function'
      ? new Promise((resolve, reject) => {
        worker = new Worker(new URL('./cloud-sea-worker.js', import.meta.url), { type: 'module' });
        worker.onerror = event => {
          event.preventDefault();
          reject(new Error('Cloud sea worker unavailable'));
        };
        worker.onmessage = event => {
          const { characters, colorBuffer, scenePalette } = event.data;
          pendingFrame = false;
          if (scenePalette) {
            palette = scenePalette;
            paint(characters, new Uint8Array(colorBuffer));
            resolve();
          } else if (!paused && visible && !document.hidden) {
            paint(characters, new Uint8Array(colorBuffer));
          }
        };
      })
      : import('./vendor/cloud-sea.js').then(module => {
        frame = module.default();
        palette = module.meta.palette;
        colors = new Uint8Array(columns * rows);
        paint(frame(sceneTime, { color: colors }), colors);
      });
    loading = initialize.then(() => {
      canvas.hidden = false;
      poster.hidden = true;
      return true;
    }).catch(() => {
      // Keep the local still image and hide an unavailable animation control.
      toggle.hidden = true;
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

  if (context) {
    paused = reducedMotion.matches;
    toggle.hidden = false;
    updateButton();
    toggle.addEventListener('click', () => {
      paused = !paused;
      updateButton();
      sync();
    });
    reducedMotion.addEventListener('change', event => {
      paused = event.matches;
      updateButton();
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
