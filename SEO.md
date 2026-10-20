

The site serves complete static HTML. Existing project and article URLs are preserved.
The projects archive is `/projects/`; Persian remains the only published locale.

## Editing

1. Edit the visible HTML content. Article headlines live in the page's `h1`.
2. Update `PAGE_COPY` in `scripts/refresh_seo.py` for homepage, archive and project search titles and descriptions. Journal metadata uses the article's existing title and description.
3. Set `PAGE_MODIFIED` entries to the actual modification date for the pages you changed. Leave dates for untouched pages and the historical `MODIFIED` fallback unchanged; do not change dates just to make content look fresh.
4. Run `python scripts/refresh_seo.py`.
5. Run `python scripts/generate_social_images.py` to update the 1200 × 630 share previews after title or summary changes. This optional authoring script needs Chrome and the Python `playwright` package; the website itself has no runtime dependencies.

The refresh script maintains a single connected JSON-LD graph per page, canonical metadata, Open Graph, Twitter previews, breadcrumbs, sitemap and RSS titles. It preserves publication dates, verification tags and redirect pages. New canonical HTML pages are discovered automatically.

`PROJECTS_BY_PAGE` controls the project list in structured data. Keep its entries in the same order as the project cards visible on each page, and include only projects actually shown there.

Fonts are served locally with their OFL licenses in `assets/fonts/`.
Social previews are static title cards, not screenshots or fabricated project visuals.

## Validation on 2026-10-20

Homepage store cards now link directly to their case studies. The introduction summarizes existing project descriptions, and the archive identifies Yarplus as a stopped prototype with payments not implemented. Project list structured data matches the visible cards on each page, including their order and count. Only the two edited pages have new modification dates; article publication dates are unchanged.

Checks passed for all 14 canonical pages, 433 local links/assets/fragments, metadata, structured data, sitemap coverage and dates, RSS parsing, and repeatable SEO generation. Chromium checks of the homepage and projects archive passed at 360, 768 and 1440 pixels, including navigation, overflow, assets and browser errors. The projects share image was regenerated at 1200 × 630. These checks do not measure search rankings or production Core Web Vitals.

## Validation on 2026-10-01

Local mobile Lighthouse audits (these are lab checks, not production field data):

| Template | Performance | Accessibility | Best practices | SEO |
| --- | --- | --- | --- | --- |
| Homepage | 97 | 100 | 100 | 100 |
| Daruham project | Not measured | 100 | 100 | 100 |
| AI journal article | Not measured | 100 | 100 | 100 |

All 12 indexable pages were checked at 360, 768 and 1440 pixels for layout and missing assets. Checks also covered unique titles/descriptions, JSON-LD references, breadcrumbs, article authors/dates, canonical sitemap coverage, local links and share image dimensions. The SEO refresh was checked for repeatability.

The homepage project list measured 629 pixels high at the desktop viewport. Yarplus screenshots now use lossless WebP with PNG fallbacks; decoded pixels were checked against the originals.

## Hosting follow-up

An audit on 2026-10-01 found both `http://arashfooladi.ir/` and `https://arashfooladi.ir/` responding with HTTP 200 through Cloudflare. All canonical URLs and internal references use HTTPS, but a permanent redirect should also be configured at the edge.

- In Cloudflare, verify the SSL mode and the origin certificate first. Enable an HTTP-to-HTTPS edge redirect (301 or 308) for this domain.
- Redirect `/index.html` to `/`, and each `/<path>/index.html` to `/<path>/`, while preserving query strings. These are server redirects; GitHub Pages HTML cannot emit HTTP redirect status codes.
- Verify the `www` hostname resolves before redirecting it to the apex domain. Do not assume its DNS is configured.
- Submit `https://arashfooladi.ir/sitemap.xml` in the existing Google Search Console property. The Google verification meta tag is retained.

Changing GitHub Pages HTTPS enforcement without checking Cloudflare's origin connection can introduce a redirect loop. The repository update does not change these hosting settings.

Google documentation: [canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [article markup](https://developers.google.com/search/docs/appearance/structured-data/article).

These changes improve crawlability and page descriptions. Indexing, rich results and search rankings remain Google's decisions.
