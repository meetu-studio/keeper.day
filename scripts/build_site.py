#!/usr/bin/env python3
"""Build the static Keeper site from curated content and reusable components.
Run with Python 3; no framework or runtime dependency is needed for deployment.
"""
from pathlib import Path
import json, re, html
ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'scripts/content.json').read_text())
A = DATA['assets']
COMPONENTS = ROOT/'scripts/components.json'
if not COMPONENTS.exists():
    old = (ROOT/'index.html').read_text()
    assert 'id="preorder-heading"' in old
    def section(marker):
        start = old.index('<section', old.rfind('<section', 0, old.index(marker)))
        return old[start:old.index('</section>', start)+10]
    parts = {key:section(marker) for key,marker in {
      'camera':'id="camera"', 'camera_heading':'class="camera-heading"',
      'preorder':'id="pre-order"', 'epaper':'id="e-paper"',
      'ritual':'class="ritual-section"','faq':'id="questions"',
      'story':'id="story"','contact':'id="contact"'}.items()}
    parts['tracking'] = old[old.index('  <noscript>'):old.index('</body>')]
    COMPONENTS.write_text(json.dumps(parts,ensure_ascii=False,indent=2)+'\n')
C = json.loads(COMPONENTS.read_text())
E = lambda x:html.escape(str(x),quote=True)
STRIPE='https://buy.stripe.com/4gM9ASgVe1IzaOse1Q6kg00?locale=en'
VERSION='20261106-collections'
NAV=[('camera.html','The camera'),('together.html','Made for two'),('little-apps.html','Little apps'),('styles.html','Your style'),('moments.html','Little moments')]
CONCEPT='Design explorations · Not included in the current pre-order'
def image(key, eager=False):
    a=A[key]
    return f'<img src="/assets/collections/{E(key)}.webp" alt="{E(a["alt"])}" width="{a["width"]}" height="{a["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
def card(key,href=None,category=None):
    a=A[key]
    photo=image(key)
    if href: photo=f'<a class="image-link" href="{E(href)}">{photo}<span class="visual-arrow" aria-hidden="true">↗</span></a>'
    else: photo=f'<a class="image-link" href="/assets/collections/{E(key)}.webp" target="_blank" rel="noopener" aria-label="View full image: {E(a["title"])} (opens new tab)">{photo}<span class="visual-arrow" aria-hidden="true">↗</span></a>'
    return f'<article class="collection-card"'+(f' data-category="{E(category)}"' if category else '')+f'><figure>{photo}</figure><p class="index">{E(a.get("label","DESIGN EXPLORATION"))}</p><h3>{E(a["title"])}</h3><p>{E(a["copy"])}</p></article>'
def intro(kicker,title,copy,concept=False):
    return f'<section class="page-intro"><p class="eyebrow"><a href="/">KEEPER.DAY</a> / {kicker}</p><h1>{title}</h1><div class="intro-bottom"><p class="section-lead">{copy}</p>'+ (f'<span class="concept-label">{CONCEPT}</span>' if concept else '')+'</div></section>'
def heading(kicker,title,copy='',href='',link='Explore the collection'):
    return f'<div class="section-heading"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2>'+ (f'<p>{copy}</p>' if copy else '')+'</div>'+ (f'<a class="text-link" href="{href}">{link} <span aria-hidden="true">↗</span></a>' if href else '')+'</div>'
def note(kind='design'):
    texts={
      'design':('From the studio, not a finished product.','These existing project visuals explore future looks and experiences. They are not available variants or confirmed launch features, and are not included in the current camera pre-order.'),
      'pairs':('Two designs. One shared idea.','Paired artwork is a visual design concept, not a two-camera bundle or a wireless sharing feature. The current pre-order includes one standard camera. Paired skins and finishes are not included.'),
      'apps':('A look at what we’re exploring.','These are interface and display concepts, not working or released apps. Connectivity, automatic updates, reminders, schedules and photo transfer are not confirmed launch features or included in the current pre-order.'),
      'styles':('A sketchbook of possibilities.','These are surface-art and sticker concepts, not currently purchasable colors or accessories. Final materials, fit and availability are unconfirmed. The current pre-order includes one standard camera.')}
    title,copy=texts[kind]
    return f'<aside class="note-bar"><strong>{title}</strong>{copy} <a href="/camera.html#pre-order">See exactly what you’re pre-ordering.</a></aside>'
def next_block():
    return '<section class="explore-next"><div><p class="eyebrow">ONE LITTLE OBJECT. A PLACE IN YOUR DAY.</p><h2>Start with a keeper.</h2><p>The color e-paper camera is in development. Explore the standard camera, the pre-order details, and what we’re building next.</p></div><a class="text-link" href="/camera.html#pre-order">Meet the camera <span aria-hidden="true">↗</span></a></section>'
def app_preview():
    keys=DATA['app_featured']
    first=A[keys[0]]
    choices=''.join(f'<button type="button" data-preview-key="{E(k)}" data-preview-src="/assets/collections/{E(k)}.webp" data-preview-alt="{E(A[k]["alt"])}" data-preview-title="{E(A[k]["title"])}" data-preview-copy="{E(A[k]["copy"])}" aria-pressed="{str(i==0).lower()}">{E(A[k]["short"])}</button>' for i,k in enumerate(keys))
    return f'<div class="app-preview" data-preview><figure>{image(keys[0])}</figure><div><p class="eyebrow">A LITTLE MORE THAN A PHOTO</p><h3 data-preview-title>{E(first["title"])}</h3><p data-preview-copy aria-live="polite">{E(first["copy"])}</p><div class="preview-choices" role="group" aria-label="Choose a display concept">{choices}</div><span class="concept-label">Interface preview · Not released software</span><br><a class="text-link" href="/little-apps.html#collection">Explore all little apps <span aria-hidden="true">↗</span></a></div></div>'
def footer():
    links=''.join(f'<a href="/{p}">{t}</a>' for p,t in NAV)
    return f'<footer><div class="footer-discover"><div><a class="wordmark" href="/">keeper<span>.</span>day</a><p>A little camera. Your favorite people. A day worth keeping.</p><span class="concept-label">Made with care by Meetu Studio</span></div><div><h3>Discover Keeper</h3>{links}</div><div><h3>Here to help</h3><a href="/camera.html#questions">Questions &amp; answers</a><a href="mailto:support@keeper.day">support@keeper.day</a><a href="/terms.html">Purchase terms</a><a href="/privacy.html">Privacy</a><a href="https://github.com/meetu-studio/keeper.day" target="_blank" rel="noopener noreferrer">Follow the project ↗</a></div></div><div class="footer-bottom"><span>© 2026 keeper.day · Meetu Studio</span><span>US pre-orders · Expected shipping August 2027</span><a href="#main">Back to top ↑</a></div></footer>'
def render(filename,title,description,body):
    nav=''.join(f'<a class="nav-link" href="/{p}"'+(' aria-current="page"' if p==filename else '')+f'>{t}</a>' for p,t in NAV)
    mobile=''.join(f'<a href="/{p}"'+(' aria-current="page"' if p==filename else '')+f'>{t}</a>' for p,t in NAV)
    canonical='https://keeper.day/'+('' if filename=='index.html' else filename)
    content=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#f8f5ed">
<link rel="canonical" href="{canonical}"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/styles.css?v=befe7547b3b5"><link rel="stylesheet" href="/redesign.css?v=20261106-1"><link rel="stylesheet" href="/experience.css?v={VERSION}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://keeper.day/assets/og-card.webp"><meta name="twitter:card" content="summary_large_image">
<script src="/site.js?v={VERSION}" defer></script></head>
<body class="keeper-home page-{filename.removesuffix('.html')}"><a class="skip-link" href="#main">Skip to content</a><div class="announcement">A little camera. A day worth keeping. <span>US pre-orders · Expected August 2027</span></div>
<header class="site-header"><a class="wordmark" href="/" aria-label="keeper.day home">keeper<span>.</span>day</a><nav aria-label="Main navigation">{nav}<a class="nav-contact" href="/camera.html#pre-order">Pre-order — $199 <span aria-hidden="true">↗</span></a></nav><details class="mobile-menu"><summary aria-label="Open navigation">Menu <span aria-hidden="true">+</span></summary><div><a href="/">Home</a>{mobile}<a href="/camera.html#questions">FAQ</a><a href="#contact">Contact</a></div></details></header>
<main id="main">{body}{C['contact']}</main>{footer()}{C['tracking']}</body></html>'''
    (ROOT/filename).write_text(content)
    print('Built',filename)
# Home: a curated overview with substantial previews of every collection.
hero=f'''<section class="hero new-hero" aria-labelledby="intro-heading"><div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span> A LITTLE CAMERA. A WORLD OF YOU.</p><h1 id="intro-heading">Your people.<br>Your little world.<br><em>Worth keeping.</em></h1><p class="hero-description">A color e-paper camera for the days you love.<br> And a whole sketchbook of ways to make it yours.</p><div class="purchase-actions"><a class="buy-button" href="/camera.html">Meet the camera <span aria-hidden="true">↗</span></a><a class="text-link" href="#discover">Find your kind of Keeper <span aria-hidden="true">↓</span></a></div><p class="fine-print">Standard camera: $199 + $20 US shipping · $219 paid today.<br>In development · Expected August 2027 · <a href="/terms.html">Full refund before shipment.</a></p></div><figure class="new-hero-art">{image('pair-photos',True)}<figcaption>Made for two · Paired design exploration, not a two-camera offer</figcaption></figure></section>'''
nav='<div class="collection-nav" id="discover">'+''.join(f'<a href="/{p}"><span><small>0{i+1} / DISCOVER</small>{t}</span><span aria-hidden="true">↗</span></a>' for i,(p,t) in enumerate(NAV[1:]))+'</div>'
home=hero+nav
home+='<section class="section-pad" id="camera">'+heading('START WITH THE CAMERA','A photograph.<br><em>With a place in your life.</em>','A red shutter button. A matte, color e-paper display. A favorite moment that stays in sight.','/camera.html','Explore the camera')+'<div class="home-camera-row"><figure><img src="/assets/product-flowers.webp" width="659" height="891" alt="Original Keeper camera design with a flower photo" loading="lazy"></figure><div><p class="eyebrow">TAKE IT. KEEP IT. COME BACK TO IT.</p><h3>Not buried in your camera roll.</h3><p>Put a favorite face beside your coffee, your books, or your bedside lamp. Keeper gives a photograph somewhere to belong.</p><ul><li>A reflective, paper-like color display</li><li>A small object made for everyday moments</li><li>One standard camera in each pre-order</li></ul><a class="text-link" href="/camera.html#e-paper">Why color e-paper? <span aria-hidden="true">↗</span></a><p class="fine-print">Product design preview. Taking and updating photos require battery power.</p></div></div></section>'
home+='<section class="editorial-split" id="together"><figure>'+image('pair-sun-moon')+'</figure><div class="editorial-copy"><p class="eyebrow">MADE FOR TWO</p><h2>You have yours.<br><em>I have you.</em></h2><p>Sun and moon. Mountains and sea. Your picture on mine, my picture on yours. Explore paired artwork for two people with a little world of their own.</p><a class="text-link" href="/together.html">Find your other half <span aria-hidden="true">↗</span></a><span class="concept-label">Paired artwork concepts · Not a bundle</span></div></section>'
home+='<section class="section-pad app-teaser" id="studio">'+heading('LITTLE APPS, BIG PERSONALITY','A little space for<br><em>your everyday.</em>')+app_preview()+note('apps')+'</section>'
home+='<section class="section-pad style-band">'+heading('MAKE IT YOURS','Same little Keeper.<br><em>A different kind of you.</em>','From quiet botanicals to retro pixels, a collection of surface-art ideas with personality.','/styles.html','Explore your style')+'<div class="collection-grid four style-grid">'+''.join(card(k,'/styles.html') for k in DATA['styles'][:4])+ '</div><p class="asset-note">Surface-art concepts, not currently available finishes or accessories.</p></section>'
home+='<section class="section-pad home-moments" id="moments">'+heading('A DAY WORTH KEEPING','The big days.<br><em>And all the days between.</em>','Your favorite people. Your favorite place. That face you never get tired of.','/moments.html','See the little moments')+'<div class="collection-grid scenes">'+''.join(card(k,'/moments.html') for k in DATA['moments'][:4])+'</div><p class="asset-note">Lifestyle imagery is illustrative and AI-created, not customer photography or testimonials.</p></section>'
home+=C['story']+C['preorder'].replace('shown below','shown on this site').replace('Companion app concepts, widgets, and Bluetooth/photo-transfer explorations','Paired designs, decorative finishes, companion app concepts, widgets, and Bluetooth/photo-transfer explorations')
render('index.html','keeper.day — A little camera. A world of you.','Discover Keeper: a color e-paper camera, paired artwork, personal styles and little app concepts. Standard camera pre-order: $199 + $20 US shipping.',home)
# The camera: detailed product, checkout terms, FAQ.
camera=intro('THE CAMERA','Take the photo.<br><em>Keep the feeling.</em>','A small camera with a color e-paper display. For favorite moments that deserve more than a place in your camera roll.')+C['camera']+C['epaper']+C['ritual']+C['preorder'].replace('shown below','shown on this site')+C['faq']
camera=camera.replace('<h2>A little camera. A little keepsake.</h2>','<h2>A little camera. A little keepsake.</h2>')
camera+='<section class="section-pad">'+heading('BEYOND THE CAMERA','There’s more in the sketchbook.','Explore the paired designs, personal styles and little-app concepts we’re imagining.','/little-apps.html','Step inside the studio')+note()+'</section>'
render('camera.html','The camera — keeper.day','Meet the Keeper color e-paper camera. One camera: US$199 + US$20 US shipping. Expected August 2027. Pre-order terms and answers.',camera)
# Together: substantial paired design collection.
together=intro('MADE FOR TWO','Two little Keepers.<br><em>One shared world.</em>','For your favorite person, your partner in everything, or the friend who just gets you. A collection of paired artwork that makes more sense together.',True)
together+='<figure class="wide-art">'+image('pair-photos',True)+'<figcaption>Your picture on mine. My picture on yours. — A paired visual concept, not a connected sharing feature.</figcaption></figure>'
together+='<section class="intro-statements"><div><h3>Different, together.</h3><p>Two complementary pieces of artwork. Each has its own personality; together, they tell a little story.</p></div><div><h3>Your kind of pair.</h3><p>For couples, best friends and the people who feel like home. Pick the design that feels like the two of you.</p></div><div><h3>A concept, clearly.</h3><p>These are existing studio explorations. Paired skins, two-camera bundles and wireless photo sharing are not included in the current pre-order.</p></div></section>'
together+='<section class="section-pad">'+heading('FIND YOUR OTHER HALF','Some things are<br><em>better together.</em>')+'<div class="collection-grid two">'+''.join(card(k) for k in DATA['pairs'] if k!='pair-photos')+'</div>'+note('pairs')+'</section>'+next_block()
render('together.html','Made for two — keeper.day','Explore Keeper paired artwork: sun and moon, mountains and sea, matching moments and little worlds for two. Design concepts, not available bundles.',together)
# Little apps: an interactive preview and a real gallery, not one tiny contact sheet.
apps=intro('LITTLE APPS','A little helper.<br><em>A little delight.</em>','A photo one moment. A quiet piece of everyday information the next. Explore the display scenes and companion-app ideas already in our sketchbook.',True)
apps+='<section class="section-pad app-teaser">'+app_preview()+'</section><section class="section-pad" id="collection">'+heading('THE CONCEPT COLLECTION','More ways to<br><em>make the day yours.</em>','Each card shows an individual design exploration. These are previews, not functioning demos.')+'<div class="filter-row" role="group" aria-label="Filter little app concepts"><button type="button" data-filter="all" aria-pressed="true">All concepts</button><button type="button" data-filter="display" aria-pressed="false">On your Keeper</button><button type="button" data-filter="companion" aria-pressed="false">Companion app</button></div><p class="filter-status" aria-live="polite">'+str(len(DATA['apps']))+' concepts</p><div class="collection-grid two app-gallery" data-filter-grid>'+''.join(card(k,category=A[k]['category']) for k in DATA['apps'])+'</div>'+note('apps')+'</section>'+next_block()
render('little-apps.html','Little apps & everyday ideas — keeper.day','Explore Keeper calendar, reminder, travel and anniversary display concepts, plus companion app galleries, layouts and device settings.',apps)
# Surface artwork collection.
styles=intro('YOUR STYLE','A little more<br><em>like you.</em>','Retro pixels. Botanical details. Quiet lines. Color everywhere. Explore the surface-art ideas that turn the same small object into something personal.',True)
styles+='<section class="section-pad style-band">'+heading('THE STYLE SKETCHBOOK','Find your kind<br><em>of little keeper.</em>')+'<div class="collection-grid four style-grid">'+''.join(card(k) for k in DATA['styles'])+'</div>'+note('styles')+'</section><section class="editorial-split"><figure>'+image('pair-sun-moon')+'</figure><div class="editorial-copy"><p class="eyebrow">A MATCH MADE IN THE SKETCHBOOK</p><h2>One for you.<br><em>One for your person.</em></h2><p>Some designs come with an other half. Explore the paired artwork collection.</p><a class="text-link" href="/together.html">See Made for two <span aria-hidden="true">↗</span></a></div></section>'+next_block()
render('styles.html','Your style — keeper.day','Browse Keeper surface-art concepts: retro pixels, botanicals, graphic lines, soft colors and personal details. Design explorations, not available finishes.',styles)
# Lifestyle image-led stories.
moments=intro('LITTLE MOMENTS','Life looks good<br><em>on you.</em>','Not every keeper is a big occasion. Sometimes it’s your favorite face, a slow afternoon, or a day you wish would last a little longer.')
moments+='<section class="section-pad home-moments">'+heading('THE EVERYDAY ALBUM','For whatever<br><em>makes your day.</em>')+'<div class="collection-grid two scenes">'+''.join(card(k) for k in DATA['moments'])+'</div><p class="asset-note">These are AI-created lifestyle illustrations and product design previews, not customer photographs or testimonials. Final hardware details and accessories remain subject to engineering.</p></section>'+C['story']+next_block()
render('moments.html','Little moments — keeper.day','An illustrated album of Keeper in everyday life: friends, gifts, favorite faces and days worth keeping.',moments)
# Sitemap includes the complete public information architecture.
urls=['','camera.html','together.html','little-apps.html','styles.html','moments.html','terms.html','privacy.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://keeper.day/{p}</loc></url>\n' for p in urls)+'</urlset>\n')
