#!/usr/bin/env python3
"""keeper.day home page (index.html) and product page (camera.html) in English, Chinese, Japanese and Korean,
the 2026-11-20 redesign, written from scripts/redesign/copy/<lang>.json.

    python3 scripts/redesign/build.py

English goes to the site root, the others to /zh/, /ja/ and /ko/. The rest of the site (guides, support,
terms, privacy, about, gifting) still comes from scripts/build_site.py, which since this redesign writes its
own version of these two pages beside them as index-20261111.html and camera-20261111.html (AGENTS.md: add,
never overwrite). Every path is root-relative, as on the rest of the site.

The new pages keep the live site's working parts: the consent banner and the optional analytics and chat
(consent.js and the tracking block in scripts/components.json), the language routing (language.js and the
keeper-i18n packet), the script policy, canonical and hreflang links, and the Product data. The copy files
are trusted HTML: strings go into text as written (so &#8209; and &copy; work) and are escaped only inside
attributes.

The first version of this design, the candidate kept beside the old site, is in the vault folder
redesign-20261120/ of the working copy that holds the other uncommitted work; it is not part of the site.
"""
import hashlib
import json
import re
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parents[2]                 # the site root (this file: scripts/redesign/build.py)
COPY = Path(__file__).resolve().parent / 'copy'
ORIGIN = 'https://keeper.day'
COMMERCE = json.loads((SITE / 'scripts/commerce.json').read_text(encoding='utf-8'))
CHECKOUT = 'https://buy.stripe.com/4gM7sK5cwdrh09Oe1Q6kg01?locale={}'
INITIAL = 'st-50'
# the live site's script policy and its optional services (analytics, ads, chat), loaded only after consent
SCRIPT_POLICY = re.search(r'^SCRIPT_POLICY = "(.*)"$', (SITE / 'scripts/build_site.py').read_text(encoding='utf-8'), re.M).group(1)
TRACKING = json.loads((SITE / 'scripts/components.json').read_text(encoding='utf-8'))['tracking']
# 2026-11-20: brighter commercial versions of these photos, picked one by one by the owner
# (20 from Codex, the self-portrait from Gemini). The old files stay where they are for the
# rest of the site and for comparison; only these pages point at the new ones.
REFRESHED = {old: 'redesign/photos-20261120/' + new for old, new in {
    'editorial/20261109-shooting/cafe-1440.webp': 'cafe-1440.webp',
    'editorial/20261109-shooting/carry-1440.webp': 'carry-1440.webp',
    'editorial/20261109-shooting/epaper-triptych-1440.webp': 'epaper-triptych-1440.webp',
    'editorial/20261109-shooting/family-1440.webp': 'family-1440.webp',
    'everyday/02-photograph-your-people.webp': 'family-1440.webp',
    'everyday/05-workdesk.webp': 'workdesk-1440.webp',
    'inspiration/20261110/01-self-portrait-960.webp': '01-self-portrait-960.webp',
    'inspiration/20261110/03-favorite-people-1440.webp': '03-favorite-people-1440.webp',
    'inspiration/20261110/04-color-walk-1440.webp': '04-color-walk-1440.webp',
    'inspiration/20261110/05-two-perspectives-960.webp': '05-two-perspectives-960.webp',
    'inspiration/20261110/06-your-city-960.webp': '06-your-city-960.webp',
    'inspiration/20261110/07-love-story-1440.webp': '07-love-story-1440.webp',
    'inspiration/20261110/08-new-beginnings-960.webp': '08-new-beginnings-960.webp',
    'inspiration/20261110/09-graduation-news-960.webp': '09-graduation-news-960.webp',
    'inspiration/20261110/10-thank-you-960.webp': '10-thank-you-960.webp',
    'inspiration/20261110/20-gift-a-memory-1440.webp': '20-gift-a-memory-1440.webp',
    'inspiration/20261110/25-frame-the-day-1440.webp': '25-frame-the-day-1440.webp',
    'inspiration/20261110/26-holiday-memory-1440.webp': '26-holiday-memory-1440.webp',
    'storefront/at-home.webp': 'at-home-1440.webp',
    'storefront/gift-box.webp': 'gift-box-1440.webp',
    'storefront/gift-opening.webp': 'gift-opening-1440.webp',
    'storefront/in-the-hand.webp': 'in-the-hand-1440.webp',
}.items()}
# 2026-11-20, later the same day: the owner asked for no Black people in the photos. The recast versions they
# picked sit beside the bright ones in redesign/photos-20261120-recast/ and win where a file exists there.
RECAST = lambda path: path.replace('/photos-20261120/', '/photos-20261120-recast/', 1)
REFRESHED = {old: RECAST(new) if (SITE / 'assets' / RECAST(new)).exists() else new for old, new in REFRESHED.items()}
# the home page's share image is cut from the 03 photo, so it is recast with it
# 2026-11-20, evening: the owner found the home photos lacked desire and picked three samples that show Keeper big and new,
# its six-colour screen at full colour. New files in redesign/home-20261120/; used where they exist, the old ones stay:
# the hero (Porcelain White, thumb on the shutter), step 2 of #how (the red shutter close up) and the order frame's
# first picture (all eight looks; clicking a look still shows that one look). Their alt texts are new keys ending _20261120.
HOME_NEW = SITE / 'assets/redesign/home-20261120'
HOME_HERO = (HOME_NEW / 'hero-classic-1440.webp').exists()
HOME_SHUTTER = (HOME_NEW / 'shutter-1440.webp').exists()
HOME_ALL_LOOKS = (HOME_NEW / 'looks-all-1080.webp').exists()
HOME_SHARE = 'share-20261120.jpg' if (SITE / 'assets/redesign/share-20261120.jpg').exists() else 'share.jpg'

LANGS = {
    'en': {'dir': '', 'html': 'en', 'stripe': 'en', 'label': 'English', 'short': 'EN', 'font': ''},
    'zh': {'dir': 'zh', 'html': 'zh-Hans', 'stripe': 'zh', 'label': '中文', 'short': '中文', 'font': 'Noto+Serif+SC'},
    'ja': {'dir': 'ja', 'html': 'ja', 'stripe': 'ja', 'label': '日本語', 'short': '日本語', 'font': 'Noto+Serif+JP'},
    'ko': {'dir': 'ko', 'html': 'ko', 'stripe': 'ko', 'label': '한국어', 'short': '한국어', 'font': 'Noto+Serif+KR'},
}

# words the live pages already use, verbatim, so the new pages say the same thing in the same place:
# the consent banner, the footer's cookie and chat controls, and the Product data for search engines
LIVE = {
    'en': {'privacy_aria': 'Privacy choices',
           'consent': 'Optional cookies enable analytics and chat. Checkout works with essential cookies.',
           'details': 'Privacy details', 'decline': 'Essential only', 'allow': 'Allow optional',
           'cookies': 'Cookie settings', 'chat': 'Live chat',
           'product': 'Keeper pocket color e-paper camera',
           'product_description': 'Pocket digital camera with a small viewfinder, physical red shutter, color e-paper photo display, gift box, lanyard and instruction manual.'},
    'zh': {'privacy_aria': '隐私选择',
           'consent': '可选 Cookie 用于分析与聊天。仅使用必要 Cookie 也能结账。',
           'details': '隐私详情', 'decline': '仅必要服务', 'allow': '允许可选服务',
           'cookies': 'Cookie 设置', 'chat': '在线聊天',
           'product': 'Keeper 随身彩色墨水屏照相机',
           'product_description': '随身数码相机，配有小取景屏、红色实体快门和彩色墨水屏照片显示，含礼盒、挂绳和说明书。'},
    'ja': {'privacy_aria': 'プライバシーの選択',
           'consent': '任意の Cookie はアクセス解析とチャットに使用します。必須 Cookie のみでも購入できます。',
           'details': 'プライバシーの詳細', 'decline': '必須サービスのみ', 'allow': '任意のサービスを許可',
           'cookies': 'Cookie 設定', 'chat': 'チャット',
           'product': 'Keeper カラー電子ペーパーポケットカメラ',
           'product_description': '小さなファインダー、赤い物理シャッター、カラー電子ペーパーの写真表示を備えたポケットデジタルカメラ。ギフトボックス、ストラップ、説明書付き。'},
    'ko': {'privacy_aria': '개인정보 선택',
           'consent': '선택 쿠키는 분석과 채팅에 사용됩니다. 필수 쿠키만으로도 결제할 수 있습니다.',
           'details': '개인정보 안내', 'decline': '필수 서비스만', 'allow': '선택 서비스 허용',
           'cookies': '쿠키 설정', 'chat': '실시간 채팅',
           'product': 'Keeper 컬러 전자종이 포켓 카메라',
           'product_description': '소형 뷰파인더, 빨간 물리 셔터, 컬러 전자종이 사진 화면을 갖춘 포켓 디지털 카메라. 선물 상자, 스트랩, 설명서 포함.'},
}

# the eight looks on sale, in the live site's order; where each picture lives and its size.
# 'site' pictures are the site's /assets/, 'own' ones this design's /assets/redesign/.
# bg: the render's own ground, so a picture shown whole (contain) has no visible edge
LOOKS = [
    ('classic', 'site', 'product-flowers.webp', 'product-flowers.webp', 659, 891, '#f7f5f2'),
    ('st-12', 'site', 'designs/st-12.webp', 'designs/st-12-360.webp', 720, 960, '#e2e1e1'),
    ('st-27', 'site', 'designs/st-27.webp', 'designs/st-27-360.webp', 720, 960, '#e7e7e7'),
    ('st-31', 'site', 'designs/st-31.webp', 'designs/st-31-360.webp', 720, 960, '#e4e3e3'),
    ('st-42', 'site', 'designs/st-42.webp', 'designs/st-42-360.webp', 720, 960, '#e6e5e8'),
    ('st-50', 'site', 'designs/st-50.webp', 'designs/st-50-360.webp', 720, 960, '#e3e1e0'),
    ('p-01-a', 'own', 'p-01-a.webp', 'p-01-a.webp', 480, 640, '#e6e5e8'),
    ('p-01-b', 'own', 'p-01-b.webp', 'p-01-b.webp', 480, 640, '#e5e5e7'),
]
NAV_CARDS = ['st-50', 'st-12', 'p-01-b', 'classic']
CUR = ' aria-current="true"'

ARROW = ('<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/>'
         '<path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>')
CHEV = ('<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

BRAND = """:root {
  --p-bg: #f5f1ea; --p-surface: #ebe4d8; --p-ink: #1d1b17; --p-muted: #66635e;
  --p-accent: #d23324; --p-accent-ink: #ffffff; --p-action: #d23324; --p-action-ink: #ffffff;
  --p-inv-bg: #1d1b17; --p-inv-surface: #292723; --p-inv-ink: #f5f1ea; --p-inv-muted: #9b9892;
  --p-inv-accent: #d23324; --p-inv-accent-ink: #ffffff; --p-inv-action: #d23324; --p-inv-action-ink: #ffffff;
  --font-display: "Fraunces", Georgia, serif;
  --font-text: "Figtree", system-ui, sans-serif;
  --display-weight: 400;
  --display-tracking: -0.02em;
  --display-tracking-xl: -0.028em;
  --display-axes: 'SOFT' 30, 'WONK' 0;
}"""


# 2026-11-20 (speed): the six kit stylesheets, in their old order, as one file (fewer requests before the first paint).
# The six files stay as they are; this one is written from them on every build.
KIT_CSS = ['system.css', 'ui/cards.css', 'motion/motion.css', 'backgrounds/backgrounds.css', 'layout/layout.css', 'icons/icon.css']
KIT_BUNDLE = 'kit-bundle.css'


def bundle_kit_css():
    parts = [f'/* ---- {name} ---- */\n' + (SITE / 'assets/kit' / name).read_text(encoding='utf-8') for name in KIT_CSS]
    (SITE / 'assets/kit' / KIT_BUNDLE).write_text('/* written by scripts/redesign/build.py from the six kit stylesheets; edit those */\n' + '\n'.join(parts), encoding='utf-8')


# 2026-11-20 (speed): the photos in redesign/photos-20261120(-recast)/ come in 480, 960 and 1440 wide; each <img> lists
# the sizes that exist so the browser fetches the one it needs. Lazy pictures size themselves from their layout
# (sizes="auto"); browsers without that, and the eager pictures, use the fallback.
SIZED = re.compile(r'<img\b[^>]*>')
SIZED_SRC = re.compile(r'\ssrc="(/assets/redesign/(?:photos-20261120(?:-recast)?|home-20261120)/[a-z0-9-]+)-(?:480|960|1440)\.webp"')


def srcsets(page):
    def add(m):
        tag = m[0]
        src = SIZED_SRC.search(tag)
        if 'srcset=' in tag or not src:
            return tag
        have = [w for w in (480, 960, 1440) if (SITE / f'{src[1].lstrip("/")}-{w}.webp').exists()]
        if len(have) < 2:
            return tag
        sizes = 'auto, (min-width: 1024px) 50vw, 100vw' if 'loading="lazy"' in tag else '100vw'
        return tag.replace(' src=', ' srcset="' + ', '.join(f'{src[1]}-{w}.webp {w}w' for w in have) + f'" sizes="{sizes}" src=', 1)
    return SIZED.sub(add, page)


def stamp(path):
    """/keeper.css?v=<hash>: a changed file is never served from a stale cache"""
    return path + '?v=' + hashlib.sha1((SITE / path.lstrip('/')).read_bytes()).hexdigest()[:8]


def a(s):
    """an attribute value"""
    return escape(str(s), quote=True)


class Page:
    def __init__(self, lang, name, copy):
        self.lang, self.name, self.c = lang, name, copy
        self.L = LANGS[lang]
        self.T = LIVE[lang]

    # paths: all root-relative, like the rest of the site
    def kit(self, p=''): return '/assets/kit/' + p
    def site(self, p=''): return '/assets/' + REFRESHED.get(p, p)
    def own(self, p=''): return '/assets/redesign/' + p

    def url(self, page, lang=None):
        """a page of the site in a language, as the site links it: English links carry ?lang=en, so a reader
        who chose English is not sent back to their browser's language (language.js)"""
        lang = lang or self.lang
        path = '/' if page == 'index.html' else '/' + page
        return path + '?lang=en' if lang == 'en' else '/' + lang + path

    def live(self, p): return self.url(p)

    def canonical(self, lang=None, name=None):
        lang, name = lang or self.lang, name or self.name
        return ORIGIN + ('' if lang == 'en' else '/' + lang) + '/' + ('' if name == 'index.html' else name)

    def look_src(self, kind, path):
        return self.site(path) if kind == 'site' else self.own(path)

    @property
    def checkout(self): return CHECKOUT.format(self.L['stripe'])

    def checkout_for(self, lid):
        return self.checkout + ('' if lid == 'classic' else '&client_reference_id=keeper-' + lid)


# ---------------------------------------------------------------- shared parts

def head(p, title, description, og_title, og_description, share, preload, product=None):
    font = 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..700,0..100,0..1&family=Figtree:wght@400..600'
    # 2026-11-20 (speed): Noto Serif SC/JP/KR (about 670 KB on the Chinese page) is no longer fetched; the serif
    # comes from the reader's own system, which keeper.css already names (Songti SC, Hiragino Mincho, AppleMyungjo)
    font += '&display=swap'
    pre = ''.join(f'<link rel="modulepreload" href="{p.kit("moments/" + m)}">' for m in preload)
    canonical = p.canonical()
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{p.canonical(l)}">' for l in LANGS)
    i18n = json.dumps({'locale': p.lang, 'page': p.name, 'messages': {},
                       'languages': {l: LANGS[l]['label'] for l in LANGS}}, ensure_ascii=False)
    ld = json.dumps({
        '@context': 'https://schema.org', '@type': 'Product', 'name': p.T['product'],
        'description': p.T['product_description'],
        'image': [ORIGIN + p.site('designs/st-50.webp'), ORIGIN + p.site('everyday/01-take-the-photo.webp')],
        'brand': {'@type': 'Brand', 'name': 'keeper.day'},
        'offers': {'@type': 'Offer', 'url': canonical, 'priceCurrency': COMMERCE['currency'], 'price': COMMERCE['price'],
                   'availability': 'https://schema.org/' + COMMERCE['availability'],
                   'itemCondition': 'https://schema.org/NewCondition',
                   'seller': {'@type': 'Organization', 'name': 'Meetu Studio'}},
    }, ensure_ascii=False).replace('</', '<\\/')
    return f"""<!doctype html>
<html lang="{p.L['html']}" data-type="product" data-radius="soft" data-buttons="arrow" data-motion data-locale="{p.lang}" data-page="{p.name}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="{a(SCRIPT_POLICY)}">
<title>{a(title)}</title>
<meta name="description" content="{a(description)}">
<!-- The 2026-11-20 design, generated by scripts/redesign/build.py from scripts/redesign/copy/{p.lang}.json.
     The design it replaced is kept beside it as {p.name.replace('.html', '-20261111.html')} (AGENTS.md: add, never overwrite). -->
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{p.canonical('en')}">
<script id="keeper-i18n" type="application/json">{i18n}</script>
<script src="{stamp('/language.js')}"></script>
<meta property="og:type" content="website">
<meta property="og:title" content="{a(og_title)}">
<meta property="og:description" content="{a(og_description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN + stamp(p.own(share))}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#f5f1ea">
<meta name="site-kind" content="other">
<meta name="page-type" content="product">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{font}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{font}"></noscript>
<link rel="stylesheet" href="{stamp(p.kit(KIT_BUNDLE))}">
<style>
{BRAND}
</style>
<link rel="stylesheet" href="{stamp('/keeper.css')}">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>
<link rel="modulepreload" href="{p.kit('moments/moments.js')}"><link rel="modulepreload" href="{p.kit('moments/lib.js')}">
{pre}
<script type="application/ld+json">{ld}</script>
<script src="{stamp('/consent.js')}" defer></script>
</head>
<body data-order-total="{COMMERCE['total']}">
"""


def consent(p):
    """the live site's consent banner, in this design's look (keeper.css); consent.js shows it until the reader
    chooses, and loads the optional services only once the reader allows them"""
    T = p.T
    return (f'<section class="consent-banner" data-consent-banner aria-label="{a(T["privacy_aria"])}" hidden>'
            f'<p>{T["consent"]} <a href="{p.live("privacy.html")}">{T["details"]}</a></p>'
            f'<div class="consent-actions"><button type="button" data-consent-decline class="btn btn--secondary">{T["decline"]}</button>'
            f'<button type="button" data-consent-allow class="btn btn--secondary">{T["allow"]}</button></div></section>\n')


def lang_menu(p):
    items = ''.join(
        f'<li><a href="{a(p.url(p.name, l))}" hreflang="{LANGS[l]["html"]}" lang="{LANGS[l]["html"]}" data-language="{l}"'
        f'{CUR if l == p.lang else ""}>{LANGS[l]["label"]}</a></li>' for l in LANGS)
    return (f'<details class="lang"><summary aria-label="{a(p.c["shared"]["language"] + ": " + p.L["label"])}">'
            f'{p.L["short"]} {CHEV}</summary><ul class="lang__list">{items}</ul></details>')


def nav(p, links):
    s = p.c['shared']
    looks = s['looks']
    by = {l[0]: l for l in LOOKS}
    cards = []
    for lid in NAV_CARDS:
        _, kind, full, thumb, w, h, _ = by[lid]
        src = p.look_src(kind, thumb)
        tw, th = (w, h) if thumb == full else (360, 480)
        cards.append(f"""            <a class="menu-card span-3" href="{links['looks']}" data-look="{lid}">
              <div class="panel"><img class="frame__img" src="{src}" alt="{a(s['in_look'].format(name=looks[lid]['name']))}" width="{tw}" height="{th}" loading="lazy"></div>
              <span class="t-card">{looks[lid]['name']}</span>
              <span class="t-small muted">{looks[lid]['short']}</span>
            </a>""")
    cur = ' aria-current="page"' if p.name == 'camera.html' else ''
    # one email_off region from the header to the action bar, as on the live pages: Cloudflare leaves the
    # support address inside it alone instead of adding its own decoder script (scripts/check_site.py)
    return f"""<!--email_off-->
<header class="nav nav--split">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">{s['skip']}</a>
    <a class="nav__logo wordmark" href="{links['home']}" aria-label="{a(s['home_aria'])}"><span class="wordmark__text">keeper<span class="wordmark__dot">.</span>day</span></a>
    <nav class="nav__links" aria-label="{a(s['main_aria'])}">
      <div class="nav__item"><a class="nav__link" href="{links['camera']}"{cur}>{s['nav']['camera']}</a></div>
      <div class="nav__item">
        <a class="nav__link" href="{links['looks']}">{s['nav']['looks']} {CHEV}</a>
        <div class="nav__menu">
          <div class="wrap grid">
{chr(10).join(cards)}
          </div>
        </div>
      </div>
      <div class="nav__item"><a class="nav__link" href="{links['screen']}">{s['nav']['screen']}</a></div>
      <div class="nav__item"><a class="nav__link" href="{links['gifts']}">{s['nav']['gifts']}</a></div>
    </nav>
    <div class="nav__actions">
      {lang_menu(p)}
      <a class="btn btn--primary" href="{links['buy']}">{s['nav']['buy']}</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="{a(s['menu'])}">
      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
{consent(p)}"""


def swatch_src(p, lid, kind, thumb):
    """2026-11-20 (speed): a 240-wide copy for the 78 px swatch when it exists (scripts/redesign/make_sizes.py)"""
    small = f'redesign/swatches-20261120/{lid}-240.webp'
    return '/assets/' + small if (SITE / 'assets' / small).exists() else p.look_src(kind, thumb)


def swatches(p):
    s = p.c['shared']
    out = []
    lazy = ' loading="lazy"' if p.name == 'index.html' else ''  # on the product page they sit on the first screen
    for lid, kind, full, thumb, w, h, bg in LOOKS:
        on = lid == INITIAL
        tw, th = (w, h) if thumb == full else (360, 480)
        out.append(f'<button class="swatch" type="button" role="radio" aria-checked="{"true" if on else "false"}" '
                   f'tabindex="{0 if on else -1}" data-look="{lid}" aria-label="{a(s["looks"][lid]["name"])}">'
                   f'<img src="{swatch_src(p, lid, kind, thumb)}" alt="" width="{tw}" height="{th}"{lazy}></button>')
    return (f'<div class="swatches" role="radiogroup" aria-label="{a(s["swatch_group"])}">\n            '
            + '\n            '.join(out) + '\n          </div>')


def looks_json(p):
    s = p.c['shared']['looks']
    data = {
        'checkout': p.checkout,
        'initial': INITIAL,
        'looks': {lid: {'name': s[lid]['name'], 'note': s[lid]['note'], 'src': p.look_src(kind, full), 'w': w, 'h': h,
                        'alt': s[lid]['alt'], 'bg': bg}
                  for lid, kind, full, thumb, w, h, bg in LOOKS},
    }
    return json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')


def initial_look(p):
    by = {l[0]: l for l in LOOKS}
    lid, kind, full, thumb, w, h, bg = by[INITIAL]
    return p.c['shared']['looks'][lid], p.look_src(kind, full), w, h, bg


def hm(c, sid):
    """a section a language's longer copy makes taller than one phone screen: two whole screens there
    (copy file: "phone_screens": {"<section id>": 2})"""
    n = c.get('phone_screens', {}).get(sid)
    return f' style="--hm: {n}"' if n else ''


def rows(items):
    return '\n'.join(f'          <li><span class="rows__name">{n}</span><span class="rows__value">{v}</span></li>' for n, v in items)


def faq(items):
    return '\n'.join(f'        <div class="faq__item"><h3>{q}</h3><p>{ans}</p></div>' for q, ans in items)


def footer(p, close, links, buy_href):
    s = p.c['shared']
    f = s['footer']
    langs = ' '.join(
        f'<a href="{a(p.url(p.name, l))}" hreflang="{LANGS[l]["html"]}" lang="{LANGS[l]["html"]}" data-language="{l}"'
        f'{CUR if l == p.lang else ""}>{LANGS[l]["label"]}</a>' for l in LANGS)
    return f"""
<footer class="footer closing footer--dark ground-inverse" id="contact" aria-labelledby="close-h">
  <div class="wrap">
    <div class="closing__cta close--photo">
      <div class="section-head--split">
        <div><h2 id="close-h">{close['h2']}</h2><p class="t-lead">{close['line']}</p></div>
        <a class="btn btn--primary" href="{buy_href}">{s['nav']['buy']}{ARROW}</a>
      </div>
      <div class="close__media" style="--pos: {close['pos']}{'; --pos-phone: ' + close['pos_phone'] if close.get('pos_phone') else ''}"><img src="{close['src']}" alt="{a(close['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="{a(close['subject'])}"></div>
    </div>
    <div class="closing__links">
      <div class="grid">
        <div class="span-4 stack-4">
          <a class="nav__logo wordmark" href="#top" aria-label="{a(s['top_aria'])}"><span class="wordmark__text">keeper<span class="wordmark__dot">.</span>day</span></a>
          <p class="footer__lede">{f['lede']}</p>
        </div>
        <div class="span-2 footer__col"><h3>{f['keeper']}</h3><ul><li><a href="{links['how']}">{f['how']}</a></li><li><a href="{links['looks']}">{f['looks']}</a></li><li><a href="{links['specs']}">{f['specs']}</a></li><li><a href="{links['shipping']}">{f['shipping']}</a></li></ul></div>
        <div class="span-2 footer__col"><h3>{f['guides']}</h3><ul><li><a href="{p.live('guide-first-photo.html')}">{f['guide_first']}</a></li><li><a href="{p.live('guide-photo-walk.html')}">{f['guide_walk']}</a></li><li><a href="{p.live('gifting.html')}">{f['gifting']}</a></li></ul></div>
        <div class="span-2 footer__col"><h3>{f['help']}</h3><ul><li><a href="{p.live('support.html')}">{f['support']}</a></li><li><a href="{p.live('terms.html')}">{f['terms']}</a></li><li><a href="mailto:support@keeper.day">{f['email']}</a></li><li><button class="footer__button" type="button" data-open-chat hidden>{p.T['chat']}</button></li></ul></div>
        <div class="span-2 footer__col"><h3>{f['company']}</h3><ul><li><a href="{p.live('about.html')}">{f['about']}</a></li><li><a href="{p.live('privacy.html')}">{f['privacy']}</a></li><li><button class="footer__button" type="button" data-open-consent>{p.T['cookies']}</button></li></ul></div>
      </div>
      <div class="footer__legal">
        <span>{f['copyright']} &nbsp; <a href="{p.live('privacy.html')}">{f['privacy']}</a> &nbsp; <a href="{p.live('terms.html')}">{f['legal_terms']}</a></span>
        <span class="footer__langs" aria-label="{a(f['languages'])}">{langs}</span>
        <span>{f['ai']}</span>
      </div>
    </div>
  </div>
</footer>

<nav class="actionbar" aria-label="{a(s['quick_aria'])}">
  <a class="btn btn--primary" href="{buy_href}">{s['nav']['buy']}</a>
</nav>
<!--/email_off-->

<script type="application/json" id="kd-looks">
{looks_json(p)}
</script>
<script type="module" src="{stamp('/keeper.js')}"></script>
<script type="module" src="{stamp(p.kit('system.js'))}"></script>
<script type="module" src="{stamp(p.kit('motion/motion.js'))}"></script>
<script type="module" src="{stamp(p.kit('layout/layout.js'))}"></script>
<template id="optional-services">{TRACKING}</template>
</body>
</html>
"""


# ---------------------------------------------------------------- the home page

def home(p):
    c, s = p.c['home'], p.c['shared']
    S = p.site
    look, look_src, lw, lh, lbg = initial_look(p)
    h = head(p, c['title'], c['description'], c['og_title'], c['og_description'], HOME_SHARE,
             ['pinned-chapters/moment.js', 'picture-develops/moment.js'])
    comment = """<!-- type: product (site-kind other: a consumer camera sold as an everyday and gift object; photographs lead)
     deal: hero product (photograph on the stage), nav nav-split, close close-photo, footer footer-dark,
     rhythm brand-band (#gift), buttons arrow, mark: the client's own wordmark (keeper.day, red dot)
     palette: the client's own colours through start.mjs brand: paper ground #f5f1ea, ink #1d1b17,
     shutter red #d23324 (the red of Keeper's shutter button and of the dot in the wordmark)
     type: Fraunces / Figtree (start.mjs deal, first pairing); Chinese, Japanese and Korean add a serif and a
     sans of their own (keeper.css)
     moments: pinned-chapters in #how (frame, press, keep: the three steps of taking a photo held on one screen),
     picture-develops in #paper (the e-paper photograph comes up like a print)
     Every photograph is the client's own (AI-generated scenes composited with locked product layers, see the
     vault's website-refresh notes); the FAQ and the legal row say so. -->
"""
    links = {'home': '#top', 'camera': p.url('camera.html'), 'looks': '#looks', 'screen': '#paper', 'gifts': '#gift', 'buy': '#order'}
    steps_src = [S('inspiration/20261110/04-color-walk-1440.webp'), S('everyday/02-photograph-your-people.webp'),
                 S('editorial/20261109-shooting/epaper-triptych-1440.webp')]
    steps_alt = [st['alt'] for st in c['how']['steps']]
    if HOME_SHUTTER:
        steps_src[1] = '/assets/redesign/home-20261120/shutter-1440.webp'
        steps_alt[1] = c['how']['steps'][1].get('alt_20261120', steps_alt[1])
    if HOME_HERO:
        hero_img = ('/assets/redesign/home-20261120/hero-classic-1440.webp', c.get('hero_alt_20261120', c['hero_alt']), '34% 50%')
    else:
        hero_img = (S('inspiration/20261110/03-favorite-people-1440.webp'), c['hero_alt'], '32% 30%')
    if HOME_ALL_LOOKS:
        order_img = ('/assets/redesign/home-20261120/looks-all-1080.webp', c['order'].get('all_alt_20261120', look['alt']), 1080, 1440, '#f8f4ee')
    else:
        order_img = (look_src, look['alt'], lw, lh, lbg)
    steps_subj = ['Framing a shot with Keeper', 'Taking a photo with the red shutter', 'The photo staying on the e-paper screen']
    steps = '\n'.join(f"""          <li class="mo-pc__step">
            <h3>{st['h3']}</h3>
            <p>{st['p']}</p>
            <figure class="mo-pc__visual"><img src="{src}" alt="{a(alt)}" width="1440" height="960" loading="lazy" data-source="client" data-subject="{subj}"></figure>
          </li>""" for st, src, alt, subj in zip(c['how']['steps'], steps_src, steps_alt, steps_subj))
    wall_items = [('st-27', '09-graduation-news', 'Keeper at a graduation'), ('p-01-a', '05-two-perspectives', 'Keeper with a dog in the park'),
                  ('st-12', '06-your-city', 'Keeper on a city street'), ('st-50', '10-thank-you', 'Keeper at a kitchen table'),
                  ('st-31', '08-new-beginnings', 'Keeper in a new apartment'), ('st-42', '01-self-portrait', 'Keeper in a garden')]
    wall = '\n'.join(
        f'        <a class="m-zoom" href="#looks" data-look="{lid}" aria-label="{a(c["everyday"]["aria"].format(look=s["looks"][lid]["name"], where=w["where"]))}">'
        f'<img src="{S("inspiration/20261110/" + f + "-960.webp")}" alt="{a(w["alt"])}" width="960" height="640" loading="lazy" data-source="client" data-subject="{subj}"></a>'
        for (lid, f, subj), w in zip(wall_items, c['everyday']['wall']))
    o = c['order']
    body = f"""{comment}{nav(p, links)}
<main id="top">
  <section class="hero hero--product" data-enter aria-labelledby="hero-h">
    <div class="wrap"><div class="hero-text hero__in">
      <div class="hero__head">
        <div>
          <h1 id="hero-h">{c['h1']}</h1>
          <p class="hero__lead">{c['lead']}</p>
        </div>
        <div class="btn-row"><a class="btn btn--primary" href="#order">{s['nav']['buy']}{ARROW}</a><a class="btn btn--secondary" href="#how">{c['see_how']}</a></div>
      </div>
      <div class="hero__stage">
        <img src="{hero_img[0]}" alt="{a(hero_img[1])}" width="1440" height="960" style="--ly-pos: {hero_img[2]}" fetchpriority="high" data-source="client" data-subject="Keeper in use, photographing two friends">
      </div>
    </div></div>
  </section>

  <!-- pinned-chapters: the section holds while the three steps open one at a time -->
  <section class="section" id="how" style="--h: 2" data-moment="pinned-chapters" aria-labelledby="how-h">
    <div class="wrap mo-pc__grid">
      <div class="mo-pc__text">
        <h2 id="how-h">{c['how']['h2']}</h2>
        <ol class="mo-pc__steps">
{steps}
        </ol>
      </div>
      <div class="mo-pc__visuals frame"></div>
    </div>
  </section>

  <section class="section" id="order" style="--hm: 2" aria-labelledby="order-h">
    <div class="wrap grid grid--top">
      <div class="span-6 order">
        <div class="section-head">
          <h2 id="order-h">{o['h2']}</h2>
          <p>{o['p']}</p>
        </div>
        <div id="looks">
          <div class="order__look" aria-live="polite">
            <p class="order__name" data-look-name>{look['name']}</p>
            <p class="order__note" data-look-note>{look['note']}</p>
          </div>
          {swatches(p)}
        </div>
        <ul class="rows rows--spec">
{rows(o['rows'])}
        </ul>
        <div class="btn-row">
          <a class="btn btn--primary" data-buy data-purchase="home-order" data-variant="{INITIAL}" href="{a(p.checkout_for(INITIAL))}">{s['nav']['buy']}{ARROW}</a>
          <a class="link" href="{p.url('camera.html')}#shipping">{o['shipping_link']}</a>
        </div>
      </div>
      <figure class="order__frame span-5 start-8" style="--look-bg: {order_img[4]}">
        <img data-look-img src="{order_img[0]}" alt="{a(order_img[1])}" width="{order_img[2]}" height="{order_img[3]}" loading="lazy" data-source="client" data-subject="Keeper, the selected look">
      </figure>
    </div>
  </section>

  <section class="section" id="everyday" aria-labelledby="everyday-h">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div>
          <h2 id="everyday-h">{c['everyday']['h2']}</h2>
          <p>{c['everyday']['p']}</p>
        </div>
        <a class="link" href="{p.live('guide-photo-walk.html')}">{c['everyday']['link']}</a>
      </div>
      <div class="wall">
{wall}
      </div>
    </div>
  </section>

  <section class="section" id="paper"{hm(c, 'paper')} aria-labelledby="paper-h">
    <div class="wrap grid grid--top">
      <div class="span-6">
        <div class="section-head">
          <h2 id="paper-h">{c['paper']['h2']}</h2>
          <p>{c['paper']['p']}</p>
        </div>
        <ul class="rows rows--spec">
{rows(c['paper']['rows'])}
        </ul>
        <p class="t-small muted">{c['paper']['note']}</p>
      </div>
      <figure class="develop span-5 start-8" data-moment="picture-develops"><img src="{S('storefront/at-home.webp')}" alt="{a(c['paper']['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Keeper's e-paper screen at home"></figure>
    </div>
  </section>

  <section class="section" id="carry" aria-labelledby="carry-h">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div>
          <h2 id="carry-h">{c['carry']['h2']}</h2>
          <p>{c['carry']['p']}</p>
        </div>
        <a class="link" href="{p.live('guide-first-photo.html')}">{c['carry']['link']}</a>
      </div>
      <div class="bleed"><img src="{S('editorial/20261109-shooting/carry-1440.webp')}" alt="{a(c['carry']['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Keeper carried with a jacket and tote"></div>
    </div>
  </section>

  <section class="section ground-brand" id="gift" aria-labelledby="gift-h">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div>
          <h2 id="gift-h">{c['gift']['h2']}</h2>
          <p>{c['gift']['p']}</p>
        </div>
        <a class="link" href="{p.live('gifting.html')}">{c['gift']['link']}</a>
      </div>
      <div class="grid">
        <figure class="pair__photo span-6"><img src="{S('inspiration/20261110/20-gift-a-memory-1440.webp')}" alt="{a(c['gift']['alt1'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Keeper wrapped as a gift"></figure>
        <figure class="pair__photo span-6"><img src="{S('storefront/gift-opening.webp')}" alt="{a(c['gift']['alt2'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Opening the Keeper gift box"></figure>
      </div>
    </div>
  </section>

  <section class="section" id="questions" aria-labelledby="questions-h">
    <div class="wrap grid grid--top">
      <div class="span-6">
        <div class="section-head">
          <h2 id="questions-h">{c['questions']['h2']}</h2>
          <p>{c['questions']['p']}</p>
        </div>
        <a class="link" href="mailto:support@keeper.day">{c['questions']['link']}</a>
      </div>
      <div class="faq span-5 start-8">
{faq(c['questions']['faq'])}
      </div>
    </div>
  </section>
</main>
"""
    close = dict(c['close'], src=S('inspiration/20261110/26-holiday-memory-1440.webp'), pos='50% 56%', pos_phone='20% 56%', subject='Keeper at a holiday at home')
    flinks = {'how': '#how', 'looks': '#looks', 'paper': '#paper', 'specs': p.url('camera.html') + '#specs', 'shipping': p.url('camera.html') + '#shipping'}
    return h + body + footer(p, close, flinks, '#order')


# ---------------------------------------------------------------- the product page

def camera(p):
    c, s = p.c['camera'], p.c['shared']
    S = p.site
    look, look_src, lw, lh, lbg = initial_look(p)
    h = head(p, c['title'], c['description'], c['og_title'], c['og_description'], 'share-camera.jpg',
             ['photo-chapters/moment.js'])
    comment = """<!-- type: product (site-kind other), the product page: choose a look and buy
     hero split (the order beside the chosen look; the home page's product hero is not dealt twice),
     nav nav-split, close close-photo, footer footer-dark, rhythm brand-band (#box), buttons arrow, mark: wordmark;
     palette and type as the home page (index.html)
     moment: photo-chapters in #day (four photographs of one day with Keeper, one large frame at a time)
     Every photograph is the client's own (AI-generated scenes composited with locked product layers); the FAQ and
     the legal row say so. Only looks on sale are shown. -->
"""
    links = {'home': p.url('index.html'), 'camera': '#top', 'looks': '#looks', 'screen': p.url('index.html') + '#paper', 'gifts': p.url('index.html') + '#gift', 'buy': '#choose-style'}
    ch_src = [S('storefront/in-the-hand.webp'), S('inspiration/20261110/07-love-story-1440.webp'),
              S('editorial/20261109-shooting/family-1440.webp'), S('inspiration/20261110/25-frame-the-day-1440.webp')]
    ch_subj = ['Keeper in hand on the way out', 'Keeper at coffee with a friend', 'Keeper at a birthday party', 'Keeper at home in the evening']
    # the chapter's panel sits on the lower left of the frame: each photograph keeps Keeper clear of it
    ch_pos = ['', '', ' style="object-position: 50% 72%"', '']
    chapters = '\n'.join(f"""        <li class="mo-ph__ch">
          <figure class="mo-ph__pic"><img src="{src}" alt="{a(ch['alt'])}" width="1440" height="960"{pos} loading="lazy" data-source="client" data-subject="{subj}"></figure>
          <h3>{ch['h3']}</h3>
          <p>{ch['p']}</p>
        </li>""" for ch, src, subj, pos in zip(c['day']['chapters'], ch_src, ch_subj, ch_pos))
    box_items = '\n'.join(f'          <li>{i}</li>' for i in c['box']['items'])
    sh = c['shipping']
    body = f"""{comment}{nav(p, links)}
<main id="top">
  <section class="hero hero--split buy" id="choose-style" data-enter aria-labelledby="hero-h">
    <div class="wrap"><div class="hero-text grid hero__grid">
      <div class="hero__text span-5">
        <h1 id="hero-h">{c['h1']}</h1>
        <p class="hero__lead">{c['lead']}</p>
        <p class="buy__price"><span class="buy__amount">{c['price']}</span><span class="buy__ship">{c['ship']}</span></p>
        <div id="looks">
          <p class="buy__look" aria-live="polite"><span class="buy__name" data-look-name>{look['name']}</span><span class="buy__note" data-look-note>{look['note']}</span></p>
          {swatches(p)}
        </div>
        <div class="btn-row"><a class="btn btn--primary" data-buy data-purchase="camera-hero" data-variant="{INITIAL}" href="{a(p.checkout_for(INITIAL))}">{s['nav']['buy']}{ARROW}</a><a class="link" href="#shipping">{c['shipping_link']}</a></div>
        <p class="buy__reassure t-small muted">{c['reassure']}</p>
      </div>
      <div class="hero__media span-6 start-7" style="--look-bg: {lbg}">
        <img data-look-img src="{look_src}" alt="{a(look['alt'])}" width="{lw}" height="{lh}" fetchpriority="high" data-source="client" data-subject="Keeper, the selected look">
      </div>
    </div></div>
  </section>

  <!-- photo-chapters: the section holds while each photograph of the day uncovers the one before -->
  <section class="section" id="day" data-moment="photo-chapters" aria-labelledby="day-h">
    <div class="wrap mo-ph">
      <div class="mo-ph__head"><h2 id="day-h">{c['day']['h2']}</h2><p>{c['day']['p']}</p></div>
      <ol class="mo-ph__list">
{chapters}
      </ol>
    </div>
  </section>

  <section class="section" id="specs" style="--hm: 2" aria-labelledby="specs-h">
    <div class="wrap grid grid--top">
      <div class="span-6">
        <div class="section-head">
          <h2 id="specs-h">{c['specs']['h2']}</h2>
          <p>{c['specs']['p']}</p>
        </div>
        <ul class="rows rows--spec">
{rows(c['specs']['rows'])}
        </ul>
        <p class="t-small muted">{c['specs']['note']}</p>
      </div>
      <figure class="side-photo span-5 start-8" style="--pos: 70% 50%"><img src="{S('everyday/05-workdesk.webp')}" alt="{a(c['specs']['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Keeper on a desk"></figure>
    </div>
  </section>

  <section class="section ground-brand" id="box" aria-labelledby="box-h">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div>
          <h2 id="box-h">{c['box']['h2']}</h2>
          <p>{c['box']['p']}</p>
        </div>
      </div>
      <figure class="box__photo"><img src="{S('storefront/full-kit.webp')}" alt="{a(c['box']['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Everything in the Keeper gift box"></figure>
      <ul class="box__items">
{box_items}
      </ul>
      <p class="box__note t-small">{c['box']['note']}</p>
    </div>
  </section>

  <section class="section ship" id="shipping" style="--hm: 2" aria-labelledby="shipping-h">
    <div class="wrap grid grid--top">
      <div class="span-6">
        <div class="section-head">
          <h2 id="shipping-h">{sh['h2']}</h2>
        </div>
        <h3 class="rows__head">{sh['head1']}</h3>
        <ul class="rows rows--spec">
{rows(sh['rows1'])}
        </ul>
        <h3 class="rows__head">{sh['head2']}</h3>
        <ul class="rows rows--spec">
{rows(sh['rows2'])}
        </ul>
        <a class="link" href="{p.live('terms.html')}">{sh['terms_link']}</a>
      </div>
      <figure class="side-photo span-5 start-8" style="--pos: 50% 55%"><img src="{S('storefront/gift-box.webp')}" alt="{a(sh['alt'])}" width="1440" height="960" loading="lazy" data-source="client" data-subject="Keeper in its gift box"></figure>
    </div>
  </section>

  <section class="section" id="questions" aria-labelledby="questions-h">
    <div class="wrap grid grid--top">
      <div class="span-6">
        <div class="section-head">
          <h2 id="questions-h">{c['questions']['h2']}</h2>
          <p>{c['questions']['p']}</p>
        </div>
        <a class="link" href="mailto:support@keeper.day">{c['questions']['link']}</a>
      </div>
      <div class="faq span-5 start-8">
{faq(c['questions']['faq'])}
      </div>
    </div>
  </section>
</main>
"""
    close = dict(c['close'], src=S('editorial/20261109-shooting/cafe-1440.webp'), pos='50% 70%', subject='Keeper at a café')
    flinks = {'how': p.url('index.html') + '#how', 'looks': '#looks', 'paper': p.url('index.html') + '#paper', 'specs': '#specs', 'shipping': '#shipping'}
    return h + body + footer(p, close, flinks, '#choose-style')


def main():
    bundle_kit_css()
    for lang in LANGS:
        f = COPY / f'{lang}.json'
        if not f.exists():
            print('skip', lang, '(no copy yet)')
            continue
        copy = json.loads(f.read_text(encoding='utf-8'))
        out = SITE / LANGS[lang]['dir']
        out.mkdir(exist_ok=True)
        for name, fn in (('index.html', home), ('camera.html', camera)):
            (out / name).write_text(srcsets(fn(Page(lang, name, copy))), encoding='utf-8')
            print('wrote', (out / name).relative_to(SITE))


if __name__ == '__main__':
    main()
