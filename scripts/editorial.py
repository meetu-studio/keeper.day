"""Keeper's editorial storefront and static companion pages."""
from html import escape
from pathlib import Path
import json
from storefront import DATA, DESIGNS, _design_card, _price, _buy, _faq, _box, _paired_section, _end, _how, _style_selector

ROOT = Path(__file__).parent
CONTENT = json.loads((ROOT/'editorial-content.json').read_text())
THEMES = [('nature','Nature'),('minimal','Quiet design'),('playful','Playful'),('retro','Retro')]
AI = 'AI-generated placeholder · replace with a real image'
DEMO = 'Illustrative content, not an actual review, publication or partnership.'
DIARY_NOTE = 'AI-created photo ideas · not customer submissions or photographs taken with Keeper.'
DIARY_CATEGORIES = [('friends','Friends'),('family','Family'),('pets','Pets'),('street','On the street'),('outdoors','Outdoors'),('details','Little things')]
DIARY_FEATURED = ['friends-pizza','pets-dog','street-rain','family-birthday','outdoors-lake','friends-rooftop','pets-cat','details-diner']


def diary_cards(ids=None):
    photos = CONTENT['photo_diary']
    if ids is not None:
        photos = [next(p for p in photos if p['id'] == key) for key in ids]
    cards = ''
    for p in photos:
        base = p['image']
        srcset = ', '.join(f'{base}-{w}.webp {w}w' for w in p['sizes'])
        cards += f'<figure class="ed-diary-card" id="photo-{p["id"]}" data-diary-category="{p["category"]}"><a class="ed-diary-image" data-diary-photo="{p["id"]}" href="{base}-full.webp" aria-label="Open photograph"><img src="{base}-960.webp" srcset="{srcset}" sizes="(max-width:700px) 46vw, (max-width:1024px) 30vw, 23vw" width="{p["width"]}" height="{p["height"]}" alt="{escape(p["alt"])}" loading="lazy" decoding="async" data-source="illustration"><span class="ed-diary-zoom" aria-hidden="true">↗</span></a><figcaption><h3>{escape(p["title"])}</h3><p class="ed-diary-caption">{escape(p["caption"])}</p><span class="ed-ai">AI photo example</span></figcaption></figure>'
    return '<div class="ed-diary-grid">'+cards+'</div>'


def diary_section(full=False):
    heading = '' if full else head('PHOTO DIARY','The moments you didn’t plan.','Friends between plans. A dog at the door. A view worth stopping for.','/moments.html#photo-diary','Explore all 12 photographs')
    filters = ''
    if full:
        options = [('all','All photographs')] + DIARY_CATEGORIES
        filters = '<nav class="ed-diary-filters" aria-label="Browse by moment">'+''.join(f'<a href="/moments.html?topic={key}#photo-diary" data-diary-filter="{key}">{label}</a>' for key,label in options)+'</nav><p class="ed-diary-count" data-diary-count role="status" aria-live="polite">12 / 12</p>'
    return '<section class="ed-section ed-diary" id="photo-diary">'+heading+f'<p class="ed-diary-note">{DIARY_NOTE}</p>'+filters+diary_cards(None if full else DIARY_FEATURED)+'</section>'


def diary_dialog():
    first = CONTENT['photo_diary'][0]
    return f'<dialog class="ed-diary-dialog" aria-labelledby="diary-title"><div class="ed-diary-toolbar"><span data-diary-position aria-live="polite"></span><button type="button" data-diary-close aria-label="Close photograph">×</button></div><img data-diary-large src="{first["image"]}-full.webp" width="{first["width"]}" height="{first["height"]}" alt="{escape(first["alt"])}" loading="lazy"><div class="ed-diary-detail"><h2 id="diary-title">{escape(first["title"])}</h2><p data-diary-description>{escape(first["caption"])}</p><p class="ed-diary-note">{DIARY_NOTE}</p><div class="ed-diary-controls"><button type="button" data-diary-prev aria-label="Previous photograph">←</button><button type="button" data-diary-next aria-label="Next photograph">→</button><a class="ed-text-link" data-diary-gallery href="/moments.html#photo-diary">View the photo diary</a></div><div class="kr-share-actions" hidden><button type="button" data-share-url="https://keeper.day/moments.html">Share this photograph</button><button type="button" data-copy-url="https://keeper.day/moments.html">Copy link</button><span data-share-status role="status"></span></div></div></dialog>'


def photo(key, eager=False, cls='', sizes='(max-width:700px) 100vw, 50vw'):
    asset = CONTENT['images'][key]
    base = asset['image']
    srcset = ', '.join(f'{base}-{w}.webp {w}w' for w in [480,960,1440])
    return f'<figure class="ed-photo {cls}"><img src="{base}-1440.webp" srcset="{srcset}" sizes="{sizes}" alt="{escape(asset["alt"])}" width="1440" height="960" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'+ (f'<figcaption class="ed-ai">{AI}</figcaption>' if asset['placeholder'] else '')+'</figure>'


def head(kicker,title,copy='',link='',label='Explore'):
    return f'<div class="ed-section-head"><div><p class="sf-kicker">{kicker}</p><h2>{title}</h2>'+ (f'<p>{copy}</p>' if copy else '')+f'</div>'+ (f'<a class="ed-text-link" href="{link}">{label} <span aria-hidden="true">↗</span></a>' if link else '')+'</div>'


def intro(kicker,title,copy):
    return f'<section class="ed-section ed-intro" data-enter><p class="sf-kicker">{kicker}</p><h1>{title}</h1><p class="ed-lead">{copy}</p></section>'


def demo_form(kind):
    forms = {
        'newsletter': ('Letters from Keeper', [('Email address','email')]),
        'membership': ('Join the photo circle', [('Your name','text'),('Email address','email')]),
        'registration': ('Register your Keeper', [('Your name','text'),('Email address','email'),('Order number','text'),('Your exterior number','text')]),
        'partnership': ('Work with Meetu Studio', [('Your name','text'),('Email address','email'),('Company or project','text'),('Tell us about your idea','textarea')])
    }
    title, fields = forms[kind]
    controls=''
    for i,(label,typ) in enumerate(fields):
        name=f'preview-{kind}-{i}'
        field=f'<textarea id="{name}" rows="3"></textarea>' if typ=='textarea' else f'<input id="{name}" type="{typ}" autocomplete="off">'
        controls+=f'<label for="{name}">{label}{field}</label>'
    return f'<div class="ed-demo" id="{kind}"><h3>{title}</h3><p class="ed-status">Preview only · not open yet</p><form data-demo-form aria-label="{title}"><fieldset disabled>{controls}<label class="ed-check"><input type="checkbox">I would like to receive Keeper news.</label><button type="button" disabled>Not open yet</button></fieldset></form><p class="ed-small">This preview does not collect or submit information.</p><a class="ed-text-link" href="mailto:support@keeper.day">Contact us by email ↗</a></div>'


GUIDES = [
    {'id':'first-photo','title':'Your first photograph with Keeper','image':'hero','summary':'Find the viewfinder, frame your subject and use the red shutter.','parts':[
        ('Start with the person, not the settings.','Choose someone or something you want to remember. Look for steady, comfortable light and a background that gives your subject some space.'),
        ('Use the small screen to frame.','Hold Keeper so that the camera faces your subject. The small IPS LCD is the viewfinder; the larger color e-paper screen is for the photograph. Keep your fingers away from the screens and hold the camera steadily.'),
        ('Take the photograph with the red shutter.','Use the red physical shutter to take your picture. Keeper can take photographs without a phone. Refer to the included manual for the controls on your particular camera; this guide does not assume a press-and-release shortcut.'),
        ('Let a photograph stay with you.','Photos are stored on microSD. A photograph on the color e-paper display can remain in sight while you carry the camera or put it on your desk. The image is displayed on the camera, not printed onto paper.'),
        ('Before a trip or a gift.','Check your card, power and operation before heading out. Card inclusion, supported storage, transfer and charging details should be confirmed with support rather than inferred from a website photograph.') ]},
    {'id':'photo-walk','title':'Take your camera for a walk','image':'street','summary':'A small route, a familiar face and something you almost walked past.','parts':[
        ('Choose an easy route.','A familiar street, campus path or neighborhood park is enough. Leave time to stop. Notice a patch of light, a doorway or a friend turning around instead of trying to cover every place.'),
        ('Make a three-photo story.','Photograph the place, the person and one small detail. A wide view gives context; a closer view shows what caught your attention. You do not need a special occasion to make a small set of photographs.'),
        ('Let people be themselves.','Ask before photographing someone. Make room for a conversation or a laugh, and keep the camera ready without asking everyone to pose. For pets, let the animal come to a comfortable position.'),
        ('Carry it with care.','Use the supplied lanyard according to the included manual. Keep the camera away from water and rough handling; this guide does not claim a waterproof rating or a tested drop resistance.'),
        ('Choose a photograph to keep nearby.','Back at home, choose the picture that brings you back to that walk. The color e-paper display gives it a place on the camera while the rest of the photographs remain on your storage card.') ]},
    {'id':'epaper','title':'Get to know color e-paper','image':'studio','summary':'Why the photograph looks different from the small viewfinder.','parts':[
        ('Two screens, two jobs.','The small IPS LCD helps you compose the shot. The 3.7-inch color e-paper display gives a photograph a larger, paper-like place on the camera. They use different display technologies.'),
        ('A photograph in the light around you.','Color e-paper has a reflective, matte appearance. Its appearance depends on the surrounding light. The photographs on this website illustrate the idea and are not calibrated camera samples.'),
        ('Still means still.','The displayed photograph is a static image. It does not play video or glow like a backlit screen. Keeping an unchanged e-paper image does not require the same continuous refreshing as an LCD.'),
        ('Keeping a picture is not taking a picture.','Taking photographs and changing the displayed image require power. Image retention does not mean the whole camera can run forever without charging. We do not publish an untested battery-life figure.'),
        ('A camera that comes home with you.','After photographing friends, take that same camera home and keep a favorite image nearby. Desk placement is part of living with the camera, not a promise of connected apps or automatic reminders.') ]}
]


def guide_cards():
    return '<div class="ed-grid ed-three">'+''.join(f'<article><a class="ed-image-link" href="/guide-{g["id"]}.html">{photo(g["image"])}<span class="ed-small">FIELD NOTES</span><h3>{g["title"]}</h3></a><p>{g["summary"]}</p><a class="ed-text-link" href="/guide-{g["id"]}.html">Read the guide ↗</a></article>' for g in GUIDES)+'</div>'


def newsletter():
    return '<section class="ed-section ed-newsletter">'+head('KEEP IN TOUCH','A little more photography in your inbox.','Photo ideas, exterior collections and notes from the studio. The signup below is a preview.')+demo_form('newsletter')+'</section>'


def service_strip():
    rows=[('Official online store','Buy directly from keeper.day.','/owners.html#where-to-buy'),('$30 worldwide shipping','One camera, one selected exterior.','/terms.html'),('Clear return terms','14-day unused returns, with conditions.','/terms.html'),('Here to help','Reach the studio before or after an order.','/support.html')]
    return '<section class="ed-section ed-services" id="services"><h2 class="sf-sr-only">Buying and support</h2>'+''.join(f'<a href="{u}"><h3>{t}</h3><p>{c}</p><span aria-hidden="true">↗</span></a>' for t,c,u in rows)+'</section>'


def reviews():
    cards=''
    for i,item in enumerate(CONTENT['reviews']):
        cards+=f'<article>{photo(item["image"],sizes="(max-width:700px) 100vw, 33vw")}{"<p class=ed-status>AI-generated review example · not a customer review</p>" if item["placeholder"] else ""}<blockquote>{escape(item["quote"])}</blockquote><p class="ed-small">{escape(item["name"])}</p></article>'
    return '<section class="ed-section" id="review-examples">'+head('PEOPLE & PHOTOGRAPHS','Everyday camera stories.','These AI-written examples pair a person, a Keeper camera and a reason to take a photograph. They are not customer testimonials.')+'<div class="ed-grid ed-three ed-reviews">'+cards+'</div></section>'


def press_cards():
    return '<div class="ed-grid ed-three">'+''.join(f'<article><a class="ed-image-link" href="/press.html#{item["id"]}">{photo(item["image"],sizes="(max-width:700px) 100vw, 33vw")}<h3>{escape(item["title"])}</h3></a><p>{escape(item["summary"])}</p>{"<p class=ed-status>AI-generated editorial example · not a published article</p>" if item["placeholder"] else ""}<a class="ed-text-link" href="/press.html#{item["id"]}">Read the example ↗</a></article>' for item in CONTENT['press'])+'</div>'


def logos():
    marks=''
    for item in CONTENT['logos']:
        label='<br><span>AI placeholder</span>' if item['placeholder'] else ''
        marks+=f'<figure><a href="{item["href"]}"><img src="{item["image"]}" alt="{escape(item["alt"])}" width="600" height="400" loading="lazy"></a><figcaption><strong>{escape(item["name"])}</strong><br>{escape(item["description"])}{label}</figcaption></figure>'
    return '<div class="ed-logos">'+marks+'</div>'


def social_wall():
    return diary_cards([p['id'] for p in CONTENT['photo_diary'] if p['id'] not in DIARY_FEATURED])+'<div class="ed-social-status"><span>Instagram · account to be added</span><span>TikTok · account to be added</span><span>YouTube · account to be added</span></div>'


def home_body(c):
    hero='<section class="ed-section ed-hero hero" data-enter><div class="ed-hero-copy"><p class="sf-kicker">A pocket camera with a color e-paper display.</p><h1>A photo that takes photos.</h1><p class="ed-lead">Frame your favorite people. Press the red shutter. Carry the photograph with you.</p><div class="ed-hero-product"><img src="/assets/campaign/st-46-landscape-640.webp" width="640" height="391" alt="Keeper ST-46 camera with its original printed exterior"><div><strong>Keeper camera</strong><span>In stock · gift box included</span></div></div><div class="shutter-order">'+_price(c)+_buy(c,'home-hero')+'</div><a class="ed-text-link" href="/guide-first-photo.html">See how to take a photo ↓</a></div><div class="ed-hero-visual" data-enter-media>'+photo('hero',True)+'</div></section>'
    routes=[('The camera','/camera.html','/assets/product-flowers.webp','One small camera.'),('Your exterior','/styles.html','/assets/designs/st-50.webp','128 ways to make it yours.'),('A paired look','/together.html','/assets/designs/p-13.webp','Choose A or B, one camera each.'),('Ready to give','/gifting.html','/assets/storefront/full-kit-720.webp','Gift box, lanyard and manual included.')]
    shop='<section class="ed-section ed-shop" id="shop"><h2 class="sf-sr-only">Explore Keeper</h2><div class="ed-grid ed-four">'+''.join(f'<a class="ed-shop-tile card" href="{u}"><img src="{im}" alt="{t}" width="640" height="480" loading="lazy"><h3>{t} <span aria-hidden="true">↗</span></h3><p>{copy}</p></a>' for t,u,im,copy in routes)+'</div></section>'
    facts='<section class="ed-facts" aria-label="Camera essentials">'+''.join(f'<div><img src="/assets/editorial/detail-{['camera','shutter','viewfinder','paper'][i]}.webp" alt="{t}" width="480" height="300" loading="lazy"><span class="ed-fact-number">0{i+1}</span><h2>{t}</h2><p>{copy}</p></div>' for i,(t,copy) in enumerate([('Take photos independently','A camera that can take photographs without a phone.'),('A real red shutter','A physical button for taking the picture.'),('A separate viewfinder','Compose with the small IPS LCD.'),('Color e-paper','Keep a photograph visible on the camera.')]))+'</section>'
    previews=''
    for key in DATA['featured_designs']:
        d=DESIGNS[key]
        previews+=f'<article data-look-panel="{key}"><img src="{d["image"]}" alt="{escape(d["name"])}" width="{d["width"]}" height="{d["height"]}" loading="lazy"><div><p>{key.upper()}</p><h3>{escape(d["name"])}</h3><a class="sf-buy" href="/camera.html?style={key}#choose-style">Choose this look ↗</a></div></article>'
    look='<section class="ed-section ed-looks" id="camera-looks">'+head('YOUR CAMERA, YOUR LOOK','Choose the one that feels like you.','The same Keeper camera, with your selected exterior.','/styles.html','All 128 choices')+'<div class="ed-look-layout"><div class="ed-look-panels">'+previews+'</div><div class="ed-look-options">'+''.join(f'<a class="ed-look-option" data-look="{key}" href="/camera.html?style={key}#choose-style"><img src="{DESIGNS[key]["thumb"]}" alt="" width="360" height="480" loading="lazy"><span>{escape(DESIGNS[key]["name"])}</span><small>{key.upper()}</small></a>' for key in DATA['featured_designs'])+'</div></div><div class="ed-theme-links">'+''.join(f'<a href="/styles.html?collection={key}">{label} <span aria-hidden="true">↗</span></a>' for key,label in THEMES)+'</div></section>'
    shooting='<section class="ed-section" id="how-it-works">'+head('THE FIRST PHOTOGRAPH','See it. Frame it. Take it.','A few ordinary actions make a photograph yours.','/guide-first-photo.html','Your first-photo guide')+'<div class="ed-grid ed-three">'+''.join(f'<article>{photo(im)}<p class="ed-small">{num}</p><h3>{title}</h3><p>{copy}</p></article>' for im,num,title,copy in [('hero','01','Find your frame.','Raise the camera toward the person or place and compose with the small viewfinder.'),('shutter','02','Press the red shutter.','Hold the camera steadily and use the physical shutter to take the photograph.'),('result','03','Keep the photograph in sight.','Give a favorite image a paper-like place on the larger color e-paper display.')])+'</div></section>'
    paper='<section class="ed-section ed-paper" id="e-paper"><div>'+head('THE PHOTOGRAPH STAYS','A little piece of the day, still here.','After the walk, the photograph comes home with you.')+'<p>The 3.7-inch color e-paper display is matte and reflective. The small viewfinder and the larger photo display have different jobs.</p><p>Taking photos and updating the display require power. Keeper displays photographs; it does not make paper prints.</p><a class="ed-text-link" href="/guide-epaper.html">Get to know color e-paper ↗</a></div><div>'+photo('epaper-triptych')+'<p class="ed-small">The same static photograph in three everyday places. Screen images are simulated.</p></div></section>'
    daily='<section class="ed-section" id="everyday">'+head('MAKE TIME FOR A PHOTOGRAPH','There is something worth keeping in an ordinary day.','','/moments.html','More photo stories')+'<div class="ed-mosaic">'+''.join(f'<a href="/moments.html#{key}">{photo(key)}<h3>{title}</h3></a>' for key,title in [('street','A walk with your people.'),('campus','The people you meet along the way.'),('family','A birthday at home.'),('pets','The face you always photograph.'),('cafe','Stay for another coffee.'),('trail','Take the longer way back.')])+'</div></section>'
    finder='<section class="ed-section ed-finder-callout"><div><p class="sf-kicker">A LITTLE HELP CHOOSING</p><h2>Which Keeper looks like you?</h2><p>Choose a mood, see three exteriors together, and find your favorite. Every choice has the same camera inside.</p></div><a class="sf-buy" href="/find-your-keeper.html">Find your Keeper ↗</a></section>'
    gift='<section class="ed-section ed-gift-intro"><div>'+photo('gift')+'</div><div>'+head('GIVE THEM THEIR NEXT PHOTOGRAPH','A camera for someone you know well.','For the friend who comes on every walk, the person across the table, or the family photographer.')+'<a class="sf-buy" href="/gifting.html">Explore gifting ↗</a><p class="ed-small">One camera with your selected exterior, gift box, lanyard and instruction manual.</p></div></section>'+_paired_section(c)+_box(c)
    media='<section class="ed-section" id="media">'+head('IN THE PICTURE','Media & creative company.',DEMO,'/press.html','Media & partnerships')+press_cards()+logos()+'</section>'
    education='<section class="ed-section" id="field-notes">'+head('FIELD NOTES','Go out with a little more inspiration.','','/learn.html','All photography guides')+guide_cards()+updates()+'</section>'
    brand='<section class="ed-section ed-brand"><div>'+photo('studio')+'</div><div>'+head('MEETU STUDIO · KEEPER.DAY','Made around the photograph.','We want the camera to come along, and a photograph to stay in sight.')+'<p>Keeper brings a physical shutter, a paper-like photo display and an exterior of your own into one small camera.</p><a class="ed-text-link" href="/about.html">Why we made Keeper ↗</a></div></section>'
    community='<section class="ed-section" id="community">'+head('THE PHOTO CIRCLE','A few more things to photograph.','A slow breakfast, another try, a detour and flowers on the way home.','/moments.html#membership','Explore the photo circle')+f'<p class="ed-diary-note">{DIARY_NOTE}</p>'+social_wall()+'<div class="kr-share-actions" hidden><button type="button" data-share-url="https://keeper.day/moments.html">Share the everyday gallery ↗</button><button type="button" data-copy-url="https://keeper.day/moments.html">Copy link</button><span data-share-status role="status"></span></div></section>'
    return '<div class="storefront editorial">'+hero+shop+diary_section()+facts+look+shooting+paper+daily+finder+gift+reviews()+media+education+brand+community+service_strip()+_faq(c)+newsletter()+_end(c)+diary_dialog()+'</div>'


def updates():
    items=[('Four languages, one Keeper.','Read the site in English, Chinese, Japanese or Korean.','/owners.html#site-updates'),('128 exterior choices.','Explore 68 individual designs and 30 pairs.','/styles.html'),('A new set of field notes.','Three guides for your first photographs and everyday walks.','/learn.html')]
    return '<div class="ed-updates" id="studio-updates"><h3>From the studio</h3>'+''.join(f'<a href="{u}"><time datetime="2026-11-09">2026.11.09</time><div><strong>{t}</strong><p>{copy}</p></div><span aria-hidden="true">↗</span></a>' for t,copy,u in items)+'</div>'


def finder_body(c):
    controls='<div class="ed-finder-controls" hidden><fieldset><legend>1. One look or a paired look?</legend><label><input type="radio" name="kind" value="single" checked>Individual designs</label><label><input type="radio" name="kind" value="paired">Paired designs</label></fieldset><fieldset><legend>2. Choose your mood.</legend>'+''.join(f'<label><input type="radio" name="theme" value="{key}"'+(' checked' if key=='nature' else '')+f'>{label}</label>' for key,label in THEMES)+'</fieldset></div>'
    groups=''
    for kind in ['single','paired']:
        for theme,label in THEMES:
            cards=''.join(_design_card(DESIGNS[k],c) for k in CONTENT['recommendations'][kind][theme])
            groups+=f'<section class="ed-finder-results" data-finder-group="{kind}:{theme}" id="{kind}-{theme}"><h2>{label}</h2><p>{"Individual designs" if kind=="single" else "Paired designs · select A or B, one camera per order"}</p><div class="kr-design-grid ed-three">{cards}</div></section>'
    return '<div class="storefront editorial">'+intro('FIND YOUR KEEPER','A look for the photographs you make.','Two choices, three suggestions. Compare the exteriors; the camera, included package and price stay the same.')+'<section class="ed-section ed-finder" data-finder>'+controls+'<p class="ed-small">One Keeper camera with the selected exterior · $199 + $30 shipping = $229 USD.</p>'+groups+'</section>'+service_strip()+_end(c)+'</div>'


def learn_body(c):
    return '<div class="storefront editorial">'+intro('FIELD NOTES','A camera. A little curiosity.','Start with the basics, take a walk and get to know the photograph on your camera.')+'<section class="ed-section">'+guide_cards()+updates()+'</section>'+_how()+newsletter()+_end(c)+'</div>'


def guide_body(c, slug):
    g=next(g for g in GUIDES if g['id']==slug)
    contents='<nav class="ed-article-index" aria-label="In this guide">'+''.join(f'<a href="#step-{i}">{title}</a>' for i,(title,copy) in enumerate(g['parts'],1))+'</nav>'
    article=''.join(f'<section id="step-{i}"><p class="ed-small">0{i}</p><h2>{title}</h2><p>{copy}</p></section>' for i,(title,copy) in enumerate(g['parts'],1))
    return '<div class="storefront editorial">'+intro('FIELD NOTES',g['title'],g['summary'])+'<div class="ed-article-hero">'+photo(g['image'],True)+'</div><div class="ed-article-layout">'+contents+'<article class="ed-article">'+article+'<p class="ed-small">Illustrative images. Refer to the included manual for the controls on your camera.</p><a class="ed-text-link" href="/support.html">A question about your camera? ↗</a></article></div><section class="ed-section">'+head('KEEP EXPLORING','Your next photo walk.')+guide_cards()+'</section>'+_end(c)+'</div>'


def about_body(c):
    return '<div class="storefront editorial">'+intro('MEETU STUDIO · KEEPER.DAY','For the photograph you want to keep close.','Keeper is a pocket camera with a color e-paper display. Its story starts with taking a photograph.')+'<section class="ed-section ed-brand">'+photo('studio',True)+'<div><h2>Start with a moment.</h2><p>A friend turning around, a familiar face across the table, a pause on a walk. We build the story of Keeper around the person taking that photograph.</p><h2>Let the photograph stay.</h2><p>The red shutter is for taking the picture. The paper-like display gives a photograph a place on the camera afterward. Carry it out, bring it home, keep it nearby.</p><h2>Make the camera your own.</h2><p>Different exteriors leave room for different tastes. The original camera structure stays the same across individual and paired designs.</p></div></section>'+head('WHY KEEPER','Small enough to come along.','The camera, the person and the photograph belong in the same story.')+'<section class="ed-section">'+photo('carry')+'</section>'+service_strip()+newsletter()+_end(c)+'</div>'


def press_body(c):
    stories=''
    for item in CONTENT['press']:
        stories+=f'<section class="ed-section ed-brand" id="{item["id"]}">{photo(item["image"])}<div>{"<p class=ed-status>AI-generated editorial example · not a published article</p>" if item["placeholder"] else ""}<h2>{escape(item["title"])}</h2><p>{escape(item["summary"])}</p><p>{escape(item["body"])}</p><p class="ed-small">This is a layout example. Its image, publication name, text and link will be replaced together when real coverage is available.</p></div></section>'
    ideas=['Make portraits of classmates, photograph the campus walk and share the story behind one picture.','Plan a short local route with three stops: a portrait, a small detail and a photograph together.','Show original artwork beside a selected Keeper exterior and tell the artist’s process, once a real collaboration is agreed.']
    concepts='<section class="ed-section"><p class="ed-status">These fictional identities illustrate possible Keeper stories and collaboration formats. No partnership is announced.</p><div class="ed-grid ed-three">'+''.join(f'<article id="concept-{i+4}"><h2>{escape(item["name"])}</h2><p>{escape(item["description"])}</p><p>{escape(ideas[i])}</p></article>' for i,item in enumerate(CONTENT['logos'][3:]))+'</div></section>'
    return '<div class="storefront editorial">'+intro('MEDIA & PARTNERSHIPS','A place for future conversations.',DEMO)+logos()+stories+concepts+'<section class="ed-section ed-brand" id="partnerships"><div><h2>Make something together.</h2><p>Photo walks, editorial stories and thoughtful gifts are possible starting points. This contact form is a preview; use our email for a real conversation.</p><p class="ed-status">AI partner marks above are examples, not confirmed partnerships.</p></div>'+demo_form('partnership')+'</section>'+_end(c)+'</div>'


def owners_body(c):
    return '<div class="storefront editorial">'+intro('FOR YOUR KEEPER','Your camera, from the first photograph onward.','Find the guides, understand your package and reach us when you need help.')+'<section class="ed-section ed-brand"><div><h2>Start with your first photograph.</h2><p>Keep the included manual with your camera. Our field notes introduce the viewfinder, shutter and e-paper display, while support can help with your particular order.</p><a class="ed-text-link" href="/guide-first-photo.html">Open the first-photo guide ↗</a><h2>Need a hand?</h2><p>For card compatibility, charging, transferring photos or a delivery date, contact us before relying on a particular feature or schedule.</p><a class="ed-text-link" href="mailto:support@keeper.day">support@keeper.day ↗</a></div>'+demo_form('registration')+'</section><section class="ed-section" id="where-to-buy">'+head('OFFICIAL CHANNEL','Buy directly from keeper.day.','This website is the current official purchase channel. No offline retailer list is announced here.')+'<a class="sf-buy" href="/camera.html#choose-style">Shop the camera ↗</a></section><section class="ed-section" id="site-updates">'+updates()+'</section>'+_faq(c)+_end(c)+'</div>'


def moments_body(c):
    titles={'hero':'Photograph your people.','street':'A walk with your people.','cafe':'Stay for another coffee.','campus':'The people you meet along the way.','pets':'The face you always photograph.','carry':'Bring the camera along.','gift':'Give them their next photograph.','studio':'Bring a photograph home.','family':'A birthday at home.','trail':'Take the longer way back.'}
    stories=''.join(f'<article id="{key}">{photo(key)}<h2>{title}</h2><p>{CONTENT["images"][key]["story"]}</p><a class="ed-text-link" href="/camera.html?style={CONTENT["images"][key]["style"]}#choose-style">Find this look ↗</a></article>' for key,title in titles.items())
    return '<div class="storefront editorial">'+intro('PHOTO DIARY','Everyday photographs, worth a second look.','A small album of the people, places and little things you could bring Keeper along to photograph.')+diary_section(True)+head('THE CAMERA COMES ALONG','From the photograph to the camera.','See how a Keeper camera can come along for these everyday moments.')+'<section class="ed-section ed-story-grid">'+stories+'</section><section class="ed-section ed-brand">'+demo_form('membership')+'<div><h2>Share a photo-walk idea.</h2><p>The photo circle is a preview of future community content. There is no active membership, rewards program or account signup yet.</p><div class="kr-share-actions" hidden><button type="button" data-share-url="https://keeper.day/moments.html">Share the everyday gallery ↗</button><button type="button" data-copy-url="https://keeper.day/moments.html">Copy link</button><span data-share-status role="status"></span></div></div></section>'+newsletter()+_end(c)+diary_dialog()+'</div>'
