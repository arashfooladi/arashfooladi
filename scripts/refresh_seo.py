"""Refresh static SEO metadata, structured data, sitemap and RSS from page content.

Run with Python 3 from any directory. No packages or network calls are required.
Publication dates and page URLs remain unchanged.
"""
from pathlib import Path
from html import escape, unescape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://arashfooladi.ir'
MODIFIED = '2026-10-01'
PAGE_MODIFIED = {
    '/': '2026-10-02',
    '/journal/': '2026-10-02',
    '/journal/sonnet-5-5-opus-5-5-gpt-6-1-sol/': '2026-10-02',
}
ORDER = ['gandishiraz', 'daruham', 'computermelli', 'telegram-bot', 'yarplus']
PAGE_COPY = {
    '/': ('آرش فولادی | طراحی وب و توسعه نرم‌افزار', 'آرش فولادی؛ طراحی و ساخت فروشگاه‌های گاندی شیراز، داروهام و کامپیوتر ملی، توسعه بک‌اند، ربات تلگرام و یادداشت‌هایی درباره نرم‌افزار.'),
    '/projects/': ('پروژه‌های آرش فولادی | فروشگاه‌های آنلاین و بک‌اند', 'نمونه پروژه‌های آرش فولادی؛ ساخت کامل فروشگاه‌های آنلاین روی پایه اختصاصی، زیرساخت ربات تلگرام و پلتفرم اشتراک محتوای یارپلاس.'),
    '/gandishiraz/': ('طراحی و ساخت فروشگاه گاندی شیراز | آرش فولادی', 'ساخت کامل فروشگاه کیف و کفش گاندی شیراز توسط آرش فولادی؛ پایه و قالب اختصاصی، جست‌وجو، فیلتر محصولات، سبد خرید و نسخه موبایل.'),
    '/daruham/': ('طراحی و ساخت وب‌سایت داروهام | آرش فولادی', 'طراحی و ساخت کامل داروهام توسط آرش فولادی؛ فروشگاه سلامت و زیبایی روی پایه اختصاصی، حساب کاربر، نوبت‌دهی و ارسال نسخه.'),
    '/computermelli/': ('ساخت فروشگاه کامپیوتر ملی | آرش فولادی', 'سابقه طراحی و ساخت کامل فروشگاه قطعات کامپیوتر ملی توسط آرش فولادی؛ قالب اختصاصی، جست‌وجوی محصول و اتصال WooCommerce. سایت اکنون غیرفعال است.'),
    '/telegram-bot/': ('زیرساخت ربات تلگرام با ۳۰۰ هزار کاربر | آرش فولادی', 'پروژه ربات تلگرام آرش فولادی با بیش از ۳۰۰ هزار کاربر و ۱۰ میلیون درخواست پردازش‌شده؛ صف کارها، کش، مدیریت درخواست و پایش.'),
    '/yarplus/': ('یارپلاس؛ اشتراک محتوا و پرداخت | آرش فولادی', 'پروژه یارپلاس آرش فولادی؛ پلتفرم اشتراک محتوا و حمایت مالی، با بک‌اند، درگاه پرداخت داخلی و کنترل دسترسی کاربران.'),
    '/journal/': ('نوشته‌های آرش فولادی | نرم‌افزار و هوش مصنوعی', 'یادداشت‌های آرش فولادی درباره نرم‌افزار، مدل‌های هوش مصنوعی، ابزارهای کدنویسی، درگاه پرداخت و تجربه ساخت یارپلاس.'),
}

def plain(text):
    return unescape(re.sub(r'<[^>]+>', ' ', text)).strip()

def meta(text, key, value, attr='name'):
    tag = f'<meta {attr}="{key}" content="{escape(value, quote=True)}">'
    pattern = rf'<meta\s+{attr}="{re.escape(key)}"[^>]*>'
    return re.sub(pattern, tag, text) if re.search(pattern, text) else text.replace('</head>', '  '+tag+'\n</head>')

person = {
    '@type':'Person', '@id':BASE+'/#arash-fooladi', 'name':'آرش فولادی',
    'alternateName':['Arash Fooladi','ارش فولادی'], 'url':BASE+'/',
    'image':BASE+'/assets/images/arash-fooladi-logo.jpg',
    'description':'طراحی و ساخت فروشگاه‌های آنلاین و توسعه نرم‌افزار؛ دانشجوی علوم کامپیوتر.',
    'knowsLanguage':['fa','en'],
    'sameAs':['https://github.com/arashfooladi','https://www.linkedin.com/in/arashfooladi','https://x.com/arashfooladiorg','https://dev.to/arashfooladi','https://hashnode.com/@arashfooladi','https://www.instagram.com/arashfooladi_/','https://t.me/onewith_aklilighalb'],
}
website = {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'آرش فولادی','alternateName':'Arash Fooladi','inLanguage':'fa','publisher':{'@id':person['@id']}}

pages = {}
for path in sorted(ROOT.rglob('*.html')):
    text = path.read_text(encoding='utf-8')
    if 'noindex' in text or 'http-equiv="refresh"' in text: continue
    canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
    if not canonical: raise ValueError(f'Missing canonical: {path}')
    url = canonical[1]; route = url.removeprefix(BASE)
    headline = plain(re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)[1])
    # Homepage has a bilingual display name; use the person's primary name.
    if route == '/': headline = 'آرش فولادی'
    title = unescape(re.search(r'<title>(.*?)</title>', text)[1])
    description = unescape(re.search(r'<meta name="description" content="([^"]*)">', text)[1])
    title, description = PAGE_COPY.get(route, (title, description))
    published = re.search(r'<time datetime="([^"]+)"', text) if route.startswith('/journal/') and route != '/journal/' else None
    image_slug = 'home' if route == '/' else route.strip('/').replace('/', '-')
    pages[route] = dict(path=path,text=text,url=url,headline=headline,title=title,description=description,published=published[1] if published else None,image=BASE+'/assets/images/social/'+image_slug+'.png')

project_list = {'@type':'ItemList','@id':BASE+'/projects/#list','name':'پروژه‌های آرش فولادی','itemListOrder':'https://schema.org/ItemListOrderAscending','numberOfItems':len(ORDER),'itemListElement':[{'@type':'ListItem','position':i,'name':pages['/'+slug+'/']['headline'],'url':BASE+'/'+slug+'/'} for i,slug in enumerate(ORDER,1)]}
articles = sorted((p for route,p in pages.items() if route.startswith('/journal/') and p['published']), key=lambda p:p['published'], reverse=True)

for route,p in pages.items():
    text,url = p['text'],p['url']
    modified = PAGE_MODIFIED.get(route, MODIFIED)
    text = re.sub(r'<title>.*?</title>', '<title>'+escape(p['title'])+'</title>',text)
    text = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '',text,flags=re.S)
    for key,value in [('description',p['description']),('author','آرش فولادی'),('robots','index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'),('twitter:card','summary_large_image'),('twitter:title',p['title']),('twitter:description',p['description']),('twitter:image',p['image']),('twitter:image:alt',p['headline']+' — آرش فولادی')]:
        text = meta(text,key,value)
    is_article = bool(p['published']) and route.startswith('/journal/')
    for key,value in [('og:type','article' if is_article else 'website'),('og:title',p['title']),('og:description',p['description']),('og:url',url),('og:site_name','آرش فولادی'),('og:locale','fa_IR'),('og:image',p['image']),('og:image:secure_url',p['image']),('og:image:type','image/png'),('og:image:width','1200'),('og:image:height','630'),('og:image:alt',p['headline']+' — آرش فولادی')]:
        text = meta(text,key,value,'property')
    if is_article:
        text = meta(text,'article:published_time',p['published'],'property')
        text = meta(text,'article:modified_time',modified,'property')
        text = meta(text,'article:author',BASE+'/','property')
    else:
        text = re.sub(r'\s*<meta property="article:[^"]+"[^>]*>', '', text)
    if 'rel="icon"' not in text:
        text = text.replace('</head>','  <link rel="icon" type="image/png" sizes="48x48" href="/assets/images/favicon-48.png">\n  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">\n</head>')
    if 'type="application/rss+xml"' not in text:
        text=text.replace('</head>','  <link rel="alternate" type="application/rss+xml" title="نوشته‌های آرش فولادی" href="/feed.xml">\n</head>')
    graph=[website,person]
    page={'@type':'ProfilePage' if route=='/' else 'CollectionPage' if route in ('/projects/','/journal/') else 'WebPage','@id':url+'#webpage','url':url,'name':p['title'],'description':p['description'],'inLanguage':'fa','isPartOf':{'@id':website['@id']},'dateModified':modified,'primaryImageOfPage':{'@id':url+'#image'}}
    graph.append({'@type':'ImageObject','@id':url+'#image','url':p['image'],'contentUrl':p['image'],'width':1200,'height':630,'caption':p['headline']})
    crumbs=[('خانه',BASE+'/')]
    if route in ('/projects/','/journal/'):
        crumbs.append((p['headline'],url))
    elif route!='/':
        parent='journal' if is_article else 'projects'
        crumbs.extend([('نوشته‌ها' if is_article else 'پروژه‌ها',BASE+'/'+parent+'/'),(p['headline'],url)])
    if route!='/':
        breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i,'name':name,'item':item} for i,(name,item) in enumerate(crumbs,1)]}
        graph.append(breadcrumb); page['breadcrumb']={'@id':breadcrumb['@id']}
        visible='<nav class="breadcrumbs" aria-label="مسیر صفحه">'+''.join((f'<a href="{item.removeprefix(BASE)}">{escape(name)}</a><span aria-hidden="true">/</span>' if i<len(crumbs)-1 else f'<span aria-current="page">{escape(name)}</span>') for i,(name,item) in enumerate(crumbs))+'</nav>'
        text=re.sub(r'\s*<nav class="breadcrumbs".*?</nav>','',text,flags=re.S)
        header=r'(<header class="(?:article-header|archive-header)[^"]*">\s*<div class="(?:inner|container)">)'
        text=re.sub(header,lambda m:m[1]+'\n      '+visible,text,count=1)
    if route in ('/','/projects/'):
        graph.append(project_list)
        if route=='/':
            page['mainEntity']={'@id':person['@id']}
            page['hasPart']=[{'@id':BASE+'/'+slug+'/#work'} for slug in ORDER]
        else: page['mainEntity']={'@id':project_list['@id']}
    elif route=='/journal/':
        blog={'@type':'Blog','@id':url+'#blog','url':url,'name':'نوشته‌های آرش فولادی','description':p['description'],'inLanguage':'fa','author':{'@id':person['@id']},'blogPost':[{'@type':'BlogPosting','@id':a['url']+'#article','headline':a['headline'],'url':a['url'],'datePublished':a['published'],'author':{'@id':person['@id']}} for a in articles]}
        graph.append(blog);page['mainEntity']={'@id':blog['@id']}
    elif is_article:
        article_body=re.search(r'<article[^>]*>(.*?)<nav class="article-nav"',text,re.S)[1]
        count=len(plain(article_body).split())
        article={'@type':'BlogPosting','@id':url+'#article','headline':p['headline'],'description':p['description'],'url':url,'mainEntityOfPage':{'@id':page['@id']},'datePublished':p['published'],'dateModified':modified,'inLanguage':'fa','author':{'@id':person['@id']},'publisher':{'@id':person['@id']},'image':{'@id':url+'#image'},'wordCount':count,'isAccessibleForFree':True}
        graph.append(article);page['mainEntity']={'@id':article['@id']}
    else:
        work={'@type':'CreativeWork','@id':url+'#work','name':p['headline'],'description':p['description'],'url':url,'inLanguage':'fa','creator':{'@id':person['@id']},'author':{'@id':person['@id']},'image':{'@id':url+'#image'},'mainEntityOfPage':{'@id':page['@id']}}
        graph.append(work);page['mainEntity']={'@id':work['@id']}
    graph.append(page)
    text=text.replace('</head>','  <script type="application/ld+json">\n'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2)+'\n  </script>\n</head>')
    text='\n'.join(line.rstrip() for line in text.splitlines())+'\n'
    p['path'].write_text(text,encoding='utf-8')

ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
sitemap=ET.Element('{'+ns+'}urlset')
for route in sorted(pages):
    node=ET.SubElement(sitemap,'{'+ns+'}url')
    ET.SubElement(node,'{'+ns+'}loc').text=pages[route]['url']
    ET.SubElement(node,'{'+ns+'}lastmod').text=PAGE_MODIFIED.get(route, MODIFIED)
ET.indent(sitemap,space='  ')
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)

atom='http://www.w3.org/2005/Atom';ET.register_namespace('atom',atom)
rss=ET.parse(ROOT/'feed.xml');channel=rss.getroot().find('channel')
if channel.find('{'+atom+'}link') is None:
    ET.SubElement(channel,'{'+atom+'}link',{'href':BASE+'/feed.xml','rel':'self','type':'application/rss+xml'})
for item in channel.findall('item'):
    route=item.findtext('link').removeprefix(BASE)
    item.find('title').text=pages[route]['headline']
    item.find('description').text=pages[route]['description']
ET.indent(rss,space='  ');rss.write(ROOT/'feed.xml',encoding='utf-8',xml_declaration=True)
print(f'Refreshed SEO for {len(pages)} canonical pages; sitemap and feed updated.')
