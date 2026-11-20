#!/usr/bin/env python3
"""Build Keeper's in-stock storefront and clearly separated studio collections."""
from pathlib import Path
import json
import html
import re
from storefront import home_body, product_body, gifting_body, support_body, styles_body, moments_body
from policies import terms_body
from editorial import home_body, moments_body, finder_body, learn_body, guide_body, about_body, press_body, owners_body, GUIDES
from i18n import LANGUAGES, canonical, read_catalogs, localize, attach_not_found

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/content.json').read_text())
COMMERCE = json.loads((ROOT / 'scripts/commerce.json').read_text())
C = json.loads((ROOT / 'scripts/components.json').read_text())
A = DATA['assets']
E = lambda x: html.escape(str(x), quote=True)
VERSION = '20261111-name-only-picker'
CATALOGS = read_catalogs()
# Keep CDN-injected analytics outside the consent-controlled provider set.
SCRIPT_POLICY = "script-src-elem 'self' 'unsafe-inline' https://www.googletagmanager.com https://connect.facebook.net https://*.clarity.ms https://*.hs-scripts.com https://*.usemessages.com https://*.hs-banner.com https://*.hs-analytics.net https://*.hscollectedforms.net https://*.hubspot.com https://*.hsadspixel.net https://*.hsleadflows.net"
STRIPE = COMMERCE['checkout_url']
PRICE, SHIPPING, TOTAL = (COMMERCE[k] for k in ['price', 'shipping', 'total'])
NAV = [('camera.html', 'The camera'), ('styles.html', 'Find your look'), ('learn.html', 'Photography'), ('gifting.html', 'Gifting'), ('support.html', 'Support')]


# 2026-11-20: brighter commercial versions of the inspiration and photo-diary pictures sit in a 20261120 folder beside the
# 20261110 originals, same names and sizes. Pages use the new file where one exists; the kept 2026-11-11 designs keep
# the originals (AGENTS.md: add, never overwrite).
# the share card: the 2026-11-20 one (its hillside photo recast) once it exists, else the old one
OG_CARD = 'og-card-20261120.webp' if (ROOT / 'assets/og-card-20261120.webp').exists() else 'og-card.webp'
BRIGHTER = re.compile(r'/assets/(inspiration|photo-diary)/20261110/([a-z0-9-]+-(?:240|480|960|1440|full)\.webp)')


def brighter(page):
    # 2026-11-20, later: a recast version (no Black people, the owner's request) wins over the bright one where it exists
    def newest(m):
        for d in ('20261120-recast', '20261120'):
            if (ROOT / 'assets' / m[1] / d / m[2]).exists():
                return f'/assets/{m[1]}/{d}/{m[2]}'
        return m[0]
    return BRIGHTER.sub(newest, page)


def image(key, eager=False):
    a = A[key]
    return f'<img src="/assets/collections/{E(key)}.webp" alt="{E(a["alt"])}" width="{a["width"]}" height="{a["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def card(key):
    a = A[key]
    return f'<article class="collection-card{" scene-wide" if a.get("wide") else ""}"><figure><a class="image-link" href="/assets/collections/{E(key)}.webp" target="_blank" rel="noopener" aria-label="View full image: {E(a["title"])} (opens new tab)">{image(key)}</a></figure><h3>{E(a["title"])}</h3><p>{E(a["copy"])}</p></article>'


def footer():
    return '<footer class="ed-footer"><div class="ed-footer-grid"><div><a class="wordmark" href="/">keeper<span>.</span>day</a><p>A pocket camera.<br>A photograph kept close.</p><p>Meetu Studio</p></div><div><h3>Shop</h3><a href="/camera.html">The camera · $199</a><a href="/styles.html">All exterior designs</a><a href="/find-your-keeper.html">Find your Keeper</a><a href="/together.html">Paired designs</a><a href="/gifting.html">Gifting</a></div><div><h3>Photography</h3><a href="/learn.html">Photography guides</a><a href="/moments.html">Everyday gallery</a><a href="/moments.html#membership">The photo circle</a><a href="/little-apps.html">Interface sketchbook</a></div><div><h3>About Keeper</h3><a href="/about.html">Our story</a><a href="/press.html">Media examples</a><a href="/press.html#partnerships">Partnerships</a><a href="/owners.html#site-updates">Studio updates</a></div><div><h3>Here to help</h3><a href="/support.html">Help &amp; answers</a><a href="/owners.html">For your Keeper</a><a href="mailto:support@keeper.day">support@keeper.day</a><a href="/terms.html">Shipping &amp; returns</a><a href="/privacy.html">Privacy</a><button class="cookie-settings" type="button" data-open-consent>Cookie settings</button></div></div><div class="footer-bottom"><span>© 2026 keeper.day · Meetu Studio</span><span>In stock · Gift box included · Worldwide shipping</span><a href="#main">Back to top ↑</a></div><p class="storefront-image-note">Screen images are simulated. Each purchase includes one camera with the selected exterior, gift box, lanyard and instruction manual.</p></footer>'


# 2026-11-20: the home page and the product page in every language now come from scripts/redesign/build.py.
# This builder keeps writing its own version of them beside the new ones, as <name>-20261111.html, out of the
# search index, so the new pages are never overwritten and the old design is never lost.
REPLACED = {'index.html': 'index-20261111.html', 'camera.html': 'camera-20261111.html'}


# 2026-11-20 (owner): Keeper goes online on its own and exports photos without a phone; it also receives photos
# sent from afar and syncs to the cloud. The current pages swap the older sentences for these (their translations
# are in scripts/locales); the sources keep the old sentences, and so do the kept 2026-11-11 pages.
NO_PHONE_20261120 = {
    'Connect directly to your phone to export photos.':
        'Keeper goes online on its own and exports photos, no phone needed.',
    'Keeper takes photos independently and stores them on microSD. Connect it directly to your phone to export photos.':
        'No phone is needed. Keeper takes photos independently and stores them on microSD, and it goes online on its own to export them.',
    'Frame with the small viewfinder, press the red shutter, then connect directly to your phone when you want to export your photos.':
        'Frame with the small viewfinder and press the red shutter. Keeper goes online on its own to export your photos, no phone needed.',
    'Check that your storage card is ready before heading out. Connect Keeper directly to your phone to export your photographs. Ask support about compatibility with your particular phone.':
        'Check that your storage card is ready before heading out. Keeper goes online on its own to export your photographs, so you do not need a phone.',
    'Connect Keeper directly to your phone to export photos. Contact us for phone or card compatibility and delivery questions.':
        'Keeper goes online on its own to export photos, no phone needed. Contact us about memory cards and delivery.',
    'These are interface concepts, not released or working apps. Wireless connectivity, reminders and automatic updates shown here are not included features of the current camera. Photos can be exported by connecting Keeper directly to a phone.':
        'These are interface concepts, not released or working apps. Reminders and automatic updates shown here are not included features of the current camera. Keeper goes online on its own: it exports photos without a phone, receives photos sent from afar and syncs them to the cloud.',
}


def no_phone(content):
    for old, new in NO_PHONE_20261120.items():
        content = content.replace(old, new)
    return content


def render(filename, title, description, body, product=False):
    nav = ''.join(f'<a class="nav-link" href="/{p}"' + (' aria-current="page"' if p == filename else '') + f'>{t}</a>' for p, t in NAV)
    about_menu = '<details class="nav-discover"><summary>About Keeper <span aria-hidden="true">⌄</span></summary><div><a href="/about.html">Our story</a><a href="/press.html">Media examples</a><a href="/press.html#partnerships">Partnerships</a><a href="/owners.html">For your Keeper</a></div></details>'
    nav = nav.replace('<a class="nav-link" href="/support.html"', about_menu+'<a class="nav-link" href="/support.html"')
    mobile = ''.join(f'<a href="/{p}">{t}</a>' for p, t in NAV)
    mobile += '<a href="/about.html">Our story</a><a href="/press.html">Media examples</a><a href="/find-your-keeper.html">Find your Keeper</a><a href="/owners.html">For your Keeper</a>'
    canonical = 'https://keeper.day/' + ('' if filename == 'index.html' else filename)
    structured = ''
    if product:
        structured = '<script type="application/ld+json">' + json.dumps({
            '@context': 'https://schema.org', '@type': 'Product', 'name': 'Keeper pocket color e-paper camera',
            'description': 'Pocket digital camera with a small viewfinder, physical red shutter, color e-paper photo display, gift box, lanyard and instruction manual.',
            'image': ['https://keeper.day/assets/everyday/01-take-the-photo.webp', 'https://keeper.day/assets/designs/st-42.webp'],
            'brand': {'@type': 'Brand', 'name': 'keeper.day'},
            'offers': {'@type': 'Offer', 'url': canonical, 'priceCurrency': 'USD',
                       'price': COMMERCE['price'], 'availability': 'https://schema.org/InStock',
                       'itemCondition': 'https://schema.org/NewCondition',
                       'seller': {'@type': 'Organization', 'name': 'Meetu Studio'}}
        }, ensure_ascii=False).replace('</', '<\\/') + '</script>'
    moments = '<script type="module" src="/assets/moments/moments.js?v='+VERSION+'"></script>' if 'data-moment=' in body else ''
    content = f'''<!doctype html>
<html lang="en" data-type="product" data-motion data-radius="soft" data-buttons="pill"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="page-type" content="product"><meta name="site-kind" content="tech">
<meta http-equiv="Content-Security-Policy" content="{SCRIPT_POLICY}">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#faf9f5">
<link rel="canonical" href="{canonical}"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/styles.css?v={VERSION}"><link rel="stylesheet" href="/redesign.css?v={VERSION}"><link rel="stylesheet" href="/experience.css?v={VERSION}"><link rel="stylesheet" href="/storefront.css?v={VERSION}"><link rel="stylesheet" href="/editorial.css?v={VERSION}"><link rel="stylesheet" href="/consent.css?v={VERSION}"><link rel="stylesheet" href="/assets/motion/motion.css?v={VERSION}">
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://keeper.day/assets/{OG_CARD}?v={VERSION}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
{structured}<script src="/consent.js?v={VERSION}" defer></script><script src="/site.js?v={VERSION}" defer></script><script src="/storefront.js?v={VERSION}" defer></script><script src="/editorial.js?v={VERSION}" defer></script><script type="module" src="/assets/motion/motion.js?v={VERSION}"></script>{moments}</head>
<body class="keeper-home storefront-body page-{filename.removesuffix('.html')}" data-order-total="{TOTAL}"><!-- Look: client paper white / ink / red accents; IBM Plex Sans; photography hero; nav-split; footer-columns; close-type; static photo chapters; pill; wordmark. Compact heights and visible AI captions follow the approved client brief. --><!--email_off--><a class="skip-link" href="#main">Skip to content</a><div class="announcement">In stock. Ready for your everyday. <span>Gift box included · ${SHIPPING} worldwide shipping</span></div>
<header class="site-header"><a class="wordmark" href="/" aria-label="keeper.day home">keeper<span>.</span>day</a><nav aria-label="Main navigation">{nav}<a class="nav-contact" data-current-checkout data-purchase="header" href="/camera.html#choose-style" aria-label="Buy one Keeper camera for ${PRICE} plus ${SHIPPING} shipping, ${TOTAL} total">Shop camera — ${PRICE} <span aria-hidden="true">↗</span></a></nav><details class="mobile-menu"><summary aria-label="Open navigation">Menu <span aria-hidden="true">+</span></summary><div><a href="/">Home</a>{mobile}<a href="/camera.html#choose-style" data-current-checkout data-purchase="mobile-menu">Shop camera — ${PRICE}</a></div></details></header>
<section class="consent-banner" data-consent-banner aria-label="Privacy choices" hidden><p>Optional cookies enable analytics and chat. Checkout works with essential cookies. <a href="/privacy.html">Privacy details</a></p><div class="consent-actions"><button type="button" data-consent-decline>Essential only</button><button type="button" data-consent-allow>Allow optional</button></div></section><main id="main">{body}</main>{footer()}<button id="mobile-open-chat" class="mobile-chat-launcher" type="button" aria-label="Live chat" hidden><svg aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092a10 10 0 1 0-4.777-4.719M8 12h.01M12 12h.01M16 12h.01"/></svg><span>Live chat</span></button><!--/email_off--><template id="optional-services">{C['tracking']}</template></body></html>'''
    if filename not in REPLACED:
        content = no_phone(content)
    pages = {locale:localize(content,locale,filename,CATALOGS,VERSION) for locale in LANGUAGES}
    if filename == '404.html':
        pages['en'] = attach_not_found(pages)
    for locale, page in pages.items():
        name = REPLACED.get(filename, filename)
        if name != filename:
            page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">\n<!-- The 2026-11-11 design of ' + filename + ', kept beside the 2026-11-20 design that replaced it (scripts/redesign/build.py; AGENTS.md: add, never overwrite). -->\n', 1)
        else:
            page = brighter(page)
        target = ROOT/name if locale == 'en' else ROOT/locale/name
        target.parent.mkdir(exist_ok=True)
        target.write_text(page)
        print('Built', target.relative_to(ROOT))


render('index.html', 'Keeper — A pocket camera with color e-paper',
       f'A pocket camera for photographing everyday life. Frame your shot, use the red shutter, and keep a photograph on color e-paper. In stock. Gift box, lanyard and manual included. ${PRICE} + ${SHIPPING} worldwide shipping.', home_body(COMMERCE), True)
render('camera.html', f'Shop Keeper — Color e-paper camera, ${PRICE}',
       f'Meet the in-stock Keeper camera: color e-paper, a red shutter button and a gift box to keep. ${PRICE} camera + ${SHIPPING} worldwide shipping = ${TOTAL}.', product_body(COMMERCE), True)
render('gifting.html', 'A gift worth keeping — Keeper camera & gift box',
       f'Give a camera for the photographs you will make together. Every Keeper includes a gift box, lanyard and instruction manual. In stock, ${PRICE} plus ${SHIPPING} shipping.', gifting_body(COMMERCE))
render('support.html', 'Keeper support — Orders, shipping, camera & returns',
       'Find answers about the Keeper camera, what is in the box, worldwide shipping, cancellations and returns. Contact support@keeper.day.', support_body(COMMERCE))

render('styles.html', 'Find your look — eight Keeper exteriors',
       'Choose from eight looks, including Porcelain White and Sun & moon A or B. Every Keeper is $199 plus $30 worldwide shipping.', styles_body(COMMERCE))
render('together.html', 'Paired designs — Choose your side, Keeper',
       'Sun & moon: choose A or B, sold individually. One Keeper camera with your selected exterior, $199 plus $30 worldwide shipping.', styles_body(COMMERCE,True))
notice = 'These are interface concepts, not released or working apps. Wireless connectivity, reminders and automatic updates shown here are not included features of the current camera. Photos can be exported by connecting Keeper directly to a phone.'
body = '<section class="page-intro"><p class="eyebrow">FROM THE DESIGN STUDIO</p><h1>Ideas for another day.</h1><p class="section-lead">'+notice+'</p><a class="text-link" href="/camera.html">Meet the camera ↗</a></section><section class="section-pad"><h2>Interface sketchbook</h2><p class="sf-micro">AI-generated concept images; the interfaces shown are not released features.</p><div class="collection-grid two">'+''.join(card(k) for k in DATA['apps'])+'</div></section>'
render('little-apps.html', 'Interface sketchbook — Keeper studio', notice, body)
render('moments.html', 'Everyday gallery — Keeper',
       'Coffee dates, campus days, trails, birthdays, workdays and gifts. A little camera for your kind of everyday.', moments_body(COMMERCE))

render('terms.html', 'Shipping, returns & purchase terms — Keeper',
       f'Keeper is in stock. ${PRICE} camera + ${SHIPPING} worldwide shipping = ${TOTAL}. Included gift box, lanyard and manual. Cancellation and return terms.', terms_body(COMMERCE))
render('404.html', 'Page not found — Keeper', 'Find your way back to Keeper.', '<section class="page-intro"><p class="eyebrow">404 · A little off the beaten path</p><h1>This page got away.</h1><p class="section-lead">The good days are still here. Let’s find your next Keeper.</p><a class="buy-button" href="/camera.html">Meet the camera ↗</a></section>')
privacy_source = ROOT / 'scripts/privacy-body.html'
render('privacy.html', 'Privacy notice — Keeper', 'How Keeper and Meetu Studio handle order, payment, support and website usage information.', privacy_source.read_text())
extra_pages = [
    ('find-your-keeper.html','Find your Keeper','Choose an exterior for your everyday photographs.',finder_body(COMMERCE)),
    ('learn.html','Photography guides','Field notes for your first Keeper photograph and your next photo walk.',learn_body(COMMERCE)),
    ('about.html','About Keeper','A pocket camera, a paper-like photograph and a look of your own.',about_body(COMMERCE)),
    ('press.html','Media and partnerships','Clearly marked editorial and partnership examples for the Keeper website.',press_body(COMMERCE)),
    ('owners.html','For your Keeper','Guides, purchase information and a preview of product registration.',owners_body(COMMERCE)),
]+[(f'guide-{g["id"]}.html',g['title'],g['summary'],guide_body(COMMERCE,g['id'])) for g in GUIDES]
for filename,title,description,body in extra_pages:
    render(filename,title,description,body)
urls = ['', 'camera.html', 'gifting.html', 'support.html', 'moments.html', 'together.html', 'styles.html', 'little-apps.html', 'terms.html', 'privacy.html']
urls += [p[0] for p in extra_pages]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{canonical(p or "index.html",locale)}</loc></url>\n' for locale in LANGUAGES for p in urls) + '</urlset>\n')
