---
name: seo-fix-static-site
description: Diagnose and fix common SEO issues on static HTML sites using Google Search Console reports
source: auto-skill
extracted_at: '2026-05-29T14:13:18.211Z'
---

# SEO Fix — Static Site

Diagnose and fix SEO issues on static (non-CMS) HTML sites by mapping Google Search Console (GSC) report categories to root causes and applying targeted fixes.

## GSC Report → Root Cause Map

### "Not found (404)"

**Diagnosis:**
- Check if the URL has a corresponding `index.html` in a matching subdirectory
- Check if `hreflang` points to a URL that doesn't exist (e.g., `hreflang="fa"` pointing to `/fa/` with no page)

**Fix:**
- If the URL should exist: create the directory + `index.html`
- If it was removed: create a redirect page at the old URL with canonical pointing to the new location + `<meta http-equiv="refresh">` + JS redirect
- Update `hreflang` references across all pages to point to the correct existing URL

### "Alternate page with proper canonical tag"

**Diagnosis:**
- Means Google sees two URLs serving identical content (e.g., `/index.html` and `/`)
- Check for mismatches between `og:url` and `link rel="canonical"`
- Check if canonical URLs are missing trailing slashes while the server also serves the slash version

**Fix:**
- Add `robots.txt` with `Disallow: /*.html$` to prevent `.html` variant crawling
- Ensure all canonical URLs end with trailing slashes for directory-style paths
- Make `og:url` exactly match the canonical URL across every page
- Add proper `hreflang` self-references on every page

### "Crawled — currently not indexed"

**Diagnosis:**
- Page has thin or placeholder content (e.g., "Coming Soon", "Under Construction")
- Google sees the page but chooses not to waste index budget on it

**Fix:**
- Option A (preferred for placeholder pages): Change `robots` to `noindex, follow` — cleaner than being indexed with a warning
- Option B: Add substantial, unique content (500+ words of real substance)
- Never leave thin pages with `index, follow` — it signals low-quality to Google

### "Page with redirect"

**Diagnosis:**
- Check for `<base target="_blank">` in `<head>` — this makes ALL links (including relative navigation) open in new tabs, which Googlebot can interpret as redirect behavior
- Check for mismatched canonical vs actual URL (redirect loop appearance)

**Fix:**
- Remove `<base target="_blank">` from all pages — add `target="_blank"` selectively to external links instead
- Ensure canonical URLs use consistent trailing slashes
- Add `hreflang` alternate tags to all subpages (not just the homepage)

## Mandatory Files to Create/Update

### `robots.txt` (root)

```
User-agent: *
Allow: /
Disallow: /*.html$
Sitemap: https://yoursite.com/sitemap.xml
```

### `sitemap.xml` (root)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://yoursite.com/</loc>
    <lastmod>YYYY-MM-DD</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://yoursite.com/"/>
    <xhtml:link rel="alternate" hreflang="fa" href="https://yoursite.com/fa/"/>
  </url>
  <!-- One <url> block per indexable page -->
</urlset>
```

Key rules:
- Every URL in the sitemap must end with `/` for directory-style paths
- Include `hreflang` alternates inside each `<url>` block
- Do NOT include `noindex` pages (they shouldn't be in the sitemap)

## Canonical & Hreflang Checklist (every page)

Every HTML page must have:
1. `<link rel="canonical" href="https://yoursite.com/path/">` (trailing slash)
2. `<link rel="alternate" hreflang="en" href="...">` (self and cross-lang)
3. `<meta property="og:url" content="...">` (must match canonical exactly)
4. No `<base target="_blank">` in `<head>`
5. All `hreflang` values must use full absolute URLs with trailing slashes

## Trailing Slash Consistency Rule

Pick one convention and enforce it everywhere. For static sites with directory-based routing (`/path/index.html`):
- **Always** use trailing slashes in canonical URLs, `og:url`, `hreflang`, and sitemap
- Links inside HTML body (`<a href>`) can stay as relative paths (these resolve the same way)
- Never mix `/path` and `/path/` in canonical/og/sitemap — they are different URLs to Google

## Debugging Commands

```bash
# Find all canonical tags
grep -r "rel=\"canonical\"" .

# Find all og:url tags
grep -r "og:url" .

# Find <base> tags (should not exist)
grep -r "<base " .

# Find .html links in internal navigation
grep -r "href.*\.html" .

# Find all hreflang tags
grep -r "hreflang" .
```
