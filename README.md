# Arash Fooladi

Personal website at [arashfooladi.ir](https://arashfooladi.ir/)
Open source and MIT licensed.

This site is a Farsi portfolio and journal built with static HTML, CSS, and JavaScript. It uses locally hosted Vazirmatn fonts, shared dark layouts, and self-hosted ASCII scenes. No build step or npm dependencies are required; the existing GitHub Pages configuration is retained.

Run the preview from this directory:

```powershell
python -m http.server 8814 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8814/`. GitHub Pages publishes the root of `master` to [arashfooladi.ir](https://arashfooladi.ir/).

Check metadata, structured data, local references, sitemap and RSS before publishing:

```sh
python3 scripts/check_seo.py
```

This check uses only the Python standard library. See [SEO.md](SEO.md) for the authoring workflow and latest review.

See [ASCII-HOME.md](ASCII-HOME.md) for the page structure, animation behavior, and verification details, and [ASCII-ART-SOURCES.md](ASCII-ART-SOURCES.md) for additional animation candidates.

Third-party artwork and fonts retain their own terms. See [community artwork credits](assets/art/CREDITS.md) and [VGA font attribution](assets/fonts/LICENSE.ibm-vga.md).
