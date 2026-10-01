from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading, functools, re, html

root=Path(__file__).resolve().parents[1]

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',8766),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
target=root/'assets/images/social';target.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
    count=0
    for path in sorted(root.rglob('*.html')):
        text=path.read_text(encoding='utf-8')
        if 'noindex' in text or 'http-equiv="refresh"' in text:continue
        title=html.unescape(re.search(r'<title>(.*?)</title>',text)[1]).split(' | ')[0]
        description=html.unescape(re.search(r'<meta name="description" content="([^"]+)"',text)[1])
        route=re.search(r'<link rel="canonical" href="https://arashfooladi.ir([^"]+)"',text)[1]
        slug='home' if route=='/' else route.strip('/').replace('/','-')
        card=f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><link rel="stylesheet" href="http://127.0.0.1:8766/assets/css/fonts.css"><style>
        *{{box-sizing:border-box}}body{{margin:0;background:#080808;color:#f5f4ee;font-family:Vazirmatn,sans-serif;width:1200px;height:630px;padding:65px 75px;display:flex;flex-direction:column;}}header{{display:flex;align-items:center;gap:20px;color:#d9ff5b;font-size:27px;}}img{{width:56px;height:56px}}h1{{margin:42px 0 18px;font-size:54px;line-height:1.55;font-weight:700;max-width:1000px;}}p{{margin:0;color:#aaa9a1;font-size:25px;line-height:1.9;max-width:1000px;}}footer{{margin-top:auto;padding-top:22px;border-top:1px solid #333;color:#aaa9a1;direction:ltr;text-align:left;font:19px Inter,sans-serif;}}</style></head><body><header><img src="http://127.0.0.1:8766/assets/images/favicon-48.png" alt=""><span>آرش فولادی · Arash Fooladi</span></header><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p><footer>arashfooladi.ir{html.escape(route if route!='/' else '')}</footer></body></html>'''
        page.goto('http://127.0.0.1:8766/')
        page.set_content(card,wait_until='load');page.evaluate('document.fonts.ready')
        assert page.evaluate('document.body.scrollHeight <= 630'),slug
        page.screenshot(path=str(target/(slug+'.png')))
        count+=1
    browser.close()
server.shutdown()
print('Created',count,'page-specific share previews at 1200 × 630.')
