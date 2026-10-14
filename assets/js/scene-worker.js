import { createSeaRenderer } from './sea-renderer.js';

const sceneLoaders = {
  'cloud-sea': () => import('./vendor/cloud-sea.js'),
  'night-coast': () => import('./vendor/night-coast.js'),
  'edge-orbit': () => import('./vendor/edge-orbit.js'),
};
let frame = null;
let colors = null;
let meta = null;
let paint = null;

function sendFrame(time, first = false) {
  const characters = frame(time, { color: colors });
  const settings = { scenePalette: first ? meta.palette : null, ground: meta.ground };
  if (paint) {
    paint(characters, colors);
    self.postMessage(settings);
  } else {
    const colorBuffer = colors.slice().buffer;
    self.postMessage({ ...settings, characters, colorBuffer }, [colorBuffer]);
  }
}

self.onmessage = async event => {
  try {
    if (typeof event.data === 'number') {
      sendFrame(event.data);
      return;
    }
    const module = await sceneLoaders[event.data.sceneName]();
    meta = module.meta;
    frame = module.default();
    colors = new Uint8Array(meta.cols * meta.rows);
    const canvas = event.data.canvas;
    if (canvas) paint = createSeaRenderer(canvas.getContext('2d', { alpha: false }), meta.palette, canvas.width, canvas.height, meta.ground);
    sendFrame(0, true);
  } catch {
    self.postMessage({ error: 'Scene unavailable' });
  }
};
