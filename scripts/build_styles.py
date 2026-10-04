"""Publish immutable CSS filenames and embed the homepage's original theme.

Run after editing assets/css/*.css. Search metadata is left unchanged.
Relative asset paths also support opening HTML files directly for preview.
"""
from pathlib import Path
import hashlib
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets/css"


def build():
    versions = {}
    for name in ("fonts", "site", "projects", "journal"):
        data = (CSS / f"{name}.css").read_bytes()
        digest = hashlib.sha256(data).hexdigest()[:12]
        filename = f"{name}.{digest}.css"
        (CSS / filename).write_bytes(data)
        versions[name] = filename

    paths = subprocess.check_output(
        ["git", "ls-files", "*.html"], cwd=ROOT, text=True
    ).splitlines()
    for filename in paths:
        page = ROOT / filename
        html = page.read_text(encoding="utf-8")
        prefix = "../" * (len(Path(filename).parts) - 1)

        def version(match):
            name = match.group(1)
            return f'href="{prefix}assets/css/{versions[name]}"'

        html = re.sub(
            r'href="(?:/|(?:\.\./)*)(?:assets/css/)(fonts|site|projects|journal)'
            r'(?:\.[0-9a-f]+)?\.css(?:\?[^" ]*)?"',
            version, html,
        )
        if filename == "index.html":
            html = re.sub(
                r'\s*<link\b[^>]*href="[^"]*assets/css/home(?:\.[0-9a-f]+)?\.css[^" ]*"[^>]*>',
                "", html,
            )
            html = re.sub(
                r'\s*<style id="portfolio-theme">.*?</style>', "", html,
                flags=re.S,
            )
            theme = (CSS / "home.css").read_text(encoding="utf-8")
            html = html.replace(
                "</head>", f'<style id="portfolio-theme">\n{theme}</style>\n</head>',
                1,
            )
        page.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
