from pathlib import Path
from html.parser import HTMLParser
import sys
ROOT=Path(__file__).resolve().parents[1]
class P(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            d=dict(attrs); href=d.get('href','')
            if href: self.links.append(href)
errors=[]
for f in ROOT.rglob('*.html'):
    p=P(); p.feed(f.read_text(encoding='utf-8'))
    for href in p.links:
        if href.startswith(('http://','https://','mailto:','#','javascript:')): continue
        target=href.split('#',1)[0].split('?',1)[0]
        if not target: continue
        dest=(f.parent/target).resolve()
        try: dest.relative_to(ROOT.resolve())
        except ValueError: continue
        if not dest.exists(): errors.append((f.relative_to(ROOT),href))
if errors:
    for a,b in errors: print('BROKEN',a,'->',b)
    sys.exit(1)
print('OK: no broken internal HTML links found')
