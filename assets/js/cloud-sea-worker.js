// Calculate the scene away from the main thread so links and scrolling stay responsive.
import cloudSea, { meta } from './vendor/cloud-sea.js';
import { createSeaRenderer } from './sea-renderer.js';

const frame = cloudSea();
const colors = new Uint8Array(meta.cols * meta.rows);
let paint = null;

function sendFrame(time, first = false) {
  const characters = frame(time, { color: colors });
  if (paint) {
    paint(characters, colors);
    self.postMessage({ scenePalette: first ? meta.palette : null });
    return;
  }
  const colorBuffer = colors.slice().buffer;
  self.postMessage({ characters, colorBuffer, scenePalette: first ? meta.palette : null }, [colorBuffer]);
}

self.onmessage = event => {
  if (typeof event.data === 'number') {
    sendFrame(event.data);
  } else {
    const canvas = event.data.canvas;
    if (canvas) paint = createSeaRenderer(canvas.getContext('2d', { alpha: false }), meta.palette, canvas.width, canvas.height);
    sendFrame(0, true);
  }
};
