from pathlib import Path
import json, re, sys
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
 'index.html','roadmap.html','labs.html','projects.html','resources.html','progress.html','search.html',
 'level-01/modules/l1-1-frontend-basics-html-and-css.html',
 'level-01/modules/l1-2-version-control-with-git-and-github.html',
 'level-01/modules/l1-3-semantic-html-and-advanced-elements.html',
 'level-01/modules/l1-4-css-layouts-and-advanced-styling.html',
 'level-01/modules/l1-5-build-a-beautiful-portfolio-website.html',
 'level-01/modules/l1-6-assignment-1.html',
 'projects/developer-portfolio.html',
 'lessons/web-foundations/responsive-design.html',
 'lessons/web-foundations/accessibility-foundations.html',
 'lessons/web-foundations/browser-devtools.html',
 'cheatsheets/html.html','cheatsheets/css.html','cheatsheets/git-github.html'
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'Missing required file: {rel}')

class P(HTMLParser):
    def error(self, message): pass

for p in ROOT.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    if '{{TITLE}}' in text: errors.append(f'Unresolved template token: {p.relative_to(ROOT)}')
    if '<html' not in text or '</html>' not in text: errors.append(f'HTML shell missing: {p.relative_to(ROOT)}')
    try: P().feed(text)
    except Exception as e: errors.append(f'Parser error {p.relative_to(ROOT)}: {e}')

# Curriculum JSON and v0.2 statuses
data=json.loads((ROOT/'data/curriculum.json').read_text(encoding='utf-8'))
mods={str(x.get('number')):x for x in data if x.get('level')==1}
for n in '123456':
    if mods[n].get('status')!='tutorial-ready': errors.append(f'Module {n} not tutorial-ready')

# Learning activity file resolution
js=(ROOT/'assets/js/learning-data.js').read_text(encoding='utf-8')
payload=js.split('=',1)[1].rsplit(';',1)[0].strip()
acts=json.loads(payload)
for a in acts:
    if not (ROOT/a['url']).exists(): errors.append(f'Activity URL missing: {a["url"]}')
if len([a for a in acts if a.get('scope')=='web-foundations'])!=16:
    errors.append('Expected 16 Web Foundations learning activities')

if errors:
    print('FAILED')
    print('\n'.join('- '+e for e in errors))
    sys.exit(1)
print(f'OK: {len(list(ROOT.rglob("*.html")))} HTML pages parsed; {len(acts)} v0.2 activities resolved; required files present.')
