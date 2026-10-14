// The same renderer serves the worker and the fallback on older browsers.
export function createSeaRenderer(context, palette, width, height) {
  const columns = 200;
  const rows = 100;
  const size = width / columns;
  const dotRadius = { '·': .65, '•': 1.4, '●': 2.35 };
  return (characters, colors) => {
    const lines = characters.split('\n');
    context.fillStyle = '#0e0e0f';
    context.fillRect(0, 0, width, height);
    const paths = palette.map(() => new Path2D());
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        const radius = dotRadius[lines[y][x]] * size / 6;
        const shade = colors[y * columns + x];
        if (!radius || !shade) continue;
        const cx = (x + .5) * size;
        const cy = (y + .5) * size;
        paths[shade].moveTo(cx + radius, cy);
        paths[shade].arc(cx, cy, radius, 0, Math.PI * 2);
      }
    }
    for (let shade = 1; shade < palette.length; shade++) {
      context.fillStyle = palette[shade];
      context.fill(paths[shade]);
    }
  };
}
