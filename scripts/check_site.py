#!/usr/bin/env python3
"""Static release gates. Checkout and responsive interaction require browser QA too."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json, re, sys
ROOT = Path(__file__).resolve().parents[1]
COMMERCE = json.loads((ROOT / 'scripts/commerce.json').read_text())

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids, self.links, self.images, self.anchors, self.resources = [], [], [], [], []
        self.anchor = None
        self.h1 = 0
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
            self.anchor = {'attrs': a, 'text': ''}
        if tag == 'img': self.images.append(a)
        if tag in ['script', 'img'] and 'src' in a: self.resources.append(a['src'])
        if tag == 'link' and a.get('rel') in ['stylesheet', 'icon']: self.resources.append(a.get('href', ''))
    def handle_data(self, data):
        if self.anchor is not None: self.anchor['text'] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.anchor is not None:
            self.anchors.append(self.anchor)
            self.anchor = None

pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
errors = []
for name, page in pages.items():
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{name}: duplicate IDs {list(k for k,v in Counter(page.ids).items() if v > 1)}')
    if page.h1 != 1: errors.append(f'{name}: expected one H1, found {page.h1}')
    text = page.path.read_text()
    if f'data-order-total="{COMMERCE["total"]}"' not in text: errors.append(f'{name}: wrong configured total')
    amounts = re.findall(r'(?:US\$|\$)\s*(\d+(?:\.\d+)?)', text)
    allowed = {float(COMMERCE[k]) for k in ['price','shipping','total']}
    if any(float(amount) not in allowed for amount in amounts): errors.append(f'{name}: unexpected monetary amounts {amounts}')
    if '<template id="optional-services">' not in text or '/consent.js?' not in text: errors.append(f'{name}: missing optional-service consent gate')
    outside_template = re.sub(r'<template.*?</template>', '', text, flags=re.S)
    if re.search(r'<script[^>]+src="https://(?:www.googletagmanager|connect.facebook|www.clarity|js-na2.hs-scripts)', outside_template): errors.append(f'{name}: optional service loads outside consent gate')
    for pattern in [r'pre[ -]?order', r'August 2027', r'\$219\b', r'\$20\b', r'United States only', r'product in development', r'4gM9ASgVe1IzaOse1Q6kg00']:
        if re.search(pattern, text, re.I): errors.append(f'{name}: stale sale copy {pattern}')
    for anchor in page.anchors:
        a = anchor['attrs']
        if 'data-purchase' in a and a['href'] != COMMERCE['checkout_url']:
            errors.append(f'{name}: wrong direct checkout {a["href"]}')
        if 'buy.stripe.com' in a['href'] and a['href'] != COMMERCE['checkout_url']:
            errors.append(f'{name}: stale Stripe link {a["href"]}')
    for url in page.links + page.resources:
        u = urlsplit(url)
        if u.scheme or u.netloc: continue
        target = unquote(u.path).lstrip('/') or name
        if u.path == '/': target = 'index.html'
        if not (ROOT / target).is_file(): errors.append(f'{name}: missing target {url}')
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{name}: missing anchor {url}')
    for img in page.images:
        if 'alt' not in img: errors.append(f'{name}: missing image alt {img.get("src")}')
        if not img.get('src', '').startswith('http') and not all(img.get(k) for k in ['width','height']):
            errors.append(f'{name}: missing image dimensions {img.get("src")}')
    if name != '404.html':
        for expected in ['mailto:support@keeper.day', 'G-783F93X4HE', '1113554937986944', 'z98vqpb6j4', '247894352.js']:
            if expected not in text: errors.append(f'{name}: missing support/tracking {expected}')
for name in ['index.html', 'camera.html', 'gifting.html', 'support.html', 'terms.html']:
    text = (ROOT / name).read_text().lower()
    for expected in ['199', '30', '229', 'gift box', 'lanyard', 'manual', 'in stock']:
        if expected not in text: errors.append(f'{name}: missing offer detail {expected}')
for name in ['index.html', 'camera.html']:
    text = (ROOT / name).read_text()
    structured = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S).group(1))
    offer = structured['offers']
    if offer['price'] != COMMERCE['price'] or offer['priceCurrency'] != COMMERCE['currency'] or offer['availability'] != 'https://schema.org/InStock': errors.append(f'{name}: invalid product offer schema')
for expected in ['14 days', 'full camera price', 'quality issue', 'original payment method', 'outbound shipping charge is not refundable']:
    if expected not in (ROOT / 'terms.html').read_text(): errors.append(f'terms.html: missing protection {expected}')
if COMMERCE['price'] + COMMERCE['shipping'] != COMMERCE['total']: errors.append('Incorrect commerce total')
if not COMMERCE['checkout_verified']: errors.append('Checkout has not been verified')
if 'Number(document.body.dataset.orderTotal)' not in (ROOT / 'site.js').read_text(): errors.append('Click analytics must read configured order total')
data = json.loads((ROOT / 'scripts/content.json').read_text())
for key in data['assets']:
    if not (ROOT / 'assets/collections' / f'{key}.webp').is_file(): errors.append(f'Missing collection asset {key}')
print(json.dumps({'pages': len(pages), 'curated_images': len(data['assets']), 'storefront_images': len(list((ROOT/'assets/storefront').glob('*.webp'))), 'checkout_verified': COMMERCE['checkout_verified'], 'errors': errors}, indent=2))
sys.exit(bool(errors))
