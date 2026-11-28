"""Refresh static SEO metadata, structured data, sitemap and RSS from page content.

Run with Python 3 from any directory. Markdown rendering uses the optional
authoring dependency in requirements-journal.txt.
"""
from datetime import date, datetime, time, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from html import escape, unescape
import json
import re
import xml.etree.ElementTree as ET

from build_journal import (
    BASE, ROOT, LEGACY_EXCERPTS, LEGACY_TOPICS, TOPICS, render_sources, topic_link, update_listings,
)

SERVICE_PREFIX = '/services/'
SITE_UPDATED = '2026-11-27'
MODIFIED = '2026-10-01'
PAGE_MODIFIED = {
    '/telegram-bot/': SITE_UPDATED,
    '/daruham/': SITE_UPDATED,
    '/gandishiraz/': SITE_UPDATED,
    '/computermelli/': SITE_UPDATED,
    '/journal/async-search-race-conditions/': SITE_UPDATED,
    '/journal/cli-tools-i-use/': SITE_UPDATED,
    '/journal/yarplus-idealist/': '2026-10-17',
    '/yarplus/': SITE_UPDATED,
    '/journal/payment-system-under-sanctions/': '2026-10-17',
    '/journal/microservices-solo-project/': '2026-10-17',
    '/': '2026-11-28',
    '/list/': '2026-11-27',
    '/projects/': SITE_UPDATED,
    '/gamesage/': SITE_UPDATED,
    '/journal/': SITE_UPDATED,
    '/journal/sonnet-5-5-opus-5-5-gpt-6-1-sol/': '2026-10-02',
}
PROJECTS_BY_PAGE = {
    '/': ['gamesage', 'telegram-bot', 'gandishiraz', 'daruham', 'computermelli'],
    '/projects/': ['gamesage', 'yarplus', 'telegram-bot', 'gandishiraz', 'daruham', 'computermelli'],
}
PROJECT_VISUALS = {
    '/computermelli/': ('/computermelli/images/home-20261126.webp', 1440, 960),
    '/gandishiraz/': ('/gandishiraz/images/home.webp', 1440, 960),
    '/daruham/': ('/daruham/images/home.webp', 1440, 960),
    '/gamesage/': ('/gamesage/images/home-20261102.webp', 1440, 1050),
    '/yarplus/': ('/yarplus/images/main.webp', 1600, 900),
}

def plain(text):
    return unescape(re.sub(r'<[^>]+>', ' ', text)).strip()

def meta(text, key, value, attr='name'):
    tag = f'<meta {attr}="{key}" content="{escape(value, quote=True)}">'
    pattern = rf'<meta\s+{attr}="{re.escape(key)}"[^>]*>'
    return re.sub(pattern, lambda _: tag, text) if re.search(pattern, text) else text.replace('</head>', '  '+tag+'\n</head>')

person = {
    '@type':'Person', '@id':BASE+'/#arash-fooladi', 'name':'آرش فولادی',
    'alternateName':['Arash Fooladi','ارش فولادی'], 'url':BASE+'/',
    'image':BASE+'/assets/images/arash-fooladi-logo.jpg',
    'description':'طراحی و ساخت فروشگاه‌های آنلاین و توسعه نرم‌افزار؛ دانشجوی علوم کامپیوتر.',
    'knowsLanguage':['fa','en'],
    'sameAs':['https://github.com/arashfooladi','https://www.linkedin.com/in/arashfooladi','https://x.com/arashfooladiorg','https://dev.to/arashfooladi','https://hashnode.com/@arashfooladi','https://www.instagram.com/arashfooladi_/','https://t.me/onewith_aklilighalb'],
}
website = {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'آرش فولادی','alternateName':'Arash Fooladi','inLanguage':'fa','publisher':{'@id':person['@id']}}

markdown_notes = render_sources()
pages = {}
for path in sorted(ROOT.rglob('*.html')):
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
        continue
    text = path.read_text(encoding='utf-8')
    head = text.partition('</head>')[0]
    if re.search(r'<meta\b[^>]*(?:name="robots"[^>]*noindex|http-equiv="refresh")[^>]*>', head):
        continue
    canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
    if not canonical: raise ValueError(f'Missing canonical: {path}')
    url = canonical[1]
    route = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
    if url != BASE + route or route in pages:
        raise ValueError(f'Invalid or duplicate canonical in {path}: {url}')
    headline = plain(re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)[1])
    # Homepage has a bilingual display name; use the person's primary name.
    if route == '/': headline = 'آرش فولادی'
    title = unescape(re.search(r'<title>(.*?)</title>', text)[1])
    description = unescape(re.search(r'<meta name="description" content="([^"]*)">', text)[1])
    language = re.search(r'<html\b[^>]*\blang="([^"]+)"', text)[1]
    note = markdown_notes.get(route, {})
    published = re.search(r'<time datetime="([^"]+)">(.*?)</time>', text, re.S) if route.startswith('/journal/') and route != '/journal/' else None
    slug = route.strip('/').rsplit('/', 1)[-1]
    image_slug = 'home' if route == '/' else route.strip('/').replace('/', '-')
    image_path = f'/assets/images/social/{image_slug}.png'
    if route in markdown_notes and not (ROOT / image_path.lstrip('/')).is_file():
        image_path = '/assets/images/social/journal.png'
    default_modified = SITE_UPDATED if route.startswith(SERVICE_PREFIX) else MODIFIED
    modified = note.get('modified', note.get('date')) or PAGE_MODIFIED.get(route, default_modified)
    topic = note.get('category', LEGACY_TOPICS.get(slug))
    excerpt = description if note else LEGACY_EXCERPTS.get(slug, '')
    pages[route] = dict(path=path, text=text, route=route, url=url, headline=headline, title=title,
                        description=description, language=language, published=published[1] if published else None,
                        date_label=plain(published[2]) if published else None, modified=modified,
                        topic=topic, excerpt=excerpt, image=BASE + image_path)

def project_list_for(route):
    slugs = PROJECTS_BY_PAGE[route]
    return {'@type':'ItemList','@id':BASE+route+('#projects-list' if route=='/' else '#list'),'name':'پروژه‌های آرش فولادی','itemListOrder':'https://schema.org/ItemListOrderAscending','numberOfItems':len(slugs),'itemListElement':[{'@type':'ListItem','position':i,'name':pages['/'+slug+'/']['headline'],'url':BASE+'/'+slug+'/'} for i,slug in enumerate(slugs,1)]}

article_pages = [page for page in pages.values() if page['published']]
articles = sorted(article_pages, key=lambda page: (page['published'], page['route']), reverse=True)
update_listings(pages, articles)
for route, listing in (('/', articles[:2]), ('/journal/', articles)):
    pages[route]['modified'] = max([pages[route]['modified'], *(article['modified'] for article in listing)])

for route,p in pages.items():
    text,url = p['text'],p['url']
    modified = p['modified']
    text = re.sub(r'<title>.*?</title>', lambda _: '<title>'+escape(p['title'])+'</title>', text)
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', '<!-- SEO_GRAPH -->',text,flags=re.S)
    uses_journal_card = route != '/journal/' and p['image'].endswith('/social/journal.png')
    image_alt = p['title'] if route in ('/', '/list/') else p['headline']+' — آرش فولادی'
    if uses_journal_card:
        image_alt = 'نوشته‌های آرش فولادی'
    for key,value in [('description',p['description']),('author','آرش فولادی'),('robots','index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'),('twitter:card','summary_large_image'),('twitter:site','@arashfooladiorg'),('twitter:creator','@arashfooladiorg'),('twitter:title',p['title']),('twitter:description',p['description']),('twitter:image',p['image']),('twitter:image:alt',image_alt)]:
        text = meta(text,key,value)
    is_article = bool(p['published'])
    is_service = route.startswith(SERVICE_PREFIX)
    is_collection = route in ('/projects/', '/journal/', '/list/')
    locale = {'fa': 'fa_IR', 'en': 'en_US'}[p['language']]
    topic = p['topic']
    for key,value in [('og:type','article' if is_article else 'website'),('og:title',p['title']),('og:description',p['description']),('og:url',url),('og:site_name','آرش فولادی'),('og:locale',locale),('og:image',p['image']),('og:image:secure_url',p['image']),('og:image:type','image/png'),('og:image:width','1200'),('og:image:height','630'),('og:image:alt',image_alt)]:
        text = meta(text,key,value,'property')
    if is_article:
        text = meta(text,'article:published_time',p['published'],'property')
        text = meta(text,'article:modified_time',modified,'property')
        text = meta(text,'article:author',BASE+'/','property')
        if topic:
            text = meta(text, 'article:section', TOPICS[topic], 'property')
            if route not in markdown_notes:
                link = topic_link(topic)
                if link not in text:
                    text = re.sub(r'(<div class="article-meta">.*?)(</div>)',
                                  lambda match: match[1] + link + match[2], text, count=1, flags=re.S)
    else:
        text = re.sub(r'\s*<meta property="article:[^"]+"[^>]*>', '', text)
    if 'rel="icon"' not in text:
        text = text.replace('</head>','  <link rel="icon" type="image/png" sizes="48x48" href="/assets/images/favicon-48.png">\n  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">\n</head>')
    if 'type="application/rss+xml"' not in text:
        text=text.replace('</head>','  <link rel="alternate" type="application/rss+xml" title="نوشته‌های آرش فولادی" href="/feed.xml">\n</head>')
    graph=[website,person]
    page={'@type':'ProfilePage' if route=='/' else 'CollectionPage' if is_collection else 'WebPage','@id':url+'#webpage','url':url,'name':p['title'],'description':p['description'],'inLanguage':p['language'],'isPartOf':{'@id':website['@id']},'dateModified':modified,'primaryImageOfPage':{'@id':url+'#image'}}
    visual = PROJECT_VISUALS.get(route)
    image_url, image_width, image_height = (BASE+visual[0], visual[1], visual[2]) if visual else (p['image'], 1200, 630)
    graph.append({'@type':'ImageObject','@id':url+'#image','url':image_url,'contentUrl':image_url,'width':image_width,'height':image_height,'caption':image_alt if uses_journal_card else p['headline']})
    crumbs=[('Home' if p['language'] == 'en' else 'خانه',BASE+'/')]
    if route != '/' and not is_collection and not is_service:
        crumbs.append(('نوشته‌ها', BASE + '/journal/') if is_article else ('پروژه‌ها', BASE + '/projects/'))
    if route != '/':
        crumbs.append((p['headline'], url))
    if route not in ('/', '/list/'):
        breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i,'name':name,'item':item} for i,(name,item) in enumerate(crumbs,1)]}
        graph.append(breadcrumb); page['breadcrumb']={'@id':breadcrumb['@id']}
        visible = '<nav aria-label="مسیر صفحه" class="breadcrumbs">' + ''.join(
            f'<a href="{item.removeprefix(BASE)}">{escape(name)}</a><span aria-hidden="true">/</span>'
            if i < len(crumbs) - 1 else f'<span aria-current="page">{escape(name)}</span>'
            for i, (name, item) in enumerate(crumbs)
        ) + '</nav>'
        text = re.sub(r'<!-- BREADCRUMBS -->|<nav\b(?=[^>]*\bclass="breadcrumbs")[^>]*>.*?</nav>',
                      lambda _: visible, text, count=1, flags=re.S)
    if route in ('/','/projects/'):
        project_list = project_list_for(route)
        graph.append(project_list)
        if route=='/':
            page['mainEntity']={'@id':person['@id']}
            page['hasPart']=[{'@id':BASE+'/'+slug+'/#work'} for slug in PROJECTS_BY_PAGE[route]]
        else: page['mainEntity']={'@id':project_list['@id']}
    elif route=='/journal/':
        blog={'@type':'Blog','@id':url+'#blog','url':url,'name':'نوشته‌های آرش فولادی','description':p['description'],'inLanguage':'fa','author':{'@id':person['@id']},'blogPost':[{'@type':'BlogPosting','@id':a['url']+'#article','headline':a['headline'],'url':a['url'],'datePublished':a['published'],'author':{'@id':person['@id']}} for a in articles]}
        graph.append(blog);page['mainEntity']={'@id':blog['@id']}
    elif route == '/list/':
        page['author'] = {'@id': person['@id']}
    elif is_service:
        service = {'@type': 'Service', '@id': url + '#service', 'url': url, 'name': p['headline'],
                   'serviceType': p['headline'], 'description': p['description'],
                   'provider': {'@id': person['@id']}, 'areaServed': {'@type': 'Country', 'name': 'ایران'},
                   'mainEntityOfPage': {'@id': page['@id']}}
        graph.append(service)
        page['mainEntity'] = {'@id': service['@id']}
    elif is_article:
        article_body=re.search(r'<article[^>]*>(.*?)<nav\b(?=[^>]*\bclass="article-nav")',text,re.S)[1]
        count=len(plain(article_body).split())
        article={'@type':'BlogPosting','@id':url+'#article','headline':p['headline'],'description':p['description'],'url':url,'mainEntityOfPage':{'@id':page['@id']},'datePublished':p['published'],'dateModified':modified,'inLanguage':'fa','author':{'@id':person['@id']},'publisher':{'@id':person['@id']},'image':{'@id':url+'#image'},'wordCount':count,'isAccessibleForFree':True}
        if topic:
            article['articleSection'] = TOPICS[topic]
        article['isPartOf'] = {'@type':'Blog', '@id':BASE+'/journal/#blog', 'url':BASE+'/journal/', 'name':'نوشته‌های آرش فولادی'}
        graph.append(article);page['mainEntity']={'@id':article['@id']}
    else:
        work={'@type':'CreativeWork','@id':url+'#work','name':p['headline'],'description':p['description'],'url':url,'inLanguage':'fa','creator':{'@id':person['@id']},'author':{'@id':person['@id']},'image':{'@id':url+'#image'},'mainEntityOfPage':{'@id':page['@id']}}
        graph.append(work);page['mainEntity']={'@id':work['@id']}
    graph.append(page)
    graph_markup='<script type="application/ld+json">\n'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2).replace('<', r'\u003c')+'\n  </script>'
    text=text.replace('<!-- SEO_GRAPH -->',graph_markup) if '<!-- SEO_GRAPH -->' in text else text.replace('</head>','  '+graph_markup+'\n</head>')
    text='\n'.join(line.rstrip() for line in text.splitlines())+'\n'
    p['path'].write_text(text,encoding='utf-8')

ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
sitemap=ET.Element('{'+ns+'}urlset')
for route in sorted(pages):
    node=ET.SubElement(sitemap,'{'+ns+'}url')
    ET.SubElement(node,'{'+ns+'}loc').text=pages[route]['url']
    ET.SubElement(node,'{'+ns+'}lastmod').text=pages[route]['modified']
ET.indent(sitemap,space='  ')
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)

atom = 'http://www.w3.org/2005/Atom'
ET.register_namespace('atom', atom)
feed_path = ROOT / 'feed.xml'
previous_dates = {
    item.findtext('link'): item.findtext('pubDate')
    for item in ET.parse(feed_path).findall('channel/item')
} if feed_path.exists() else {}
iran = timezone(timedelta(hours=3, minutes=30))

def published_at(article):
    day = date.fromisoformat(article['published'])
    if article['url'] in previous_dates:
        previous = parsedate_to_datetime(previous_dates[article['url']])
        if previous.date() == day:
            return previous
    return datetime.combine(day, time.min, tzinfo=iran)

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
for key, value in {
    'title': 'نوشته‌های آرش فولادی',
    'link': BASE + '/journal/',
    'description': pages['/journal/']['description'],
    'language': 'fa',
    'lastBuildDate': format_datetime(max([
        datetime.combine(date.fromisoformat(pages['/journal/']['modified']), time.min, tzinfo=iran),
        *(published_at(article) for article in articles),
    ])),
}.items():
    ET.SubElement(channel, key).text = value
ET.SubElement(channel, f'{{{atom}}}link', href=BASE + '/feed.xml', rel='self', type='application/rss+xml')
for article in sorted(articles, key=published_at, reverse=True):
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'title').text = article['headline']
    ET.SubElement(item, 'link').text = article['url']
    ET.SubElement(item, 'guid', isPermaLink='true').text = article['url']
    ET.SubElement(item, 'pubDate').text = format_datetime(published_at(article))
    ET.SubElement(item, 'description').text = article['description']
    if article['topic']:
        ET.SubElement(item, 'category').text = TOPICS[article['topic']]
ET.indent(rss, space='  ')
ET.ElementTree(rss).write(feed_path, encoding='utf-8', xml_declaration=True)
print(f'Refreshed SEO for {len(pages)} canonical pages; sitemap and feed updated.')
