# ASCII portfolio — local review

The redesign lives on `design/ascii-home`, based on public `master` commit `d8240fb`. It has not been pushed or deployed. The source remains static HTML, CSS, and JavaScript and is compatible with the existing GitHub Pages hosting configuration.

## Scope and presentation

All 18 HTML pages have been refreshed: the homepage, project archive, five case studies, journal archive, five articles, the error page, one legacy project page, and three redirect fallback pages. Existing search metadata, canonical URLs, Open Graph, Twitter cards, and JSON-LD are preserved. The ten article and case-study bodies retain their original text. Published routes, redirects, sitemap, robots file, feed, and hosting settings remain unchanged.

Cloud Sea fills the homepage opening. The original logo replaces the header name; the marked hero links and credits strip have been removed. Below it, actual Yarplus imagery, a backend project, and concise store rows present the work. The journal opens with a blue Night Coast scene and lighthouse, with a stronger dark gradient behind the title and subtitle. The projects archive opens with Edge Orbit. Shared dark surfaces, locally hosted Vazirmatn typography, restrained spacing, and desktop article contents links connect the remaining pages.

The homepage archive links are prominent light buttons, and the journal introduction makes the additional articles clear. The unfinished-work tagline and footer GitHub, Telegram, RSS, and playback links have been removed. Three community illustrations are used sparingly: an abstract crosshatch interlude after the homepage projects, birds at its footer, and a squirrel near the end of the Yarplus case study. No suitable Telegram ASCII icon was found in the selected gallery, so none was added.

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

Small illustrations load only as their section enters view and play once. Birds begin when the footer enters view, play through the original final empty frame, and then hide. Session storage prevents replay when scrolling back or revisiting the homepage in that tab. A full page reload resets them; browsers do not expose a reliable distinction between normal and cache-bypassing reloads. The texture and squirrel stop on their last frame. All pause offscreen and in hidden tabs. Reduced motion shows static texture/squirrel frames and suppresses bird takeoff. Artist attribution and remix permission details are in `assets/art/CREDITS.md`; these artworks are separate from the editor's MIT license.

## Verification

- Existing SEO metadata compared across all 18 HTML pages; original prose compared across ten articles and case studies.
- All 15 nonredirect pages checked at 320, 390, 768, and 1440 pixels: 60 layouts with no horizontal overflow or clipped text, correct RTL, and loaded fonts.
- Desktop and mobile screenshots captured and visually reviewed across the main layouts.
- Internal links and anchors, unique IDs, heading structure, image loading, JavaScript errors, keyboard skip links, and 200% text zoom checked.
- All three scenes checked for progression, offscreen suspension, live reduced motion, and no-JavaScript posters. The earlier two-scene checks also covered failed-module and no-worker fallbacks.
- Birds checked for footer entry, completion, no replay on scroll or navigation, resize after completion, reset on reload, and suppression with reduced motion. The squirrel checked for lazy loading and one-shot playback.
- JavaScript syntax and Git whitespace checks passed.

Current screenshots and the machine-readable QA report are stored outside the checkout in `../arashfooladi-ascii-preview/refinement/`; the earlier whole-site audit remains in `../arashfooladi-ascii-preview/recreation/`. These are local Chromium viewport checks, not physical-device or cross-browser certification.
