// Curated community artwork. Sources and adaptation notes: assets/art/CREDITS.md.
// Each accent plays once on entry; the birds also remember across page visits.
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const reload = performance.getEntriesByType('navigation')[0]?.type === 'reload';

for (const element of document.querySelectorAll('[data-ascii-art]')) {
  const name = element.dataset.asciiArt;
  const sources = {
    birds: new URL('../art/birds.json', import.meta.url),
    squirrel: new URL('../art/squirrel.json', import.meta.url),
    crosshatch: new URL('../art/crosshatch.json', import.meta.url),
  };
  if (!sources[name]) continue;
  const canvas = element.querySelector('canvas');
  const context = canvas?.getContext('2d');
  if (!context) continue;
  const key = `ascii-once:${name}`;
  const remember = element.dataset.once === 'session';
  let remembered = false;
  try {
    if (remember && reload) sessionStorage.removeItem(key);
    remembered = remember && sessionStorage.getItem(key) === 'played';
  } catch { /* Playback still works when browser storage is disabled. */ }
  if (remembered) continue;

  let artwork = null;
  let loading = null;
  let visible = false;
  let finished = false;
  let started = false;
  let animation = 0;
  let frameIndex = 0;
  let frameElapsed = 0;
  let lastTick = 0;
  const font = name === 'birds' ? '"IBM VGA", monospace' : '"JetBrains Mono", monospace';

  function paint() {
    if (!artwork) return;
    const size = canvas.width / artwork.width;
    const lineHeight = canvas.height / artwork.height;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = getComputedStyle(element).color;
    context.font = `${size * 1.6}px ${font}`;
    context.textBaseline = 'middle';
    for (const [y, row] of artwork.frames[frameIndex].rows.entries()) {
      for (let x = 0; x < row.length; x++) {
        if (row[x] !== ' ') context.fillText(row[x], x * size, (y + .5) * lineHeight);
      }
    }
  }

  function resize() {
    if (!artwork) return;
    const width = element.clientWidth;
    const height = element.clientHeight;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    paint();
  }

  function stop() {
    cancelAnimationFrame(animation);
    animation = 0;
    lastTick = 0;
  }

  function tick(now) {
    if (!visible || document.hidden || motion.matches || finished) {
      stop();
      return;
    }
    if (!lastTick) lastTick = now;
    frameElapsed += Math.min(now - lastTick, 100);
    lastTick = now;
    if (frameElapsed >= artwork.frames[frameIndex].duration) {
      frameElapsed -= artwork.frames[frameIndex].duration;
      frameIndex++;
      if (frameIndex >= artwork.frames.length) {
        frameIndex = artwork.frames.length - 1;
        finished = true;
        element.dataset.playback = 'finished';
        if (name === 'birds') canvas.hidden = true;
        stop();
        return;
      }
      paint();
    }
    animation = requestAnimationFrame(tick);
  }

  async function sync() {
    if (!visible || document.hidden || finished) {
      stop();
      return;
    }
    if (!loading) loading = fetch(sources[name])
      .then(response => {
        if (!response.ok) throw new Error('Artwork unavailable');
        return response.json();
      })
      .then(async data => {
        await document.fonts.load(`16px ${font}`);
        artwork = data;
        resize();
        // Reduced-motion readers get quiet still accents; no birds take off.
        canvas.hidden = motion.matches && name === 'birds';
      })
      .catch(() => { finished = true; canvas.hidden = true; });
    await loading;
    if (!artwork || !visible || document.hidden || finished) return;
    if (motion.matches) {
      stop();
      if (name === 'birds') canvas.hidden = true;
      return;
    }
    canvas.hidden = false;
    if (!started) {
      started = true;
      element.dataset.playback = 'playing';
      if (remember) {
        try { sessionStorage.setItem(key, 'played'); } catch { /* Optional memory. */ }
      }
    }
    if (!animation) animation = requestAnimationFrame(tick);
  }

  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    sync();
  }, { threshold: name === 'birds' ? .2 : .35 }).observe(name === 'birds' ? element.closest('.site-footer') : element);
  new ResizeObserver(resize).observe(element);
  document.addEventListener('visibilitychange', sync);
  motion.addEventListener('change', sync);
  addEventListener('pagehide', stop);
  addEventListener('pageshow', sync);
}
