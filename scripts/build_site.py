#!/usr/bin/env python3
"""Build Keeper's in-stock storefront and clearly separated studio collections."""
from pathlib import Path
import json
import html
import re
from storefront import home_body, product_body, gifting_body, support_body
from policies import terms_body

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/content.json').read_text())
COMMERCE = json.loads((ROOT / 'scripts/commerce.json').read_text())
C = json.loads((ROOT / 'scripts/components.json').read_text())
A = DATA['assets']
E = lambda x: html.escape(str(x), quote=True)
VERSION = '20261108-in-stock'
STRIPE = COMMERCE['checkout_url']
PRICE, SHIPPING, TOTAL = (COMMERCE[k] for k in ['price', 'shipping', 'total'])
NAV = [('camera.html', 'Shop Keeper'), ('index.html#how-it-works', 'How it works'),
       ('moments.html', 'Gallery'), ('gifting.html', 'Gifting'), ('support.html', 'Support')]


def image(key, eager=False):
    a = A[key]
    return f'<img src="/assets/collections/{E(key)}.webp" alt="{E(a["alt"])}" width="{a["width"]}" height="{a["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def card(key):
    a = A[key]
    return f'<article class="collection-card{" scene-wide" if a.get("wide") else ""}"><figure><a class="image-link" href="/assets/collections/{E(key)}.webp" target="_blank" rel="noopener" aria-label="View full image: {E(a["title"])} (opens new tab)">{image(key)}</a></figure><h3>{E(a["title"])}</h3><p>{E(a["copy"])}</p></article>'


def footer():
    return '''<footer><div class="footer-discover"><div><a class="wordmark" href="/">keeper<span>.</span>day</a><p>A little camera.<br>A day worth keeping.</p><p>Color e-paper. Favorite people. Everyday life.</p></div><div><h3>Make it a Keeper</h3><a href="/camera.html">Shop the camera</a><a href="/gifting.html">Inside the gift box</a><a href="/moments.html">Everyday gallery</a><a href="/support.html">Help &amp; answers</a></div><div><h3>Here to help</h3><a href="mailto:support@keeper.day">support@keeper.day</a><a href="/terms.html">Shipping &amp; returns</a><a href="/privacy.html">Privacy</a><button class="cookie-settings" type="button" data-open-consent>Cookie settings</button><details><summary>From the design studio</summary><a href="/together.html">Paired artwork concepts</a><a href="/styles.html">Surface-art concepts</a><a href="/little-apps.html">Interface concepts</a></details></div></div><div class="footer-bottom"><span>© 2026 keeper.day · Meetu Studio</span><span>In stock · Gift box included · Worldwide shipping</span><a href="#main">Back to top ↑</a></div><p class="storefront-image-note">Some product and lifestyle images are AI-generated visualizations, not customer photographs or actual camera sample output. Screen images are simulated. See product details for included items.</p></footer>'''


def render(filename, title, description, body, product=False):
    nav = ''.join(f'<a class="nav-link" href="/{p}"' + (' aria-current="page"' if p == filename else '') + f'>{t}</a>' for p, t in NAV)
    mobile = ''.join(f'<a href="/{p}">{t}</a>' for p, t in NAV)
    canonical = 'https://keeper.day/' + ('' if filename == 'index.html' else filename)
    structured = ''
    if product:
        structured = '<script type="application/ld+json">' + json.dumps({
            '@context': 'https://schema.org', '@type': 'Product', 'name': 'Keeper color e-paper camera',
            'description': 'In-stock camera with a gift box, lanyard and instruction manual.',
            'image': ['https://keeper.day/assets/storefront/everyday-hero.webp', 'https://keeper.day/assets/storefront/gift-box.webp'],
            'brand': {'@type': 'Brand', 'name': 'keeper.day'},
            'offers': {'@type': 'Offer', 'url': canonical, 'priceCurrency': 'USD',
                       'price': COMMERCE['price'], 'availability': 'https://schema.org/InStock',
                       'itemCondition': 'https://schema.org/NewCondition',
                       'seller': {'@type': 'Organization', 'name': 'Meetu Studio'}}
        }, ensure_ascii=False).replace('</', '<\\/') + '</script>'
    content = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#f8f5ed">
<link rel="canonical" href="{canonical}"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/styles.css?v={VERSION}"><link rel="stylesheet" href="/redesign.css?v={VERSION}"><link rel="stylesheet" href="/experience.css?v={VERSION}"><link rel="stylesheet" href="/storefront.css?v={VERSION}"><link rel="stylesheet" href="/consent.css?v={VERSION}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://keeper.day/assets/og-card.webp?v={VERSION}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
{structured}<script src="/consent.js?v={VERSION}" defer></script><script src="/site.js?v={VERSION}" defer></script><script src="/storefront.js?v={VERSION}" defer></script></head>
<body class="keeper-home storefront-body page-{filename.removesuffix('.html')}" data-order-total="{TOTAL}"><a class="skip-link" href="#main">Skip to content</a><div class="announcement">In stock. Ready for your everyday. <span>Gift box included · ${SHIPPING} worldwide shipping</span></div>
<header class="site-header"><a class="wordmark" href="/" aria-label="keeper.day home">keeper<span>.</span>day</a><nav aria-label="Main navigation">{nav}<a class="nav-contact" data-purchase="header" href="{E(STRIPE)}" aria-label="Buy one Keeper camera for ${PRICE} plus ${SHIPPING} shipping, ${TOTAL} total">Buy Keeper — ${PRICE} <span aria-hidden="true">↗</span></a></nav><details class="mobile-menu"><summary aria-label="Open navigation">Menu <span aria-hidden="true">+</span></summary><div><a href="/">Home</a>{mobile}<a href="{E(STRIPE)}" data-purchase="mobile-menu">Buy Keeper — ${PRICE}</a></div></details></header>
<section class="consent-banner" data-consent-banner aria-label="Privacy choices" hidden><p>Optional analytics, advertising and chat stay off until you choose. Shopping and secure checkout work either way. <a href="/privacy.html">Privacy details</a></p><div class="consent-actions"><button type="button" data-consent-decline>Essential only</button><button type="button" data-consent-allow>Allow optional</button></div></section><main id="main">{body}</main>{footer()}<template id="optional-services">{C['tracking']}</template></body></html>'''
    (ROOT / filename).write_text(content)
    print('Built', filename)


render('index.html', 'Keeper — A little camera. A day worth keeping.',
       f'Keep favorite moments in sight with the Keeper color e-paper camera. In stock. Gift box, lanyard and manual included. ${PRICE} + ${SHIPPING} worldwide shipping.', home_body(COMMERCE), True)
render('camera.html', f'Shop Keeper — Color e-paper camera, ${PRICE}',
       f'Meet the in-stock Keeper camera: color e-paper, a red shutter button and a gift box to keep. ${PRICE} camera + ${SHIPPING} worldwide shipping = ${TOTAL}.', product_body(COMMERCE), True)
render('gifting.html', 'A gift worth keeping — Keeper camera & gift box',
       f'Give a little camera and a place for favorite memories. Every Keeper includes a gift box, lanyard and instruction manual. In stock, ${PRICE} plus ${SHIPPING} shipping.', gifting_body(COMMERCE))
render('support.html', 'Keeper support — Orders, shipping, camera & returns',
       'Find answers about the Keeper camera, what is in the box, worldwide shipping, cancellations and returns. Contact support@keeper.day.', support_body(COMMERCE))

# Old studio URLs remain useful, but are no longer presented as the retail offer.
collections = [
    ('together.html', 'Paired artwork', 'Two little worlds. One shared idea.', 'pairs', 'two',
     'These paired designs are studio artwork concepts, not a two-camera bundle or a wireless photo-sharing feature. The standard purchase contains one camera; illustrated skins are not included.'),
    ('styles.html', 'Surface-art sketchbook', 'A little more like you.', 'styles', 'four style-grid',
     'A collection of surface-art ideas, not available colors, finishes or included stickers. Shop Keeper for the standard camera and its confirmed contents.'),
    ('little-apps.html', 'Interface sketchbook', 'Ideas for another day.', 'apps', 'two',
     'These are interface concepts, not released or working apps. Connectivity, reminders, automatic updates and phone-photo transfer shown here are not included features of the current camera.')]
for filename, title, headline, group, grid, notice in collections:
    body = f'<section class="page-intro"><p class="eyebrow">FROM THE DESIGN STUDIO</p><h1>{headline}</h1><p class="section-lead">{notice}</p><a class="text-link" href="/camera.html">Shop the standard camera ↗</a></section><section class="section-pad"><h2>{title}</h2><div class="collection-grid {grid}">' + ''.join(card(k) for k in DATA[group]) + '</div></section>'
    render(filename, title + ' — Keeper studio', notice, body)

# A focused photographic album; concept art stays in the studio collections.
scenes = [('everyday-hero', 'The coffee that ran a little long.', 'A face worth keeping close, even on an ordinary morning.'),
          ('in-the-hand', 'Take the long way home.', 'For neighborhood walks and the people who make them better.'),
          ('at-home', 'Give a photo a place to belong.', 'Beside the books, the coffee, and the things you come back to.'),
          ('gift-box', 'A small box. A personal beginning.', 'One camera, a gift box, a lanyard and an instruction manual are included.')]
gallery = '<section class="page-intro"><p class="eyebrow">EVERYDAY KEEPERS</p><h1>The days between<br><em>the big days.</em></h1><p class="section-lead">A camera for your favorite people. A color e-paper display for a moment you want to keep in sight.</p></section><section class="section-pad"><div class="collection-grid two scenes">'
for key, title, copy in scenes:
    gallery += f'<article class="collection-card scene-wide"><figure><a href="/assets/storefront/{key}.webp" target="_blank" rel="noopener" aria-label="Open full image: {E(title)}"><img src="/assets/storefront/{key}.webp" width="1440" height="960" loading="lazy" decoding="async" alt="{E(title)}"></a></figure><h2>{title}</h2><p>{copy}</p></article>'
gallery += ''.join(card(k) for k in ['moment-cafe-friends', 'moment-neighborhood-couple'])
gallery += '</div><p class="asset-note">An AI-generated lifestyle album, not customer photographs or samples captured with a production camera. Screen images illustrate how a favorite photograph can have a place in daily life.</p><a class="buy-button" href="/camera.html">Find your Keeper ↗</a></section>'
render('moments.html', 'Everyday gallery — Keeper', 'Coffee dates, walks, quiet corners and gifts. Explore a photographic vision of everyday life with the Keeper color e-paper camera.', gallery)

render('terms.html', 'Shipping, returns & purchase terms — Keeper',
       f'Keeper is in stock. ${PRICE} camera + ${SHIPPING} worldwide shipping = ${TOTAL}. Included gift box, lanyard and manual. Cancellation and return terms.', terms_body(COMMERCE))
render('404.html', 'Page not found — Keeper', 'Find your way back to Keeper.', '<section class="page-intro"><p class="eyebrow">404 · A little off the beaten path</p><h1>This page got away.</h1><p class="section-lead">The good days are still here. Let’s find your next Keeper.</p><a class="buy-button" href="/camera.html">Meet the camera ↗</a></section>')
error_page = ROOT / '404.html'
error_page.write_text(error_page.read_text().replace('<title>', '<meta name="robots" content="noindex"><title>', 1))
privacy_source = ROOT / 'scripts/privacy-body.html'
render('privacy.html', 'Privacy notice — Keeper', 'How Keeper and Meetu Studio handle order, payment, support and website usage information.', privacy_source.read_text())
urls = ['', 'camera.html', 'gifting.html', 'support.html', 'moments.html', 'together.html', 'styles.html', 'little-apps.html', 'terms.html', 'privacy.html']
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://keeper.day/{p}</loc></url>\n' for p in urls) + '</urlset>\n')
