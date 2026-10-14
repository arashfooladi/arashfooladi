# ASCII homepage — local review

This redesign is saved on `design/ascii-home`, based on public `master` commit `d8240fb`. It has not been pushed or deployed.

Only the homepage presentation changes. The project pages, journal pages, shared styles, published URLs, sitemap, robots file, feed, redirects, and hosting settings are unchanged. Existing homepage search metadata, Google verification, canonical URL, Open Graph, Twitter cards, and JSON-LD are preserved exactly.

The direction is charcoal and silver, Persian typography using the existing locally hosted Vazirmatn font, and ASCII details. Cloud Sea supplies the warm sunset in the hero. Project illustrations use text characters; the website itself has a small showcase section with a source link.

## Preview

From this checkout, run:

```powershell
python -m http.server 8814 --bind 127.0.0.1
```

Open `http://127.0.0.1:8814/`. Stop the preview with Ctrl+C. Opening `index.html` as a file will not run the JavaScript modules; use the HTTP preview.

## Animation

Cloud Sea is self-hosted, with no npm installation or external runtime request. Its calculation runs in a module worker while the canvas renders at up to 12 frames per second. The animation pauses offscreen and when the browser tab is hidden. A visible button pauses or resumes it. Reduced-motion visitors initially receive the static WebP image and can explicitly opt into animation. The still image also remains available without JavaScript or if the animation module cannot load.

Source: [Cloud Sea](https://ascii.rest/cloud-sea/) by [bas3line](https://github.com/bas3line/ascii). The bundled original generator and its MIT license are in `assets/js/vendor/`. The dot renderer, playback controls, worker wrapper, page layout, and project illustrations are local additions.

## Verification

- Chromium browser checks at 320, 360, 390, 768, 1024, 1440, and 1920 pixels: no clipped content or horizontal overflow; local fonts loaded; one H1; RTL layout.
- Desktop and mobile screenshots taken, including individual sections, and visually reviewed.
- Animation progression, pause/resume, offscreen suspension/resumption, live reduced-motion changes, reduced-motion opt-in, no-JavaScript fallback, failed-module fallback, and the no-worker fallback checked.
- Keyboard skip link and every homepage internal link and anchor checked.
- All existing SEO tags and JSON-LD compared with the base commit and found unchanged.
- Mobile layout checked at 200% text size: no clipped text or horizontal overflow.
- A 4× CPU slowdown simulation showed no recurring main-thread long tasks during steady animation after moving calculation into the worker. Startup long tasks remain; this is a local simulation, not a production performance score.
- JavaScript syntax checks and `git diff --check` passed.

Screenshots and machine-readable QA results are stored outside the source checkout in `../arashfooladi-ascii-preview/`. These browser checks emulate viewport sizes; they are not physical-device or cross-browser certification.
