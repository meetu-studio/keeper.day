"""Product-first Keeper storefront. Body fragments; shell and commerce belong to build_site."""
from html import escape
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
import json

DATA = json.loads((Path(__file__).parent/'content.json').read_text())
CHOICES = DATA['active_choices']
DATA['variants'] = [v for v in DATA['variants'] if v['id'] in CHOICES]
DATA['designs'] = [d for d in DATA['designs'] if any(v['group'] == d['id'] for v in DATA['variants'])]
DESIGNS = {d['id']: d for d in DATA['designs']}


def _e(value):
    return escape(str(value), quote=True)


def _money(value):
    return f'${float(value):,.0f}'


def _image(name, alt, eager=False, thumbnail=False):
    path = name if name.startswith('/') else '/assets/storefront/' + name + '.webp'
    w, h = (659, 891) if 'product-flowers' in path else (1440, 960)
    responsive = ' srcset="/assets/storefront/full-kit-720.webp 720w, /assets/storefront/full-kit.webp 1440w" sizes="(max-width:700px) calc(100vw - 40px), 46vw"' if name == 'full-kit' else ''
    if '/assets/inspiration/' in path:
        base = path.removesuffix('-1440.webp')
        responsive = ' srcset="'+', '.join(f'{base}-{size}.webp {size}w' for size in [480,960,1440])+'" sizes="(max-width:700px) calc(100vw - 40px), 46vw"'
    if thumbnail:
        responsive = ''
        if '/inspiration/' in path: path = path.replace('-1440.webp','-240.webp')
        elif name == 'full-kit': path = '/assets/storefront/full-kit-720.webp'
    return f'<img src="{_e(path)}"{responsive} alt="{_e(alt)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'


def _buy(c, placement, label='Buy Keeper'):
    direct = placement == 'product-hero'
    href = c['checkout_url'] if direct else '/camera.html#choose-style'
    return f'<a class="sf-buy" data-current-checkout data-purchase="{_e(placement)}" href="{_e(href)}">{label if direct else "Shop the camera"}<span aria-hidden="true">↗</span></a>'


def _price(c):
    return f'<div class="sf-price"><strong>{_money(c["price"])}</strong><span>USD · camera &amp; gift package</span></div><p class="sf-shipping">+ {_money(c["shipping"])} worldwide shipping <span>·</span> <strong>{_money(c["total"])} USD total</strong></p><p class="sf-micro sf-price-note">Destination customs duties or taxes, if applicable, are not included. <a href="/terms.html">Payment &amp; shipping details</a>.</p>'


def _purchase(c, placement):
    return _price(c)+f'<div class="sf-actions">{_buy(c, placement)}<a class="sf-link" href="#how-it-works">How it works <span aria-hidden="true">↓</span></a></div><p class="sf-micro">Full refund before shipment. <a href="/terms.html">14-day unused returns &amp; terms</a>.<br>Need it by a particular date? <a href="mailto:support@keeper.day">Ask us before ordering.</a></p>'


def _head(kicker, title, copy=''):
    return f'<div class="sf-section-head"><p class="sf-kicker">{kicker}</p><h2>{title}</h2>'+ (f'<p>{copy}</p>' if copy else '')+'</div>'


def _gallery():
    editorial=json.loads((Path(__file__).parent/'editorial-content.json').read_text())['images']
    images = [('/assets/product-flowers.webp','Keeper camera with flower image on the color e-paper display','The camera'),(editorial['trail']['image']+'-1440.webp',editorial['trail']['alt'],'Out taking photographs'),(editorial['hero']['image']+'-1440.webp',editorial['hero']['alt'],'Photograph your people'),('full-kit','Keeper camera, gift box, lanyard and instruction manual','What’s included'),(editorial['studio']['image']+'-1440.webp',editorial['studio']['alt'],'At your desk')]
    panels, buttons = [], []
    for i, (src, alt, label) in enumerate(images):
        visual = _image(src,alt,i==0)
        if i == 0:
            visual = '<div class="sf-photo-stage">'+visual+'<div class="kr-pair-overlay" data-pair-overlay hidden><button type="button" data-pair-side="a" aria-pressed="false"><span>A · left</span></button><button type="button" data-pair-side="b" aria-pressed="false"><span>B · right</span></button></div></div>'
        panels.append(f'<figure class="sf-gallery-panel{" sf-hardware" if i == 0 else ""}" id="sf-photo-{i}" data-sf-panel>{visual}<figcaption>{label}</figcaption></figure>')
        buttons.append(f'<button class="sf-thumb" type="button" data-sf-photo="{i}" aria-controls="sf-photo-{i}" aria-pressed="{str(i == 0).lower()}" aria-label="Show image {i+1}: {_e(label)}">{_image(src,"",False,True)}</button>')
    return '<div class="sf-gallery" data-sf-gallery><p class="kr-image-selection" data-image-selection aria-live="polite">Classic cream · one camera</p><div class="sf-gallery-panels">'+''.join(panels)+'</div><div class="sf-thumbnails" role="group" aria-label="Product images" hidden>'+''.join(buttons)+'</div><p class="sf-micro">AI images and screen simulations are shooting references, not camera sample photographs.</p><p class="sf-sr-only" data-sf-gallery-status aria-live="polite"></p></div>'


def _box(c):
    items = ''.join(f'<li><span aria-hidden="true">✓</span>{_e(item)}</li>' for item in c['included'])
    return f'<section class="sf-box sf-section" id="in-the-box"><figure>{_image("full-kit","The standard Keeper package: one camera, gift box, lanyard and instruction manual")}</figure><div>{_head("Included with your camera","Ready to give.","Every camera includes the gift box.")}<ul class="sf-included">{items}</ul><p class="sf-micro">One camera with your selected exterior per package. Memory card inclusion is not confirmed; please ask before ordering.</p><a class="sf-link" href="/gifting.html">Meet your next thoughtful gift <span aria-hidden="true">↗</span></a></div></section>'


def _benefits():
    return '<section class="sf-section sf-benefits" aria-label="Made for taking photographs"><article><span class="sf-icon" aria-hidden="true">↗</span><h2>Find something worth a photo.</h2><p>The friend who makes you laugh. The light on your walk. Bring a camera and notice a little more.</p></article><article><span class="sf-icon" aria-hidden="true">●</span><h2>Press a real shutter.</h2><p>Frame your picture in the small viewfinder. Take it with the red physical shutter button.</p></article><article><span class="sf-icon" aria-hidden="true">▤</span><h2>Keep the photograph you took.</h2><p>A favorite shot stays visible on the color e-paper display, ready to come along with you.</p></article></section>'


def _how():
    diagram = '<figure class="kr-camera-controls"><div><img src="/assets/camera-controls.webp" srcset="/assets/camera-controls-640.webp 640w, /assets/camera-controls.webp 960w" sizes="(max-width:700px) calc(100vw - 72px), 44vw" width="960" height="586" loading="lazy" decoding="async" alt="Keeper held in landscape orientation: color e-paper photograph on the left, small viewfinder at upper right, red shutter at lower right"><span class="kr-control-label kr-control-view" aria-hidden="true">1</span><span class="kr-control-label kr-control-shutter" aria-hidden="true">2</span><span class="kr-control-label kr-control-photo" aria-hidden="true">3</span></div><figcaption><span>1 · Small LCD viewfinder</span><span>2 · Red physical shutter</span><span>3 · Color e-paper photograph</span></figcaption></figure>'
    steps = '<ol class="sf-steps"><li><span>01 · FRAME IT</span><h3>Who are you photographing?</h3><p>Raise your camera toward the person or scene. Use the small LCD viewfinder to compose your picture.</p></li><li><span>02 · TAKE IT</span><h3>Make it a photograph.</h3><p>Use the red physical shutter to take the shot. Keeper takes photographs on its own and stores them on microSD.</p></li><li><span>03 · KEEP IT</span><h3>Your shot, still in sight.</h3><p>The larger color e-paper screen gives a photograph you took a paper-like place on the camera.</p></li></ol>'
    return '<section class="sf-section" id="how-it-works">'+_head('The red button takes the photograph','Pick it up. Take a photo.')+'<div class="kr-shooting-layout">'+diagram+steps+'</div>'+'<p class="sf-micro">Frame with the small viewfinder, press the red shutter, then connect directly to your phone when you want to export your photos.</p></section>'


def _epaper():
    return '<section class="sf-section shutter-paper" id="e-paper" data-moment="word-highlight"><div class="wrap"><h2>Meet color e-paper.</h2><p class="mo-wh__text">A photograph stays visible on the matte, paper-like display. Take it along, or give it a place on your desk.</p><p class="sf-micro">Taking photos and updating the display require power. The small viewfinder is a separate IPS LCD. Screen images on this site are simulated.</p></div></section>'


def _moments():
    cards = [('/assets/collections/moment-cafe-friends.webp','Friends spending time at a café','The coffee that became an afternoon.','For the friends who turn an ordinary catch-up into a good day.'),('/assets/collections/moment-neighborhood-couple.webp','A couple walking through a neighborhood','Your favorite person. Any ordinary day.','Not every photograph needs a special occasion.'),('at-home','Keeper in a home setting','A little more you, at home.','A favorite image, with a place among your everyday things.')]
    return '<section class="sf-section">'+_head('FOR LIFE AS IT HAPPENS','The everyday is worth keeping.')+'<div class="sf-moments">'+''.join(f'<article><figure>{_image(src,alt)}</figure><h3>{title}</h3><p>{copy}</p></article>' for src,alt,title,copy in cards)+'</div></section>'


def _specs():
    rows = [('Product','Pocket digital camera'),('Viewfinder','Separate small IPS LCD'),('Photo display','3.7-inch color e-paper'),('Shutter','Physical red shutter button'),('Photo storage','microSD; card inclusion not confirmed'),('Phone required to capture?','No'),('Photo transfer','Connect directly to your phone to export photos.'),('Battery life','Charge twice a year. Actual battery life varies with use.'),('Warranty','Your statutory consumer rights apply in the relevant sales region.'),('Availability','Manufactured and in stock'),('Standard package','Camera, gift box, lanyard, instruction manual')]
    return '<section class="sf-section sf-specs" id="product-details"><div>'+_head('THE DETAILS, CLEARLY','Know your Keeper.')+'<p class="sf-micro">Battery life varies with use. Contact <a href="mailto:support@keeper.day">support@keeper.day</a> for compatibility or order support.</p></div><dl>'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows)+'</dl></section>'


def _faq(c, full=False):
    groups = [('Ordering & shipping', [('Is Keeper available now?','Yes. Keeper is manufactured and in stock. Each standard package includes one camera, a gift box, a lanyard and an instruction manual.'),('What will I pay?',f'The camera and package are {_money(c["price"])} USD, plus {_money(c["shipping"])} worldwide shipping: {_money(c["total"])} USD total. Stripe may offer local-currency pricing with a different converted amount; choose USD to pay the listed USD amount. Contact us about any destination-specific duties before ordering.'),('When will my order arrive?','For United States orders, allow 3 business days for handling and 15 business days in transit, Monday to Friday. For other destinations or a specific delivery date, email support@keeper.day before ordering.')]),('Camera & screen',[('Does it print photos?','No. Your photograph appears on a color e-paper display. Keeper does not make physical prints.'),('Do I need a phone or app?','Keeper takes photos independently and stores them on microSD. Connect it directly to your phone to export photos.'),('What should I know about e-paper?','The main color e-paper screen has a reflective, paper-like appearance that uses the light around you. Taking photographs and changing the displayed image use battery power. The small lower-right display is an IPS LCD, not e-paper.')]),('Returns & help',[('Can I cancel before shipment?',f'Yes. Cancel before shipment for a full refund of {_money(c["total"])} USD. Contact support@keeper.day with your order details.'),('What if I change my mind after delivery?',f'You can return an unused item in its original packaging within 14 days. For change-of-mind returns, the camera price ({_money(c["price"])} USD) is refundable, but the original {_money(c["shipping"])} shipping charge is not; you pay return shipping. The studio pays return shipping for quality issues. See the purchase terms for the full policy.'),('How do I get help?','Email <a href="mailto:support@keeper.day">support@keeper.day</a> with your question and order number if you have one. Ask before purchase if you need a particular technical feature or delivery date.')])]
    groups[0][1].append(('How do I choose an exterior?', 'Choose a look on the product page. ST designs are individual looks. For P designs, select A (left) or B (right); each order contains one camera with the chosen exterior, not two. All choices have the same $199 camera price plus $30 shipping.'))
    if not full:
        pairs = [groups[0][1][1],groups[0][1][2],groups[1][1][0],groups[1][1][1],groups[2][1][1],groups[0][1][-1]]
        groups = [('',pairs)]
    content = ''
    for title,pairs in groups:
        content += '<div class="sf-faq-group">'+(f'<h3>{title}</h3>' if title else '')+''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><div class="sf-answer"><p>{a}</p></div></details>' for q,a in pairs)+'</div>'
    return '<section class="sf-section sf-faq" id="questions"><div>'+_head('Before you order','Questions about Keeper.')+'<a class="sf-link" href="/support.html">All questions &amp; support ↗</a></div><div>'+content+'</div></section>'


def _end(c):
    return f'<section class="sf-section sf-final"><div><p class="sf-kicker">IN STOCK · GIFT BOX INCLUDED</p><h2>Your next photo<br>starts here.</h2></div><div>{_price(c)}{_buy(c,"final")}<p class="sf-micro"><a href="/terms.html">Shipping &amp; returns</a> · <a href="mailto:support@keeper.day">Talk to us</a></p></div></section><aside class="sf-mobile-buy" aria-label="Buy Keeper"><div><strong data-sticky-selection>Keeper · {_money(c["price"])}</strong><span>{_money(c["total"])} USD incl. worldwide shipping</span></div>{_buy(c,"mobile-sticky")}</aside>'


def home_body(commerce):
    c = commerce
    hero = f'''<section class="hero hero--product sf-section shutter-hero" data-enter><div class="hero__head shutter-head"><div><p class="sf-kicker">Keeper · Color e-paper camera</p><h1>Your everyday camera.</h1><p class="sf-lead">Frame your people. Press the red shutter. Keep a photograph in view.</p></div><div class="shutter-order">{_price(c)}{_buy(c,"home-hero")}</div></div><div class="hero__stage shutter-stage" data-enter-media><img src="/assets/campaign/st-46-landscape.webp" srcset="/assets/campaign/st-46-landscape-640.webp 640w, /assets/campaign/st-46-landscape.webp 1270w" sizes="(max-width:700px) calc(100vw - 40px), 70vw" width="1270" height="775" loading="eager" fetchpriority="high" decoding="async" alt="Keeper ST-46 pocket camera, shown in landscape orientation"></div><div class="shutter-foot"><a class="sf-link" href="#how-it-works">How it works <span aria-hidden="true">↓</span></a><p>Camera. Selected exterior. Gift box. Lanyard. Manual.</p><p class="sf-micro">Screen images are simulated.</p></div></section>'''
    featured = '<section class="sf-section shutter-collection" id="camera-looks"><div class="kr-section-top">'+_head('128 exterior choices','A camera in your colors.','Choose a look. The camera stays Keeper.')+'<a class="sf-link" href="/styles.html">See all 128 choices ↗</a></div><div class="kr-design-grid kr-featured">'+''.join(_design_card(DESIGNS[k],c) for k in DATA['featured_designs'])+'</div></section>'
    street = '<section class="sf-section shutter-journal ground-inverse"><div class="wrap"><div class="kr-section-top">'+_head('Take it outside','Your day, in photographs.','Bring a camera for the photographs you want to make along the way.')+'<a class="sf-link" href="/moments.html">See the everyday gallery ↗</a></div><div class="shutter-photo-pair"><figure><img src="/assets/campaign/street-friends.webp" srcset="/assets/campaign/street-friends-480.webp 480w, /assets/campaign/street-friends-960.webp 960w, /assets/campaign/street-friends.webp 1440w" sizes="(max-width:700px) 100vw, 50vw" width="1440" height="960" loading="lazy" decoding="async" alt="Two friends walking together on an American city street"></figure><figure>'+_lifestyle_image(DATA['camera_story'][0])+'</figure></div></div></section>'
    return '<div class="storefront">'+hero+featured+_how()+street+_epaper()+_paired_section(c)+_box(c)+_faq(c)+_end(c)+'</div>'


def product_body(commerce):
    c = commerce
    hero = '<section class="hero sf-section sf-product" data-enter><div class="sf-product-heading"><p class="sf-kicker"><span class="sf-stock-dot" aria-hidden="true"></span> YOUR EVERYDAY CAMERA · IN STOCK</p><h1>Keeper camera.</h1><p class="sf-lead">A pocket camera with a color e-paper display. Frame the people and places you love, use the red shutter, and keep a favorite shot in view.</p></div>'+_gallery()+f'<div class="sf-product-copy">{_style_selector(c)}{_purchase(c,"product-hero")}</div></section>'
    browser = ''
    return '<div class="storefront">'+hero+browser+_how()+_box(c)+_specs()+_epaper()+_faq(c)+_end(c)+'</div>'


def gifting_body(commerce):
    c = commerce
    gift=json.loads((Path(__file__).parent/'editorial-content.json').read_text())['images']['gift']
    hero = f'<section class="hero sf-section sf-hero sf-gift-hero" data-enter><div class="sf-hero-copy"><p class="sf-kicker">FOR THEIR NEXT FAVORITE PHOTOGRAPH</p><h1>Give them<br>a <em>camera.</em></h1><p class="sf-lead">For the birthdays, the people and the everyday adventures they want to photograph. A little Keeper, with a gift box and a look of their own.</p>{_purchase(c,"gifting-hero")}</div><figure class="sf-hero-image" data-enter-media>{_image(gift["image"]+"-1440.webp",gift["alt"],True)}<figcaption>A camera for the photographs you will make together.<br><span class="sf-micro">AI images and screen simulations are shooting references, not camera sample photographs.</span><br><span class="sf-micro">Gift wrapping shown is a styling example. See the included package below.</span></figcaption></figure></section>'
    contexts = '<section class="sf-section sf-gift-contexts">'+_head('YOU KNOW WHO IT’S FOR','Something to make memories with.')+'<div class="sf-steps"><article><span>FOR YOUR PERSON</span><h3>The days you share.</h3><p>An anniversary, a birthday, or just because a favorite face deserves a place nearby.</p></article><article><span>FOR YOUR FRIEND</span><h3>More days like this.</h3><p>For coffee dates, catch-ups and the person who makes ordinary plans worth remembering.</p></article><article><span>FOR YOUR FAMILY</span><h3>A little closer to home.</h3><p>A thoughtful object for someone who loves taking pictures of the people they love.</p></article></div></section>'
    return '<div class="storefront">'+hero+_box(c)+contexts+_how()+_faq(c)+_end(c)+'</div>'


def support_body(commerce):
    intro = '<section class="sf-section sf-support-intro"><div><p class="sf-kicker">HERE TO HELP</p><h1>A question?<br><em>Talk to us.</em></h1><p class="sf-lead">Before you buy, after it arrives, or when you need a little help with your Keeper.</p></div><div class="sf-contact-card"><h2>A real way to reach us.</h2><a class="sf-contact-email" href="mailto:support@keeper.day">support@keeper.day ↗</a><p>Include your order number if you have one. If a delivery date or technical detail matters to you, ask us before placing an order.</p><button class="sf-buy" type="button" id="open-chat" hidden>Chat with us <span aria-hidden="true">↗</span></button><p class="sf-micro" id="chat-status" aria-live="polite"></p><a class="sf-link" href="/terms.html">Read the purchase terms ↗</a></div></section>'
    return '<div class="storefront">'+intro+_faq(commerce,True)+_end(commerce)+'</div>'


def checkout_url(c, variant):
    url = urlsplit(c['checkout_url'])
    query = dict(parse_qsl(url.query))
    query['client_reference_id'] = 'keeper-'+variant
    return urlunsplit((url.scheme,url.netloc,url.path,urlencode(query),url.fragment))


def _design_card(design, c):
    key, paired = design['id'], design['kind'] == 'paired'
    sides = ['a','b'] if paired else ['']
    sizes = '(max-width:700px) calc(100vw - 40px), 48vw' if paired else '(max-width:700px) 46vw, 24vw'
    choices = ''
    for side in sides:
        variant = key+('-'+side if side else '')
        label = ('Side '+side.upper()+(' · left' if side == 'a' else ' · right')) if side else 'Choose this look'
        choices += f'<div class="kr-design-choice"><a class="kr-choose" href="/camera.html?style={variant}#choose-style">{label} ↗</a><a class="kr-quick-buy" data-purchase="design-{variant}" data-variant="{variant}" href="{_e(checkout_url(c,variant))}" aria-label="Buy one {_e(design["name"])} {side.upper()} Keeper, $229 USD including shipping">Buy one · $199</a></div>'
    label = 'A / left · B / right · sold individually' if paired else 'Camera + selected exterior'
    return f'<article class="kr-design-card card" data-design-card data-kind="{design["kind"]}" data-search="{_e(key+" "+design["name"]+" "+design["name_zh"])}"><a class="kr-design-image" href="/camera.html?style={key}{"-a" if paired else ""}#choose-style"><img src="{design["thumb"]}" srcset="{design["thumb"]} 360w, {design["image"]} {design["width"]}w" sizes="{sizes}" alt="{_e(design["name"])} — {key.upper()}{" A and B exterior designs" if paired else " exterior design"}" width="{design["width"]}" height="{design["height"]}" loading="lazy" decoding="async"></a><div class="kr-design-heading"><h3>{_e(design["name"])}</h3><span>{key.upper()}</span></div><p class="kr-design-caption">{label}</p>{choices}</article>'


def design_catalog(c, paired_only=False):
    designs = [d for d in DATA['designs'] if not paired_only or d['kind'] == 'paired']
    classic = '' if paired_only else f'<article class="kr-design-card card" data-design-card data-kind="single"><a class="kr-design-image" href="/camera.html?style=classic#choose-style"><img src="/assets/product-flowers.webp" alt="Classic cream" width="659" height="891" loading="lazy"></a><div class="kr-design-heading"><h3>Classic cream</h3></div><p class="kr-design-caption">Camera + selected exterior</p><div class="kr-design-choice"><a class="kr-choose" href="/camera.html?style=classic#choose-style">Choose this look ↗</a><a class="kr-quick-buy" data-purchase="design-classic" data-variant="classic" href="{_e(c["checkout_url"])}">Buy one · $199</a></div></article>'
    count = 'Two sides. Choose one camera.' if paired_only else 'Eight looks, one camera.'
    return '<section class="sf-section kr-catalog"><h2>'+count+'</h2><div class="kr-design-grid">'+classic+''.join(_design_card(d,c) for d in designs)+'</div></section>'


def styles_body(c, paired_only=False):
    title = 'Sun & moon' if paired_only else 'Eight looks. Pick your favorite.'
    copy = 'Sun & moon: choose A (left) or B (right). Each order includes one camera, not a pair.' if paired_only else 'Classic cream, five individual designs, and two Sun & moon sides. Eight choices in total, with the same camera inside.'
    intro = '<section class="sf-section kr-page-intro"><p class="sf-kicker">CHOOSE YOUR KEEPER</p><h1>'+title+'</h1><p class="sf-lead">'+copy+'</p><p class="kr-price-line"><strong>$199 per camera</strong> + $30 worldwide shipping · $229 USD total</p><div class="kr-intro-links"><a href="/styles.html">All designs</a><a href="/together.html">Paired designs</a><a href="/camera.html">The camera &amp; what’s included</a></div></section>'
    return '<div class="storefront">'+intro+design_catalog(c,paired_only)+_share_section()+_end(c)+'</div>'


def _style_selector(c):
    payload = json.dumps({'variants':DATA['variants'],'checkout':c['checkout_url']},ensure_ascii=False).replace('</','<\\/')
    picks = '<a data-pick-style="classic" href="/camera.html#choose-style"><img src="/assets/product-flowers.webp" alt="Classic cream" width="659" height="891" loading="lazy"><span>Classic cream</span></a>'
    static_buys = f'<li><a href="{_e(c["checkout_url"])}">Classic cream</a></li>'
    for variant in DATA['variants']:
        key, d = variant['id'], DESIGNS[variant['group']]
        side = ' · '+('A · left' if variant['side'] == 'a' else 'B · right') if variant['side'] else ''
        picks += f'<a data-pick-style="{key}" href="/camera.html?style={key}#choose-style"><img src="{d['thumb']}" alt="{_e(d['name'])}" width="{d['width']}" height="{d['height']}" loading="lazy"><span>{key.upper()}</span>'+ (f'<small>{side[3:]}</small>' if side else '')+'</a>'
        static_buys += f'<li><a data-variant="{key}" href="{_e(checkout_url(c,key))}">{key.upper()}</a></li>'
    return f'<div class="kr-selector" id="choose-style" data-style-selector><h2 class="kr-picker-title">Choose from eight looks</h2><p class="kr-selected-name" data-selected-name>Classic cream</p><p class="kr-selection-note" data-selection-note>One camera · classic cream exterior · gift box, lanyard &amp; manual.</p><div class="kr-side-choices" data-side-choices hidden><button type="button" data-pair-side="a">Choose A · left</button><button type="button" data-pair-side="b">Choose B · right</button></div><div class="kr-visual-picks">{picks}</div><p class="kr-selection-status" data-selection-status aria-live="polite"></p><div class="kr-share-actions" hidden><button type="button" data-share-current>Share this look ↗</button><button type="button" data-copy-current>Copy link</button><span data-share-status role="status"></span></div><noscript><p>Without JavaScript, use the named checkout links below. The main purchase button buys Classic cream.</p><ul class="kr-static-checkouts">{static_buys}</ul></noscript><script type="application/json" id="keeper-design-data">{payload}</script></div>'


def _lifestyle_image(scene, eager=False):
    base = '/assets/everyday/'+scene['id']
    alt = scene.get('alt', scene['title']+' — Keeper '+scene['style'].upper()+' in an American everyday setting')
    return f'<img src="{base}.webp" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}.webp 1440w" sizes="(max-width:700px) 100vw, 60vw" width="1440" height="960" alt="{_e(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'


def _lifestyle_section(indices=None):
    scenes = DATA['camera_story']+DATA['lifestyle'] if indices is None else [DATA['lifestyle'][i] for i in indices]
    cards = ''
    for scene in scenes:
        cards += f'<article class="kr-life-card"><a class="kr-life-image" href="/camera.html?style={scene["style"]}#choose-style">{_lifestyle_image(scene)}</a><div class="kr-life-meta"><span>{scene["style"].upper()}</span><a href="/camera.html?style={scene["style"]}#choose-style">Find this look ↗</a></div><h3>{_e(scene["title"])}</h3><p>{_e(scene["copy"])}</p></article>'
    return '<section class="sf-section"><div class="kr-section-top">'+_head('WHAT WILL YOU PHOTOGRAPH TODAY?','The people. The light. The little surprises.','Bring a camera for the photographs you want to make along the way.')+'<a class="sf-link" href="/moments.html">Explore the everyday gallery ↗</a></div><div class="kr-life-grid">'+cards+'</div><p class="sf-micro">Screen images are simulated.</p></section>'


def _paired_section(c):
    return '<section class="sf-section kr-pair-section"><div class="kr-section-top">'+_head('For two photographers','Pick your side.','Choose A (left) or B (right). Each order is one camera, with one exterior.')+'<a class="sf-link" href="/together.html">Explore Sun & moon ↗</a></div><div class="kr-design-grid kr-pair-featured">'+''.join(_design_card(DESIGNS[k],c) for k in DATA['featured_pairs'])+'</div></section>'


def _share_section():
    return '<section class="sf-section kr-share-strip"><div><p class="sf-kicker">KEEP THE GOOD DAYS GOING</p><h2>Who would you take photographing?</h2><p>Share the camera with your next photo-walk partner.</p></div><div class="kr-share-actions" hidden><button type="button" data-share-url="https://keeper.day/styles.html">Share the collection ↗</button><button type="button" data-copy-url="https://keeper.day/styles.html">Copy link</button><span data-share-status role="status"></span></div></section>'


def moments_body(c):
    return '<div class="storefront"><section class="sf-section kr-page-intro"><p class="sf-kicker">EVERYDAY KEEPERS</p><h1>What will you<br><em>photograph today?</em></h1><p class="sf-lead">A friend laughing. Your dog on a walk. The light you nearly missed. Take your camera and make the photograph.</p></section>'+_lifestyle_section()+_share_section()+_end(c)+'</div>'
