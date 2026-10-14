# ASCII portfolio — local review

The redesign lives on `design/ascii-home`, based on public `master` commit `d8240fb`. It has not been pushed or deployed. The source remains static HTML, CSS, and JavaScript and is compatible with the existing GitHub Pages hosting configuration.

## Scope and presentation

All 18 HTML pages have been refreshed: the homepage, project archive, five case studies, journal archive, five articles, the error page, one legacy project page, and three redirect fallback pages. Existing search metadata, canonical URLs, Open Graph, Twitter cards, and JSON-LD are preserved. The ten article and case-study bodies retain their original text. Published routes, redirects, sitemap, robots file, feed, and hosting settings remain unchanged.

Cloud Sea fills the homepage opening. The original logo replaces the header name; the marked hero links and credits strip have been removed. Below it, actual Yarplus imagery, a backend project, and concise store rows present the work. The journal opens with a blue Night Coast scene and lighthouse. Shared dark surfaces, locally hosted Vazirmatn typography, restrained spacing, and desktop article contents links connect the remaining pages.

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
- `assets/js/vendor/` — the two scene generators and their MIT license.
- `ASCII-ART-SOURCES.md` — smaller animation suggestions, awaiting selection.

## Animation

Both scenes are self-hosted, with no npm installation or external runtime request. A module worker calculates and, where OffscreenCanvas is supported, renders at up to 12 frames per second. Fallback rendering supports browsers without workers. Scenes pause offscreen and when the browser tab is hidden. Playback controls live in the footer, outside the opening artwork. Reduced-motion visitors initially receive a static WebP poster and can explicitly opt into motion. The poster also works without JavaScript or when a scene module cannot load.

Sources: [Cloud Sea](https://ascii.rest/cloud-sea/) and [Night Coast](https://ascii.rest/night-coast/) by [bas3line](https://github.com/bas3line/ascii). Their attribution and MIT license are retained in the vendor directory. The dot renderer, worker wrapper, controls, and layout are local additions.

## Verification

- Existing SEO metadata compared across all 18 HTML pages; original prose compared across ten articles and case studies.
- All 15 nonredirect pages checked at 320, 390, 768, and 1440 pixels: 60 layouts with no horizontal overflow or clipped text, correct RTL, and loaded fonts.
- Desktop and mobile screenshots captured and visually reviewed across the main layouts.
- Internal links and anchors, unique IDs, heading structure, image loading, JavaScript errors, keyboard skip links, and 200% text zoom checked.
- Both scenes checked for progression, pause/resume, offscreen suspension, reduced-motion changes and opt-in, no-JavaScript fallback, and failed-module fallback.
- JavaScript syntax and Git whitespace checks passed.

Screenshots and the machine-readable QA report are stored outside the checkout in `../arashfooladi-ascii-preview/recreation/`. These are local Chromium viewport checks, not physical-device or cross-browser certification.
