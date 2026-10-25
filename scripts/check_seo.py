"""Check static SEO metadata and local references without packages or network access.

Run `python3 scripts/check_seo.py` before publishing. This is a local consistency
check, not a search ranking, rich-result eligibility, or production HTTP audit.
"""

from collections import Counter
from datetime import date
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

BASE = 'https://arashfooladi.ir'
ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.route = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
        self.url = BASE + self.route
        self.meta = {}
        self.links = []
        self.refs = []
        self.ids = []
        self.h1 = []
        self.title = ''
        self.lang = None
        self.direction = None
        self.capture = None
        self.json_text = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang, self.direction = attrs.get('lang'), attrs.get('dir')
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property', ''))
            self.meta.setdefault(key, []).append(attrs.get('content', ''))
        if tag == 'link':
            self.links.append(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for field in ('href', 'src', 'poster'):
            if attrs.get(field):
                self.refs.append(attrs[field])
        if attrs.get('srcset'):
            self.refs.extend(item.strip().split()[0] for item in attrs['srcset'].split(','))
        if tag in ('h1', 'title'):
            self.capture = tag
            if tag == 'h1':
                self.h1.append('')
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.capture = 'json'
            self.json_text.append('')

    def handle_data(self, text):
        if self.capture == 'title':
            self.title += text
        elif self.capture == 'h1':
            self.h1[-1] += text
        elif self.capture == 'json':
            self.json_text[-1] += text

    def handle_endtag(self, tag):
        if tag == self.capture or (tag == 'script' and self.capture == 'json'):
            self.capture = None

    def value(self, name):
        return self.meta.get(name, [''])[0]


def main():
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    pages = {path: Page(path) for path in sorted(ROOT.rglob('*.html')) if '.git' not in path.parts}
    indexable = {}
    articles = {}
    page_nodes = {}
    titles, descriptions = [], []
    references = 0
    for path, page in pages.items():
        label = path.relative_to(ROOT).as_posix()
        for identity, count in Counter(page.ids).items():
            check(count == 1, f'{label}: duplicate id {identity!r}')
        for ref in page.refs:
            url = urlsplit(urljoin(page.url, ref))
            if url.scheme not in ('http', 'https') or url.netloc != urlsplit(BASE).netloc:
                continue
            target = (ROOT / unquote(url.path).lstrip('/')).resolve()
            if target.is_dir():
                target /= 'index.html'
            references += 1
            check(target.is_relative_to(ROOT) and target.is_file(), f'{label}: missing local reference {ref}')
            if target in pages and url.fragment:
                check(unquote(url.fragment) in pages[target].ids, f'{label}: missing fragment {ref}')
        if 'noindex' in page.value('robots'):
            continue
        indexable[page.url] = page
        check((page.lang, page.direction) == ('fa', 'rtl'), f'{label}: expected Persian RTL document')
        check(len(page.h1) == 1 and bool(page.h1[0].strip()), f'{label}: expected one nonempty h1')
        check(bool(page.title.strip()), f'{label}: missing title')
        check(bool(page.value('viewport')), f'{label}: missing viewport')
        canonical = [link.get('href') for link in page.links if link.get('rel') == 'canonical']
        check(canonical == [page.url], f'{label}: canonical must be exactly {page.url}')
        check('noindex' not in page.value('robots') and 'index' in page.value('robots'), f'{label}: indexing is not enabled')
        for name in ('description', 'og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt',
                     'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt'):
            check(len(page.meta.get(name, [])) == 1 and bool(page.value(name).strip()), f'{label}: missing or duplicate {name}')
        for name, expected in (('og:title', page.title), ('twitter:title', page.title),
                               ('og:description', page.value('description')), ('twitter:description', page.value('description')),
                               ('og:url', page.url), ('twitter:image', page.value('og:image'))):
            check(page.value(name) == expected, f'{label}: inconsistent {name}')
        image = ROOT / urlsplit(page.value('og:image')).path.lstrip('/')
        if image.is_file():
            data = image.read_bytes()
            check(data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) >= 24
                  and struct.unpack('>II', data[16:24]) == (1200, 630), f'{label}: share image must be a 1200 x 630 PNG')
        else:
            check(False, f'{label}: share image does not exist')
        titles.append(page.title)
        descriptions.append(page.value('description'))
        try:
            check(len(page.json_text) == 1, f'{label}: expected one JSON-LD graph')
            graph = json.loads(page.json_text[0])['@graph']
            nodes = {node['@id']: node for node in graph}
            page_nodes[page.url] = nodes
            entity = nodes[page.url + '#webpage']
            modified = date.fromisoformat(entity['dateModified'])
            check(entity['url'] == page.url, f'{label}: structured-data page URL differs from canonical')
            check(entity['name'] == page.title and entity['description'] == page.value('description'), f'{label}: stale structured-data copy')
            author = nodes[BASE + '/#arash-fooladi']
            check(author['@type'] == 'Person' and author['url'] == BASE + '/', f'{label}: missing author identity')
            article = nodes.get(page.url + '#article')
            if article:
                articles[page.url] = (page, article)
                published = date.fromisoformat(article['datePublished'])
                check(modified >= published, f'{label}: modification date precedes publication')
                check(page.value('article:published_time') == article['datePublished'], f'{label}: publication dates disagree')
                check(page.value('article:modified_time') == entity['dateModified'], f'{label}: modification dates disagree')
                check(article['author']['@id'] in nodes, f'{label}: unresolved author')
                check(article['isPartOf']['@id'] == BASE + '/journal/#blog', f'{label}: missing journal association')
        except (ValueError, KeyError, IndexError, TypeError) as error:
            check(False, f'{label}: invalid or incomplete structured data ({error})')
    for label, values in (('title', titles), ('description', descriptions)):
        for value, count in Counter(values).items():
            check(count == 1, f'Duplicate {label}: {value}')

    sitemap = ET.parse(ROOT / 'sitemap.xml')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    entries = sitemap.findall('s:url', ns)
    urls = [entry.findtext('s:loc', namespaces=ns) for entry in entries]
    check(len(urls) == len(set(urls)), 'Sitemap contains duplicate URLs')
    check(set(urls) == set(indexable), 'Sitemap does not match indexable canonical pages')
    for entry in entries:
        url = entry.findtext('s:loc', namespaces=ns)
        entity = page_nodes.get(url, {}).get(str(url) + '#webpage', {})
        if 'dateModified' in entity:
            modified = entity['dateModified']
            check(entry.findtext('s:lastmod', namespaces=ns) == modified, f'Sitemap date differs for {url}')
    check(f'Sitemap: {BASE}/sitemap.xml' in (ROOT / 'robots.txt').read_text(), 'robots.txt does not advertise the sitemap')

    items = ET.parse(ROOT / 'feed.xml').findall('channel/item')
    feed_urls = [item.findtext('link') for item in items]
    check(len(feed_urls) == len(set(feed_urls)) and set(feed_urls) == set(articles), 'RSS does not cover each published article exactly once')
    for item in items:
        url = item.findtext('link')
        if url in articles:
            page, article = articles[url]
            check(item.findtext('title') == article['headline'], f'RSS title differs for {url}')
            check(item.findtext('description') == page.value('description'), f'RSS description differs for {url}')
            check(parsedate_to_datetime(item.findtext('pubDate')).date().isoformat() == article['datePublished'], f'RSS publication date differs for {url}')
    for path in (ROOT / 'assets/css').rglob('*.css'):
        for ref in re.findall(r'url\([\'\"]?([^\s)\'\"]+)', path.read_text()):
            url = urlsplit(urljoin(BASE + '/' + path.relative_to(ROOT).as_posix(), ref))
            if url.netloc == urlsplit(BASE).netloc:
                check((ROOT / url.path.lstrip('/')).is_file(), f'{path.name}: missing CSS asset {ref}')
    if errors:
        print('\n'.join('FAIL: ' + error for error in errors), file=sys.stderr)
        print(f'{len(errors)} SEO check(s) failed.', file=sys.stderr)
        return 1
    print(f'Passed: {len(indexable)} canonical pages, {references} local references, structured data, share images, sitemap and {len(items)} RSS articles.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
