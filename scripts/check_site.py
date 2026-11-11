#!/usr/bin/env python3
"""Static release gates. Checkout and responsive interaction require browser QA too."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, unquote, parse_qs
from collections import Counter
import json, re, sys
from i18n import LANGUAGES, HTML_LANG, read_catalogs, canonical, variant_name
ROOT = Path(__file__).resolve().parents[1]
COMMERCE = json.loads((ROOT / 'scripts/commerce.json').read_text())
DATA = json.loads((ROOT / 'scripts/content.json').read_text())
CHOICES = set(DATA['active_choices'])
ARCHIVE_VARIANTS = {v['id']:v for v in DATA['variants']}
VARIANTS = {key:value for key,value in ARCHIVE_VARIANTS.items() if key in CHOICES}

def valid_checkout(href, variant=None, locale='en'):
    actual, expected = urlsplit(href), urlsplit(COMMERCE['checkout_url'])
    if (actual.scheme,actual.netloc,actual.path) != (expected.scheme,expected.netloc,expected.path): return False
    query, base = parse_qs(actual.query), parse_qs(expected.query)
    base['locale'] = [locale]
    reference = query.pop('client_reference_id', None)
    if query != base: return False
    if variant and variant != 'classic': return reference == ['keeper-'+variant] and variant in VARIANTS
    return reference is None

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids, self.links, self.images, self.anchors, self.resources = [], [], [], [], []
        self.anchor = None
        self.searches = []
        self.h1 = 0
        self.locale = None
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.locale = a.get('data-locale')
        if 'data-search' in a: self.searches.append(a['data-search'])
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

catalogs = read_catalogs()
verification = ROOT / 'google0c0b3716f5a1174c.html'
paths = [p for p in ROOT.glob('*.html') if p != verification]+[p for lang in LANGUAGES if lang != 'en' for p in (ROOT/lang).glob('*.html')]
pages = {str(p.relative_to(ROOT)): Page(p) for p in paths}
errors = []
if not verification.is_file() or verification.read_text().strip() != 'google-site-verification: google0c0b3716f5a1174c.html':
    errors.append('Google site verification file must be preserved')
if len(pages) != 76: errors.append(f'Expected 76 language pages, found {len(pages)}')
for name, page in pages.items():
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{name}: duplicate IDs {list(k for k,v in Counter(page.ids).items() if v > 1)}')
    if page.h1 != 1: errors.append(f'{name}: expected one H1, found {page.h1}')
    text = re.sub(r'<script id="keeper-not-found" type="application/json">.*?</script>', '', page.path.read_text(), flags=re.S)
    if page.locale not in LANGUAGES: errors.append(f'{name}: missing or invalid locale')
    if f'lang="{HTML_LANG.get(page.locale)}"' not in text: errors.append(f'{name}: wrong document language')
    for lang in LANGUAGES:
        if f'hreflang="{HTML_LANG[lang]}" href="{canonical(page.path.name,lang)}"' not in text: errors.append(f'{name}: missing alternate {lang}')
    if f'rel="canonical" href="{canonical(page.path.name,page.locale)}"' not in text: errors.append(f'{name}: wrong canonical')
    if '/language.js?' not in text or 'id="keeper-i18n"' not in text: errors.append(f'{name}: missing language bootstrap')
    if f'data-order-total="{COMMERCE["total"]}"' not in text: errors.append(f'{name}: wrong configured total')
    amounts = re.findall(r'(?:US\$|\$)\s*(\d+(?:\.\d+)?)', text)
    allowed = {float(COMMERCE[k]) for k in ['price','shipping','total']}
    if any(float(amount) not in allowed for amount in amounts): errors.append(f'{name}: unexpected monetary amounts {amounts}')
    if '<template id="optional-services">' not in text or '/consent.js?' not in text: errors.append(f'{name}: missing optional-service consent gate')
    # Cloudflare otherwise places its email decoder inside our inert consent template.
    email_regions = re.findall(r'<!--email_off-->(.*?)<!--/email_off-->', text, re.S)
    if len(email_regions) != 1 or 'mailto:support@keeper.day' not in email_regions[0]:
        errors.append(f'{name}: support email must work without optional services')
    email_excluded = re.sub(r'<!--email_off-->.*?<!--/email_off-->', '', text, flags=re.S)
    if 'mailto:' in email_excluded or '__cf_email__' in text or '/cdn-cgi/l/email-protection' in text:
        errors.append(f'{name}: unprotected or pre-obfuscated support email')
    policy_match = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)">', text)
    policy = unescape(policy_match.group(1)).split() if policy_match else []
    if not policy or policy[0] != 'script-src-elem' or "'self'" not in policy:
        errors.append(f'{name}: missing script-provider allowlist')
    if any(source in ['*', 'https:', 'http:'] or 'cloudflareinsights.com' in source for source in policy):
        errors.append(f'{name}: injected analytics can bypass the consent provider boundary')
    outside_template = re.sub(r'<template.*?</template>', '', text, flags=re.S)
    if re.search(r'<script[^>]+src="https://(?:www.googletagmanager|connect.facebook|www.clarity|js-na2.hs-scripts)', outside_template): errors.append(f'{name}: optional service loads outside consent gate')
    for pattern in [r'pre[ -]?order', r'August 2027', r'\$219\b', r'\$20\b', r'United States only', r'product in development', r'4gM9ASgVe1IzaOse1Q6kg00']:
        if re.search(pattern, text, re.I): errors.append(f'{name}: stale sale copy {pattern}')
    for anchor in page.anchors:
        a = anchor['attrs']
        parsed = urlsplit(a['href'])
        style = parse_qs(parsed.query).get('style', [None])[0]
        if parsed.path.endswith('/camera.html') and style and style not in CHOICES | {v['group'] for v in VARIANTS.values()}:
            errors.append(f'{name}: link offers an inactive exterior {style}')
        routing = 'data-current-checkout' in a and parsed.path.endswith('/camera.html') and parsed.fragment == 'choose-style'
        if 'data-purchase' in a and not routing and not valid_checkout(a['href'],a.get('data-variant'),page.locale):
            errors.append(f'{name}: wrong direct checkout {a["href"]}')
        if 'buy.stripe.com' in a['href'] and not valid_checkout(a['href'],a.get('data-variant'),page.locale):
            errors.append(f'{name}: stale Stripe link {a["href"]}')
    for url in page.links + page.resources:
        u = urlsplit(url)
        if u.scheme or u.netloc: continue
        target = unquote(u.path).lstrip('/') or name
        if u.path == '/': target = 'index.html'
        elif u.path.endswith('/'): target += 'index.html'
        if not (ROOT / target).is_file(): errors.append(f'{name}: missing target {url}')
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{name}: missing anchor {url}')
    for img in page.images:
        if 'alt' not in img: errors.append(f'{name}: missing image alt {img.get("src")}')
        if not img.get('src', '').startswith('http') and not all(img.get(k) for k in ['width','height']):
            errors.append(f'{name}: missing image dimensions {img.get("src")}')
    if page.path.name != '404.html':
        for expected in ['mailto:support@keeper.day', 'G-783F93X4HE', '1113554937986944', 'z98vqpb6j4', '247894352.js']:
            if expected not in text: errors.append(f'{name}: missing support/tracking {expected}')
for name in ['index.html', 'camera.html', 'gifting.html', 'support.html', 'terms.html']:
    text = (ROOT / name).read_text().lower()
    for expected in ['199', '30', '229', 'gift box', 'lanyard', 'manual', 'in stock']:
        if expected not in text: errors.append(f'{name}: missing offer detail {expected}')
for name in [str(p.relative_to(ROOT)) for p in paths if p.name in ['index.html','camera.html']]:
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
if len(data['designs']) != 98 or len(ARCHIVE_VARIANTS) != 128: errors.append('The original design archive must be retained')
if len(CHOICES) != 8 or 'classic' not in CHOICES or CHOICES - {'classic'} != set(VARIANTS): errors.append('Expected exactly eight active choices including Classic cream')
if sum(d['kind']=='single' for d in data['designs']) != 68 or sum(d['kind']=='paired' for d in data['designs']) != 30: errors.append('Wrong individual/paired design counts')
for d in data['designs']:
    for key in ['image','thumb']:
        if not (ROOT/d[key].lstrip('/')).is_file(): errors.append(f'Missing design image {d[key]}')
    expected = {d['id']+'-a',d['id']+'-b'} if d['kind']=='paired' else {d['id']}
    if {v['id'] for v in ARCHIVE_VARIANTS.values() if v['group']==d['id']} != expected: errors.append(f'Wrong sides for {d["id"]}')
listed = {a['attrs'].get('data-variant') for a in pages['styles.html'].anchors if 'buy.stripe.com' in a['attrs']['href']}
if listed != CHOICES: errors.append('The static catalog must offer exactly the eight active choices')
for lang in LANGUAGES:
    prefix = '' if lang=='en' else lang+'/'
    listed = {a['attrs'].get('data-variant') for a in pages[prefix+'styles.html'].anchors if 'buy.stripe.com' in a['attrs']['href']}
    if listed != CHOICES: errors.append(f'{lang}: wrong static purchase choices')
    product = (ROOT/(prefix+'camera.html')).read_text()
    if set(re.findall(r'data-pick-style="([^"]+)"',product)) != CHOICES: errors.append(f'{lang}: visual picker must contain the same eight choices')
    payload = json.loads(re.search(r'<script type="application/json" id="keeper-design-data">(.*?)</script>',(ROOT/(prefix+'camera.html')).read_text(),re.S).group(1))
    if {v['id'] for v in payload['variants']} != set(VARIANTS): errors.append(f'{lang}: selector and catalog disagree')
    if parse_qs(urlsplit(payload['checkout']).query).get('locale') != [lang]: errors.append(f'{lang}: wrong checkout language')
    for variant in payload['variants']:
        if variant['name'] != variant_name(VARIANTS[variant['id']], catalogs[lang]): errors.append(f'{lang}: wrong localized variant name {variant["id"]}')
    for card in pages[prefix+'styles.html'].anchors:
        if card['attrs'].get('data-variant') and not valid_checkout(card['attrs']['href'],card['attrs']['data-variant'],lang): errors.append(f'{lang}: invalid design checkout')
for lang in ['zh','ja','ko']:
    unchanged = [key for key,value in catalogs[lang]['text'].items() if value == catalogs['en']['text'][key]]
    if unchanged: errors.append(f'{lang}: untranslated text {unchanged}')
if len(re.findall(r'<url>',(ROOT/'sitemap.xml').read_text())) != 72: errors.append('Expected 72 indexable language URLs')
if len(data['lifestyle']) != 8: errors.append('Expected eight lifestyle scenes')
if len(data.get('camera_story',[])) != 2: errors.append('Expected two camera-use scenes')
for scene in data['lifestyle']+data.get('camera_story',[]):
    for suffix in ['', '-480', '-960']:
        if not (ROOT/f'assets/everyday/{scene["id"]}{suffix}.webp').is_file(): errors.append(f'Missing responsive lifestyle image {scene["id"]}{suffix}')
editorial = json.loads((ROOT/'scripts/editorial-content.json').read_text())
for key, asset in editorial['images'].items():
    for width in [480,960,1440]:
        if not (ROOT/(asset['image'].lstrip('/')+f'-{width}.webp')).is_file(): errors.append(f'Missing editorial image {key}-{width}')
for lang in LANGUAGES:
    prefix = '' if lang=='en' else lang+'/'
    home = (ROOT/(prefix+'index.html')).read_text()
    for module in ['ed-hero','ed-shop','ed-facts','camera-looks','how-it-works','e-paper','everyday','ed-finder-callout','ed-gift-intro','review-examples','media','field-notes','ed-brand','community','services','ed-newsletter','ed-footer']:
        if module not in home: errors.append(f'{lang}: missing homepage module {module}')
    if re.search(r'"(?:Review|AggregateRating)"',home): errors.append(f'{lang}: sample review must not output review schema')
    for name in ['index.html','moments.html','press.html','owners.html','learn.html']:
        markup=(ROOT/(prefix+name)).read_text()
        for form in re.findall(r'<form[^>]*data-demo-form[^>]*>.*?</form>',markup,re.S):
            if not re.search(r'<fieldset\b[^>]*\bdisabled(?:\s|>)',form) or not re.search(r'<button\b(?=[^>]*\btype="button")(?=[^>]*\bdisabled(?:\s|>))[^>]*>',form) or re.search(r'<form[^>]+action=',form):errors.append(f'{lang}/{name}: demonstration form enabled')
for lang in LANGUAGES:
    prefix = '' if lang=='en' else lang+'/'
    for filename in ['index.html','styles.html','camera.html','find-your-keeper.html','together.html','press.html','owners.html']:
        if re.search(r'\b128\b', (ROOT/(prefix+filename)).read_text()): errors.append(f'{lang}/{filename}: stale 128-choice offer')
print(json.dumps({'pages': len(pages), 'languages':list(LANGUAGES), 'translation_texts_per_language':len(catalogs['en']['text']), 'ui_messages_per_language':len(catalogs['en']['ui']), 'curated_images': len(data['assets']), 'archived_design_images':len(data['designs']), 'selectable_designs_including_classic':len(CHOICES), 'lifestyle_images':len(data['lifestyle']), 'camera_use_images':len(data.get('camera_story',[])), 'checkout_verified': COMMERCE['checkout_verified'], 'errors': errors}, indent=2))
sys.exit(bool(errors))
