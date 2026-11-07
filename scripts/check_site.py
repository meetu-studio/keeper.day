#!/usr/bin/env python3
"""Local, dependency-free static-site checks. Does not contact checkout."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.ids=[];self.links=[];self.images=[];self.anchors=[];self.anchor=None;self.h1=0;self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='a' and 'href' in a:
            self.links.append(a['href']);self.anchor={'attrs':a,'text':''}
        if tag=='img':self.images.append(a)
    def handle_data(self,data):
        if self.anchor is not None:self.anchor['text']+=data
    def handle_endtag(self,tag):
        if tag=='a' and self.anchor is not None:
            self.anchors.append(self.anchor);self.anchor=None
pages={p.name:Page(p) for p in ROOT.glob('*.html')}
errors=[]
for name,page in pages.items():
    if len(page.ids)!=len(set(page.ids)):errors.append(f'{name}: duplicate IDs')
    if page.h1!=1:errors.append(f'{name}: expected 1 H1, found {page.h1}')
    for anchor in page.anchors:
        a=anchor['attrs']
        if anchor['text'].strip().lower().startswith('pre-order') or 'data-preorder' in a:
            if a['href']!='https://buy.stripe.com/4gM9ASgVe1IzaOse1Q6kg00?locale=en':
                errors.append(f'{name}: preorder must link directly to Stripe, found {a["href"]}')
    for url in page.links:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        target=unquote(u.path).lstrip('/') or name
        if u.path=='/':target='index.html'
        p=ROOT/target
        if not p.is_file():errors.append(f'{name}: missing target {url}')
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{name}: missing anchor {url}')
    for img in page.images:
        src=img.get('src','')
        if src.startswith('http'):continue
        if not (ROOT/src.lstrip('/')).is_file():errors.append(f'{name}: missing image {src}')
        if 'alt' not in img:errors.append(f'{name}: image has no alt {src}')
    if name in ['index.html','camera.html','together.html','little-apps.html','styles.html','moments.html']:
        text=page.path.read_text()
        if 'mailto:support@keeper.day' not in text:errors.append(f'{name}: official support missing')
        if 'August 2027' not in text:errors.append(f'{name}: development timing missing')
        if 'gmail.com' in text:errors.append(f'{name}: old contact address')
for name in ['index.html','camera.html']:
    text=(ROOT/name).read_text()
    for expected in ['219','199','20','14 days','full refund','quality issues','buy.stripe.com/4gM9ASgVe1IzaOse1Q6kg00']:
        if expected.lower() not in text.lower():errors.append(f'{name}: missing purchase detail {expected}')
data=json.loads((ROOT/'scripts/content.json').read_text())
for key in data['assets']:
    if not (ROOT/'assets/collections'/f'{key}.webp').is_file():errors.append(f'Missing optimized asset: {key}')
print(json.dumps({'pages':len(pages),'curated_images':len(data['assets']),'errors':errors},indent=2))
sys.exit(bool(errors))
