# SEO and publishing

The site serves Persian RTL HTML directly from GitHub Pages. Project case studies, collaboration pages under `/services/`, and the journal have their own roles and share the existing styles.

## Editing

1. Edit the visible HTML. Keep the search title and description in the page's `<title>` and `<meta name="description">`.
2. Record the date of substantive edits to hand-written HTML in `PAGE_MODIFIED` in `scripts/refresh_seo.py`. Markdown notes carry their dates in the source file.
3. Run `python scripts/refresh_seo.py` to regenerate social metadata, JSON-LD, journal listings, sitemap and RSS.
4. For a changed search title or description, optionally regenerate its title card with `python scripts/generate_social_images.py --route /example/`. This tool uses Chromium and Python Playwright. Run the refresh again if you create a dedicated card for a Markdown note.
5. Run `python scripts/check_seo.py` and preview with `python -m http.server 8814 --bind 127.0.0.1`.

`PROJECTS_BY_PAGE` controls the project list in structured data. Keep its entries in the visible card order. `PROJECT_VISUALS` maps each visual case study to the actual primary screenshot and its dimensions. Social previews use separate 1200 × 630 title cards.

## Publish a journal note

Install the Markdown parser in a local virtual environment once. The generated site still runs as static files.

```sh
python -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-journal.txt
```

Save a finished note at `journal/_posts/your-note-slug.md`. The filename becomes `/journal/your-note-slug/`. Keep private drafts outside that directory. Write the note in Markdown after the second `---` line. Start body headings at `##`.

```text
---
title: <عنوان نوشته>
description: <خلاصهٔ کوتاه نوشته>
date: YYYY-MM-DD
date-label: <تاریخ شمسی دلخواه>
category: personal
---
```

`date` and the optional `modified` use Gregorian ISO dates. `date-label` is optional and can supply a Persian calendar display date. Category values are `software`, `ai`, `hardware`, `gaming`, `music`, and `personal`. Rust fits under `gaming`. Metal, Buckethead, and electric guitar fit under `music`. The journal lists topics that have published notes.

```sh
.venv/bin/python scripts/refresh_seo.py
.venv/bin/python scripts/check_seo.py
```

Review the generated HTML, homepage and journal listings, sitemap, and RSS before committing those files with the source note. Each existing HTML article keeps its current URL and text. A new Markdown note uses the shared journal preview until it has a dedicated title card.

## Search and growth plan

Persian search results reviewed in November 2026 suggest the following long-tail intents. Use the queries that actually surface in Search Console to decide which explanations to expand.

| Search intent | Example queries | Where it belongs |
| --- | --- | --- |
| Commission a site or estimate scope | طراحی سایت اختصاصی برای معرفی خدمات، هزینه طراحی سایت با قالب اختصاصی | [Custom websites](services/custom-website/index.html) |
| Choose an online store approach | طراحی سایت فروشگاهی با ووکامرس، طراحی فروشگاه با قالب اختصاصی، هزینه ساخت فروشگاه اینترنتی | [E-commerce](services/ecommerce/index.html) and the relevant store case study |
| Commission a bot | طراحی ربات تلگرام اختصاصی، ساخت ربات تلگرام برای ثبت درخواست | [Telegram bots](services/telegram-bot/index.html) and the infrastructure case study |
| Learn how to implement a bot | ساخت ربات تلگرام با پایتون، استفاده از وب‌هوک تلگرام | A future hands-on journal note when there is original code or implementation experience to share |
| Commission a web app | طراحی وب‌اپلیکیشن اختصاصی، ساخت پنل وب برای پیگیری درخواست، توسعه نرم‌افزار تحت وب | [Web applications](services/web-app/index.html) and the Yarplus case study |

Observed examples include scope and price pages, bot commissioning pages, and a separate Python tutorial intent. [Website pricing example](https://irantarah.com/services/web-design/pricing/) · [Web application scope example](https://lumosagency.org/services/web-app) · [Bot service example](https://rahkarstudio.ir/services/telegram-bot/) · [Python tutorial example](https://taha-heidaryfard.ir/blog/python/telegram-bot)

- After publishing, submit the sitemap and inspect the five new URLs. Compare consecutive 28-day windows in Search Console, starting with the service paths and an Iran segment where the sample supports it. Use the non-branded filter when available or exclude variations of آرش فولادی, Arash Fooladi, the domain and project names with a query regex. Track impressions, new relevant queries, clicks and genuine project inquiries received through Telegram. Keep a small tally of inquiries that mention search or a specific service page. Review query and page pairs before changing titles or copy. [Search Console reports](https://developers.google.com/search/docs/monitor-debug/search-console-start) · [Branded-query filter](https://developers.google.com/search/blog/2025/11/search-console-branded-filter)
- Ask clients such as Gandi Shiraz, Daruham or Computer Melli whether an existing credits, about or launch page could link to the matching case study. A contextual credit is useful when it explains who built the work.
- Write from work already done. Possible subjects include how Computer Melli handles Persian digits in filters, how delivery rules affect a Next.js product page in GameSage, and a small Python bot example with polling versus webhooks if you build it yourself.
- Publish reusable code that you own, with an example, license and README linking to the corresponding explanation. The public portfolio source and Yarplus are natural starting points for linking code to a real case study.
- Participate where an answer or example fits an existing discussion. Share the relevant article when it answers the question. [Persian Python community on Virgool](https://virgool.io/python-community) · [Quera on Virgool](https://virgool.io/@Quera)

## SEO update on 2026-11-27

The collaboration pages link to actual work, and the six project pages link back to the relevant collaboration page. The journal retains its chronological archive and shows a compact list of topics with published notes. The homepage verification tag, case study URLs, article URLs, legacy aliases, and seven published notes are retained.

Chromium ran desktop and mobile checks of the 21 canonical pages and extra narrow checks of the five new pages. The service links, mobile table of contents, journal category links, redirects, and three animated scenes were exercised. A temp-copy Markdown note verified generation of the article, journal and homepage entries, structured data, sitemap, and RSS.

| Asset served in the mobile preview | Before | After |
| --- | ---: | ---: |
| Homepage scene poster | 161 kB | 109 kB |
| Projects scene poster | 85 kB | 53 kB |
| Journal scene poster | 420 kB | 318 kB |
| Yarplus thumbnail in Projects | 695 kB | 24 kB |

The poster dimensions are unchanged. The project archive uses a responsive thumbnail and the case study keeps its full-size image. Local LCP readings varied across runs. Use Search Console for field Core Web Vitals after deployment.

## Screenshot refresh on 2026-11-02

GameSage and Computer Melli have fresh public-homepage captures in desktop and mobile sizes. The project pages, homepage and project archive reference dated WebP filenames so cached older images do not mask the update. Capture captions and modification dates were updated only for the affected pages, along with the primary-image structured data and sitemap. The earlier image files remain available for existing direct links. Project descriptions, layout, social title cards and journal content are unchanged.

## Project showcases on 2026-10-28

All six project pages now present the work as showcases: a short introduction, prominent visuals or existing project metrics, three concise highlights, a compact technology summary and links to more work. Existing canonical URLs and section anchors are preserved. Yarplus remains explicitly identified as a stopped prototype with payments not implemented; no new business or performance metrics were added.

Computer Melli was verified live at `https://computermelli.com/` with an HTTP 200 response. Its showcase, homepage listing, archive listing, metadata and share preview no longer identify it as inactive. Its public-site link is restored. The implementation summary was checked against the theme source and public storefront.

Real public desktop screenshots of Computer Melli, Gandi Shiraz and Daruham, plus mobile screenshots of all four active stores, were captured on 2026-10-28 and saved locally as WebP images. GameSage's existing desktop capture and Yarplus's existing prototype images are retained. The archive's three additional store entries now have screenshot cards. Screenshot dimensions are reflected in project structured data; social cards remain separately generated title cards.

Validation passed for 16 canonical pages, 481 local references, structured data, social images, sitemap and seven RSS articles. Chromium checks passed for all six showcases, the homepage and projects archive at 360, 768 and 1440 pixels (24 layouts), including image loading, overflow, navigation, Computer Melli's live-site link and the Yarplus status text. All six showcases remain readable without JavaScript. Existing journal pages and RSS are unchanged.

## GameSage addition on 2026-10-28

Added `/gamesage/` with a Persian project description grounded in the live storefront and the reviewed source snapshot. The page covers the catalog, order and delivery states, payment implementation, management tools and technical stack. It makes no traffic, sales, performance or security certification claims. Private source repositories are not linked from the public page.

The storefront screenshot was captured from the public homepage on 2026-10-28 and saved as a local 1440 × 1050 WebP. Its caption records that date. The homepage and projects archive feature the new project; the archive now contains six projects. Project lists, metadata, share previews and sitemap were updated together. Modification dates changed only for the homepage, projects archive and new project page; existing articles and RSS were unchanged.

Validation passed for 16 canonical pages, 500 local references, structured data, share images, sitemap and seven RSS articles. The SEO check now verifies project list order and counts against visible cards. SEO generation was checked for repeatability. Chromium checks passed at 360, 768 and 1440 pixels for the homepage, projects archive and GameSage page, including navigation, screenshot loading, breadcrumbs, anchors, overflow and browser errors. The new project remains readable without JavaScript.

## Review on 2026-10-25

The local review found the existing crawlability basics in good shape: 14 indexable pages have unique titles and descriptions, self-referencing HTTPS canonicals, connected JSON-LD and sitemap entries. Five other HTML pages are deliberately excluded from indexing: three legacy redirects, the unfinished project page and the error page. All 436 local HTML references, including image source sets and fragments, resolve.

The review made these changes:

- Decorative hero posters on the homepage and both archives now use low fetch priority and asynchronous decoding. The main heading was the homepage's measured largest contentful element, so decorative downloads should yield to content resources. Posters still load eagerly and remain available without JavaScript and with reduced motion.
- Social cards identify the existing public X account. The homepage's image description now states the name and role instead of repeating the name.
- Each article's structured data explicitly identifies the journal it belongs to. Existing URLs, article copy, publication dates and modification dates are preserved.
- `scripts/check_seo.py` provides repeatable, read-only checks. Its failure behavior was verified against broken canonicals, missing links, invalid structured data and incorrect sitemap coverage in temporary copies.

Local mobile Lighthouse 13.0.1 runs in Chromium, served by Python's HTTP server:

| Check | Before | After |
| --- | --- | --- |
| Performance | 92 | 97 |
| Accessibility | 100 | 100 |
| Best practices | 100 | 100 |
| SEO | 100 | 100 |
| Largest Contentful Paint | 3.2 s | 2.3 s |

These are individual lab runs under simulated mobile conditions; scores vary and do not establish production Core Web Vitals or a ranking improvement. Remaining image-compression opportunities should be evaluated with visual review. Cache lifetimes and compression warnings from Python's development server do not establish a problem with the production host.

Chromium checks passed for all 15 nonredirect, nonplaceholder pages at 360, 768 and 1440 pixels: 45 layouts with no horizontal overflow, JavaScript errors or failed asset requests. All images and fonts loaded. Homepage and archive scene workers ran, all three posters remained visible with JavaScript disabled and with reduced motion, and navigation from the homepage through the journal archive to an article worked. SEO generation remained repeatable, and optional social-image generation produced a 1200 × 630 card in a temporary copy.

Production HTTP status, HTTPS enforcement, host redirects, search indexing and Search Console data were not verified in this review. The cloud environment's outbound policy blocked access to `arashfooladi.ir`; the proxy's 403 response was not a response from the website. Recheck the hosting follow-up below against production before changing Cloudflare or GitHub Pages settings.

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

A production check on 2026-11-27 found the apex HTTP URL, `/index.html`, and `/journal/index.html` serving duplicate content with HTTP 200. The GitHub Pages host redirected to the HTTP apex. The `www` host failed hostname certificate verification. The site advertises HTTPS directory URLs in its canonical tags, internal links, and sitemap.

- Verify the Cloudflare TLS mode and origin certificate. Then redirect the HTTP apex to HTTPS and verify the GitHub Pages host ultimately lands on the HTTPS apex.
- Redirect the explicit `index.html` forms to their corresponding directory URLs while preserving query strings.
- Provision a valid certificate for `www` before redirecting that hostname to the apex.
- Recheck the status codes on the legacy aliases after any edge rule change. They currently use static HTML refreshes and canonical targets.

Google documentation: [canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [article markup](https://developers.google.com/search/docs/appearance/structured-data/article).

These changes improve crawlability and page descriptions. Indexing, rich results and search rankings remain Google's decisions.
