"""Render published Markdown notes and update the HTML journal listings."""

from datetime import date
from html import escape, unescape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / 'journal'
AUTHOR = 'آرش فولادی'
BASE = 'https://arashfooladi.ir'
TOPICS = {
    'software': 'نرم‌افزار',
    'ai': 'هوش مصنوعی',
    'hardware': 'فناوری و سخت‌افزار',
    'gaming': 'بازی',
    'music': 'موسیقی و گیتار',
    'personal': 'یادداشت‌های شخصی',
}
LEGACY_TOPICS = {
    'async-search-race-conditions': 'software',
    'yarplus-idealist': 'software',
    'cli-tools-i-use': 'software',
    'payment-system-under-sanctions': 'software',
    'microservices-solo-project': 'software',
    'sonnet-5-5-opus-5-5-gpt-6-1-sol': 'ai',
    'ai-pair-programmer': 'ai',
}
LEGACY_EXCERPTS = {
    'async-search-race-conditions': 'چرا نتیجه جست‌وجوی قبلی جای نتیجه جدید می‌نشیند؟ یک مثال جاوااسکریپت با لغو درخواست و کنترل پاسخ‌های دیررس.',
    'yarplus-idealist': 'روایت نمونه اولیه یارپلاس، حضور در رقابت و شایسته تقدیر شدن؛ با نگاهی به جایی که پروژه متوقف شد.',
    'sonnet-5-5-opus-5-5-gpt-6-1-sol': 'سونت را باحوصله‌تر می‌دانم؛ Sol گاهی با وجود توانایی‌اش به ساده‌ترین راه‌حل بسنده می‌کند.',
    'cli-tools-i-use': 'Reasonix، Codex و OpenCode؛ چند یادداشت درباره استفاده روزانه، هزینه و انتخاب مدل.',
}
GENERATED = '<!-- Generated from a journal/_posts Markdown file. -->'
PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def plain(markup):
    return unescape(re.sub(r'<[^>]*>', '', markup)).strip()


def topic_link(topic):
    return f'<a href="/journal/#topic-{topic}">{TOPICS[topic]}</a>'


def read_source(source):
    parts = re.split(r'^---[ \t]*\n', source.read_text(encoding='utf-8'), maxsplit=2, flags=re.M)
    if len(parts) != 3 or parts[0]:
        raise ValueError(f'{source.name}: expected metadata between two --- lines')
    fields = {}
    for line in parts[1].splitlines():
        key, separator, value = line.partition(':')
        if not separator or key in fields or not value.strip():
            raise ValueError(f'{source.name}: invalid metadata line {line!r}')
        fields[key] = value.strip()
    required = {'title', 'description', 'date', 'category'}
    optional = {'date-label', 'modified'}
    if not required <= fields.keys() or fields.keys() - required - optional:
        raise ValueError(f'{source.name}: use title, description, date, category, and optional date-label or modified')
    if fields['category'] not in TOPICS:
        raise ValueError(f'{source.name}: choose a category from {", ".join(TOPICS)}')
    for key in ('date', 'modified'):
        if key in fields and date.fromisoformat(fields[key]).isoformat() != fields[key]:
            raise ValueError(f'{source.name}: {key} must use YYYY-MM-DD')
    if fields.get('modified', fields['date']) < fields['date']:
        raise ValueError(f'{source.name}: modified precedes publication')
    if not parts[2].strip():
        raise ValueError(f'{source.name}: missing article body')
    return fields, parts[2]


def render_sources():
    sources = sorted((JOURNAL / '_posts').glob('*.md'))
    targets = {JOURNAL / source.stem / 'index.html' for source in sources}
    for path in JOURNAL.glob('*/index.html'):
        if path not in targets and GENERATED in path.read_text(encoding='utf-8'):
            raise ValueError(f'{path.relative_to(ROOT)} has lost its Markdown source. Restore it or explicitly remove the generated page.')

    if not sources:
        return {}
    try:
        from markdown_it import MarkdownIt
    except ImportError as error:
        raise SystemExit('Install the Markdown authoring dependency with pip install -r scripts/requirements-journal.txt.') from error

    parser = MarkdownIt('commonmark', {'html': False})
    archive = (JOURNAL / 'index.html').read_text(encoding='utf-8')
    header = re.search(r'<header class="site-header">.*?</header>', archive, re.S)[0]
    footer = re.search(r'<footer class="site-footer">.*?</footer>', archive, re.S)[0]
    rendered = {}
    metadata = {}
    for source in sources:
        slug = source.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError(f'{source.name}: use a lowercase, hyphenated URL slug')
        target = JOURNAL / slug / 'index.html'
        if target.exists() and GENERATED not in target.read_text(encoding='utf-8'):
            raise ValueError(f'{source.name}: this URL already has an existing HTML page')
        fields, markdown = read_source(source)
        route = f'/journal/{slug}/'
        tokens = parser.parse(markdown)
        headings = []
        previous_level = 1
        for i, token in enumerate(tokens):
            if token.type != 'heading_open':
                continue
            level = int(token.tag[1])
            if level < 2 or level > previous_level + 1:
                raise ValueError(f'{source.name}: start headings at ## and do not skip levels')
            previous_level = level
            anchor = f'section-{len(headings) + 1}'
            token.attrSet('id', anchor)
            if level == 2:
                headings.append((anchor, tokens[i + 1].content))
            else:
                token.attrSet('id', f'subsection-{i}')
        body = parser.renderer.render(tokens, parser.options, {})
        toc = ''
        if headings:
            links = ''.join(f'<li><a href="#{anchor}">{escape(label)}</a></li>' for anchor, label in headings)
            toc = f'<aside class="reading-sidebar"><nav aria-label="فهرست صفحه"><details class="page-contents" open><summary>در این صفحه</summary><ul>{links}</ul></details></nav></aside>'

        title = escape(fields['title'])
        description = escape(fields['description'], quote=True)
        published = fields['date']
        date_label = escape(fields.get('date-label', published.translate(PERSIAN_DIGITS) + ' میلادی'))
        rendered[target] = f'''<!doctype html>
{GENERATED}
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | {AUTHOR}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{BASE}{route}">
  <link rel="stylesheet" href="/assets/css/fonts.css?v=ascii-20261015">
  <link rel="stylesheet" href="/assets/css/site.css?v=review-20261104">
  <link rel="stylesheet" href="/assets/css/journal.css?v=topics-20261127">
</head>
<body class="note-page">
<a class="skip-link" href="#article">رفتن به متن نوشته</a>
{header}
<main>
  <header class="page-heading note-heading">
    <div class="reading-container">
      <!-- BREADCRUMBS -->
      <h1>{title}</h1>
      <div class="article-meta">
        <a href="/#about" rel="author">نوشته {AUTHOR}</a>
        <span>تاریخ انتشار: <time datetime="{published}">{date_label}</time></span>
        {topic_link(fields['category'])}
      </div>
    </div>
  </header>
  <div class="container reading-layout note-layout">
    {toc or '<div></div>'}
    <article class="prose note-copy" id="article" tabindex="-1">
{body.rstrip()}
      <nav class="article-nav" aria-label="نوشته‌های مرتبط">
        <a href="/journal/">→ همه نوشته‌ها</a>
      </nav>
    </article>
  </div>
</main>
{footer}
<script type="module" src="/assets/js/reading.js?v=review-20261104"></script>
</body>
</html>
'''
        metadata[route] = fields
    for target, content in rendered.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    return metadata


def note_link(article, featured):
    excerpt = f'<p>{escape(article["excerpt"])}</p>' if article['excerpt'] else ''
    classes = 'journal-link featured-note' if featured else 'journal-link'
    return (
        f'<li><a class="{classes}" href="{article["route"]}">'
        f'<span class="journal-date"><time datetime="{article["published"]}">{escape(article["date_label"])}</time></span>'
        f'<div><h3>{escape(article["headline"])}</h3>{excerpt}</div>'
        '<span class="journal-arrow" aria-hidden="true">↗</span></a></li>'
    )


def update_listings(pages, articles):
    for route, notes in (('/', articles[:2]), ('/journal/', articles)):
        listing = '<ul class="journal-list" role="list">' + ''.join(
            note_link(article, featured=i == 0) for i, article in enumerate(notes)
        ) + '</ul>'
        page = pages[route]
        page['text'], count = re.subn(r'<ul class="journal-list"[^>]*>.*?</ul>', lambda _: listing, page['text'], count=1, flags=re.S)
        if count != 1:
            raise ValueError(f'{route}: expected a journal list')
    more = len(articles) - min(len(articles), 2)
    label = f'+{str(more).translate(PERSIAN_DIGITS)} نوشته دیگر' if more else ''
    pages['/']['text'] = re.sub(
        r'(<a class="archive-button" href="/journal/">همه نوشته‌ها <span class="archive-count">)[^<]*',
        lambda match: match[1] + label, pages['/']['text'], count=1,
    )
    sections = []
    for topic, label in TOPICS.items():
        links = ''.join(
            f'<li><a href="{article["route"]}">{escape(article["headline"])}</a></li>'
            for article in articles if article['topic'] == topic
        )
        if links:
            sections.append(f'<section id="topic-{topic}"><h3>{label}</h3><ul>{links}</ul></section>')
    categories = '<details class="journal-topics"><summary>موضوع‌ها</summary>' + ''.join(sections) + '</details>'
    page = pages['/journal/']
    page['text'], count = re.subn(
        r'<!-- JOURNAL TOPICS -->.*?<!-- END JOURNAL TOPICS -->',
        lambda _: '<!-- JOURNAL TOPICS -->\n' + categories + '\n<!-- END JOURNAL TOPICS -->',
        page['text'], count=1, flags=re.S,
    )
    if count != 1:
        raise ValueError('Missing journal topic markers')
