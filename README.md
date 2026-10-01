# Arash Fooladi

Personal website at [arashfooladi.ir](https://arashfooladi.ir/), published from `master` through GitHub Pages.

Static Persian HTML with shared CSS, locally hosted fonts, project pages and a journal. No JavaScript framework or build dependency is needed to serve the website.

- Edit each page's HTML for visible content.
- Run `python scripts/refresh_seo.py` after updating search metadata.
- Run `python scripts/generate_social_images.py` after changing share titles or descriptions (Chrome and Python Playwright required for this optional authoring step).
- Preview locally with `python -m http.server 8000`.

See [SEO.md](SEO.md) for metadata maintenance and the remaining Cloudflare/Search Console setup.

Open source and MIT licensed. Bundled font licenses are included in `assets/fonts/`.
