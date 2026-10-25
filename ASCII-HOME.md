# ASCII portfolio

The redesign was developed on `design/ascii-home`, based on public `master` commit `d8240fb`. GitHub Pages publishes the root of `master` to https://arashfooladi.ir/. The source remains static HTML, CSS, and JavaScript and is compatible with the existing GitHub Pages hosting configuration.

## Scope and presentation

All 18 HTML pages have been refreshed: the homepage, project archive, five case studies, journal archive, five articles, the error page, one legacy project page, and three redirect fallback pages. Existing search metadata, canonical URLs, Open Graph, Twitter cards, and JSON-LD are preserved. The ten article and case-study bodies retain their original text. Published routes, redirects, sitemap, robots file, feed, and hosting settings remain unchanged.

Cloud Sea fills the homepage opening. The original logo replaces the header name; the marked hero links and credits strip have been removed. The homepage features the Telegram backend project, followed by three compact store listings that link to the full projects archive. Yarplus appears in the projects archive and its own case study. The journal opens with a blue Night Coast scene and lighthouse, with a stronger dark gradient behind the title and subtitle. The projects archive opens with Edge Orbit. Shared dark surfaces, locally hosted Vazirmatn typography, restrained spacing, and desktop article contents links connect the remaining pages.

The homepage archive buttons sit below their content with 64 pixels of separation on desktop and 48 on mobile. Their counts indicate four other case studies beyond the featured Telegram project, and three articles beyond the two homepage previews. The unfinished-work tagline is replaced with concise Persian copy. All six original social profiles are restored in the footer; the homepage has one Telegram action in its contact section, with a compact ASCII rendering of the official logo above the bird animation. Other pages include Telegram alongside the six social profiles. RSS and playback controls remain removed.

Mobile name and role text receive a stronger dark backdrop, brighter text, and deliberate font weights. The mobile role is 16 pixels. Homepage section borders are replaced by spacing below 600 pixels; desktop separators remain. A real world-map character animation replaces the abstract strip below the projects, while the original birds and Yarplus case-study squirrel remain.

## Preview

From this checkout, run:

```powershell
python -m http.server 8814 --bind 127.0.0.1
```

Open `http://127.0.0.1:8814/`, `/projects/`, or `/journal/`. Stop the preview with Ctrl+C. Use an HTTP preview so the JavaScript modules can load.

## Source layout

- `index.html` — homepage content.
- `projects/`, individual project directories, and `journal/` — archives, case studies, and articles.
- `assets/css/site.css` — shared navigation, typography, reading layouts, and footer.
- `assets/css/home.css`, `projects.css`, and `journal.css` — page-specific layouts.
- `assets/css/scenes.css` — shared fullscreen openings.
- `assets/js/home.js`, `scene-worker.js`, and `sea-renderer.js` — scene loading, rendering, and playback.
- `assets/js/vendor/` — the three scene generators and their MIT license.
- `assets/css/accents.css`, `assets/js/accents.js`, and `assets/art/` — curated small animations, compact frame data, and artist credits.
- `ASCII-ART-SOURCES.md` — scene and community artwork sources.

## Animation

All three scenes are self-hosted, with no npm installation or external runtime request. A module worker calculates and, where OffscreenCanvas is supported, renders at up to 12 frames per second. Fallback rendering supports browsers without workers. Scenes pause offscreen and when the browser tab is hidden. Reduced-motion visitors receive a static WebP poster. The poster also works without JavaScript or when a scene module cannot load.

Sources: [Cloud Sea](https://ascii.rest/cloud-sea/), [Night Coast](https://ascii.rest/night-coast/), and [Edge Orbit](https://ascii.rest/edge-orbit/) by [bas3line](https://github.com/bas3line/ascii). Their attribution and MIT license are retained in the vendor directory. The dot renderer, worker wrapper, and layout are local additions.

The map and squirrel load as their section enters view and play once. Birds prepare their artwork and IBM VGA font in parallel when the footer comes within 800 pixels of the viewport, then begin only when the footer enters view, play through the original final empty frame, and hide. Preparing the birds does not mark them as played; reduced-motion visitors skip these bird downloads. The original first-frame perch duration is preserved. Session storage prevents replay when scrolling back or revisiting the homepage in that tab. A full page reload resets them; browsers do not expose a reliable distinction between normal and cache-bypassing reloads. The world map and squirrel stop on their last frame. All pause offscreen and in hidden tabs. Reduced motion shows static map/squirrel frames and suppresses bird takeoff. Artist attribution and source details are in `assets/art/CREDITS.md`. The inline Telegram character icon works without JavaScript and has a brief lift on hover/focus, suppressed with reduced motion.

## Verification

- Existing SEO metadata compared across all 18 HTML pages; original prose compared across ten articles and case studies.
- All 15 nonredirect pages checked at 320, 390, 768, and 1440 pixels: 60 layouts with no horizontal overflow or clipped text, correct RTL, and loaded fonts.
- Desktop and mobile screenshots captured and visually reviewed across the main layouts.
- Internal links and anchors, unique IDs, heading structure, image loading, JavaScript errors, keyboard skip links, and 200% text zoom checked.
- All three scenes checked for progression, offscreen suspension, live reduced motion, and no-JavaScript posters. The earlier two-scene checks also covered failed-module and no-worker fallbacks.
- Birds checked for footer entry, completion, no replay on scroll or navigation, resize after completion, reset on reload, and suppression with reduced motion. The squirrel checked for lazy loading and one-shot playback.
- Bird loading checked with 400 ms delays on both artwork and font requests: preparing them near the footer reduced the measured wait on entry from about 870 ms to 30 ms. Checks also covered concurrent downloads, fast scrolling away during loading, reduced-motion changes, static map/squirrel rendering and failed artwork requests.
- JavaScript syntax and Git whitespace checks passed.

Current homepage screenshots and QA results are stored in `../arashfooladi-ascii-preview/home-final/`, covering 320, 360, 390, 430, 768, and 1440 pixels, including live art and 200% text zoom. The restored shared footer was checked across all 15 nonredirect pages at mobile/desktop widths in `../arashfooladi-ascii-preview/mobile-revision/`. Earlier whole-site audits remain in `../arashfooladi-ascii-preview/refinement/` and `recreation/`. These are local Chromium viewport checks, not physical-device or cross-browser certification.
