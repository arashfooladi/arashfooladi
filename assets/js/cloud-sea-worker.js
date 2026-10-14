// Calculate the scene away from the main thread so links and scrolling stay responsive.
import cloudSea, { meta } from './vendor/cloud-sea.js';

const frame = cloudSea();
const colors = new Uint8Array(meta.cols * meta.rows);

function sendFrame(time, first = false) {
  const characters = frame(time, { color: colors });
  const colorBuffer = colors.slice().buffer;
  self.postMessage({ characters, colorBuffer, scenePalette: first ? meta.palette : null }, [colorBuffer]);
}

self.onmessage = event => sendFrame(event.data);
sendFrame(0, true);
