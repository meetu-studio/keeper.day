"""Build complete static language pages from the existing storefront templates."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from string import Formatter
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {'en': 'English', 'zh': '中文', 'ja': '日本語', 'ko': '한국어'}
HTML_LANG = {'en': 'en', 'zh': 'zh-Hans', 'ja': 'ja', 'ko': 'ko'}
DATA = json.loads((ROOT/'scripts/content.json').read_text())
INVARIANT = {'keeper', 'day', 'keeper.day', 'Keeper', 'Meetu Studio', 'Stripe', 'HubSpot',
             'Google Analytics', 'Meta Pixel', 'Microsoft Clarity', 'GitHub Pages', 'A', 'B', 'USD', 'microSD', 'IPS LCD'}


def invariant(text):
    return (not re.search(r'[A-Za-z]', text) or text in INVARIANT or
            re.fullmatch(r'(?:ST|P)-\d{2}(?:-[AB])?', text) or
            re.fullmatch(r'support@keeper\.day(?: ↗)?', text) or
            re.fullmatch(r'(?:US)?\$[\d,.]+', text) or text.startswith('© '))


def money_text(text):
    return re.sub(r'(?<!US)\$(?=\d)', 'US$', text)


def localized_url(url, locale, explicit_en=True):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path.startswith('/') or parts.path.startswith('/assets/'):
        return url
    path = re.sub(r'^/(?:zh|ja|ko)(?=/|$)', '', parts.path) or '/'
    if path not in ['/'] and not path.endswith('.html'):
        return url
    if locale != 'en':
        path = '/'+locale+path
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.pop('lang', None)
    if locale == 'en' and explicit_en:
        query['lang'] = 'en'
    return urlunsplit(('', '', path, urlencode(query), parts.fragment))


def canonical(filename, locale):
    return 'https://keeper.day'+localized_url('/'+('' if filename == 'index.html' else filename), locale, False)


def checkout_url(url, locale):
    p = urlsplit(url)
    q = dict(parse_qsl(p.query))
    q['locale'] = locale
    return urlunsplit((p.scheme,p.netloc,p.path,urlencode(q),p.fragment))


def read_catalogs():
    catalogs = {lang: json.loads((ROOT/f'scripts/locales/{lang}.json').read_text()) for lang in LANGUAGES}
    for lang, catalog in catalogs.items():
        for section in ['text', 'ui', 'designs']:
            if set(catalog[section]) != set(catalogs['en'][section]):
                raise ValueError(f'{lang}: translation keys disagree in {section}')
            for key, value in catalog[section].items():
                if not isinstance(value,str) or not value.strip():
                    raise ValueError(f'{lang}: empty translation {section}/{key}')
                placeholders = lambda s: sorted(name for _,name,_,_ in Formatter().parse(s) if name is not None)
                if placeholders(value) != placeholders(catalogs['en'][section][key]):
                    raise ValueError(f'{lang}: placeholder mismatch {section}/{key}')
        if set(catalog['designs']) != {d['id'] for d in DATA['designs']}:
            raise ValueError(f'{lang}: exterior names do not cover all 98 designs')
    return catalogs


def dynamic_entries(catalog):
    ui, names, texts = (catalog[k] for k in ['ui','designs','text'])
    t = lambda key, **values: ui[key].format(**values)
    entries = {}
    for design in DATA['designs']:
        key, paired = design['id'], design['kind'] == 'paired'
        name, local = design['name'], names[key]
        entries[name] = local
        suffix = ' A and B exterior designs' if paired else ' exterior design'
        entries[name+' — '+key.upper()+suffix] = t('paired_image' if paired else 'design_image',name=local,id=key.upper())
        for side in (['a','b'] if paired else ['']):
            entries[f'Buy one {name} {side.upper()} Keeper, $229 USD including shipping'] = t('buy_design_aria',name=local,side=side.upper())
    for variant in DATA['variants']:
        group, side = variant['group'], variant['side']
        label = names[group]+(t('side_suffix',side=side.upper()) if side else '')
        original = f'{group.upper()}{" "+side.upper() if side else ""} — {variant["name"]}'
        entries[original] = f'{group.upper()}{" "+side.upper() if side else ""} — {label}'
    for scene in DATA['lifestyle']+DATA['camera_story']:
        if not scene.get('alt'):
            original = scene['title']+' — Keeper '+scene['style'].upper()+' in an American everyday setting'
            entries[original] = t('scene_alt',title=texts.get(scene['title'],scene['title']),id=scene['style'].upper())
    for asset in DATA['assets'].values():
        title = asset['title']
        entries['View full image: '+title+' (opens new tab)'] = t('view_full_image',title=texts.get(title,title))
    labels = ['The camera','Out taking photographs','Photograph your people','What’s included','At your desk']
    for i, label in enumerate(labels):
        entries[f'Show image {i+1}: {label}'] = t('image_button',index=i+1,label=texts.get(label,label))
    return entries


class Localizer(HTMLParser):
    def __init__(self, locale, filename, catalogs):
        super().__init__(convert_charrefs=True)
        self.locale, self.filename, self.catalogs = locale, filename, catalogs
        self.catalog = catalogs[locale]
        self.entries = {**self.catalog['text'], **dynamic_entries(self.catalog)}
        self.output = []
        self.script = None
        self.in_template = False

    def text(self, value):
        key = value.strip()
        if not key:
            return value
        if key in self.entries:
            result = self.entries[key]
        elif invariant(key):
            result = key
        else:
            raise ValueError(f'{self.locale}/{self.filename}: missing translation {key!r}')
        return value[:len(value)-len(value.lstrip())]+money_text(result)+value[len(value.rstrip()):]

    def handle_decl(self, decl):
        self.output.append('<!'+decl+'>')

    def handle_comment(self, data):
        self.output.append('<!--'+data+'-->')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'template':
            self.in_template = True
        if tag == 'script':
            self.script = a.get('id') or a.get('type') or 'script'
        if tag == 'html':
            a.update({'lang':HTML_LANG[self.locale], 'data-locale':self.locale,'data-page':self.filename})
        classes = a.get('class','').split()
        if tag == 'button' or 'sf-buy' in classes or 'nav-contact' in classes:
            a['class'] = ' '.join(classes+['btn'])
        elif 'kr-design-image' in classes or 'kr-life-image' in classes:
            a['class'] = ' '.join(classes+['m-zoom'])
        if not self.in_template:
            for key in ['alt','aria-label','placeholder','label']:
                if a.get(key):
                    a[key] = self.text(a[key])
            if tag == 'meta' and (a.get('name') == 'description' or a.get('property') in ['og:title','og:description']):
                a['content'] = self.text(a['content'])
            if tag == 'meta' and a.get('property') == 'og:url':
                a['content'] = canonical(self.filename,self.locale)
            if tag == 'link' and a.get('rel') == 'canonical':
                a['href'] = canonical(self.filename,self.locale)
            elif 'href' in a:
                if urlsplit(a['href']).netloc == 'buy.stripe.com':
                    a['href'] = checkout_url(a['href'],self.locale)
                else:
                    a['href'] = localized_url(a['href'],self.locale)
            if 'data-search' in a:
                key = a['data-search'].split()[0]
                variants = ' '.join(v['id'] for v in DATA['variants'] if v['group'] == key)
                a['data-search'] = key+' '+variants+' '+' '.join(c['designs'][key] for c in self.catalogs.values())
            for key in ['data-share-url','data-copy-url']:
                if key in a:
                    p = urlsplit(a[key])
                    a[key] = 'https://keeper.day'+localized_url(p.path+('?' + p.query if p.query else ''),self.locale)
        self.output.append('<'+tag+''.join(' '+key if value is None else ' '+key+'="'+escape(value,quote=True)+'"' for key,value in a.items())+'>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)

    def handle_endtag(self, tag):
        self.output.append('</'+tag+'>')
        if tag == 'script':
            self.script = None
        if tag == 'template':
            self.in_template = False

    def handle_data(self, data):
        if self.script == 'keeper-design-data':
            payload = json.loads(data)
            for variant in payload['variants']:
                variant['name'] = self.catalog['designs'][variant['group']]+(self.catalog['ui']['side_suffix'].format(side=variant['side'].upper()) if variant['side'] else '')
            payload['checkout'] = checkout_url(payload['checkout'],self.locale)
            self.output.append(safe_json(payload))
        elif self.script == 'application/ld+json':
            payload = json.loads(data)
            for key in ['name','description']:
                payload[key] = self.text(payload[key])
            payload['offers']['url'] = canonical(self.filename,self.locale)
            self.output.append(safe_json(payload))
        elif self.script or self.in_template:
            self.output.append(data)
        else:
            self.output.append(escape(self.text(data),quote=False))


def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')


def localize(source, locale, filename, catalogs, version):
    parser = Localizer(locale,filename,catalogs)
    parser.feed(source)
    result = ''.join(parser.output)
    if locale != 'en':
        word = escape(catalogs[locale]['text']['Everyday'])
        result = result.replace(word+' <em>',word+'<em>')
    alternate = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[lang]}" href="{canonical(filename,lang)}">' for lang in LANGUAGES)
    alternate += f'<link rel="alternate" hreflang="x-default" href="{canonical(filename,"en")}">'
    context = {'locale':locale,'page':filename,'messages':catalogs[locale]['ui'],'languages':LANGUAGES}
    boot = f'<script id="keeper-i18n" type="application/json">{safe_json(context)}</script><script src="/language.js?v={version}"></script>'
    result = result.replace('<title>',alternate+boot+'<title>',1)
    links = ''.join(f'<a href="{localized_url("/"+("" if filename=="index.html" else filename),lang)}" data-language="{lang}" lang="{HTML_LANG[lang]}"'+(' aria-current="true"' if lang==locale else '')+f'>{label}</a>' for lang,label in LANGUAGES.items())
    label = escape(catalogs[locale]['ui']['language_label'])
    switch = f'<details class="language-switch"><summary aria-label="{label}: {LANGUAGES[locale]}" lang="{HTML_LANG[locale]}">{LANGUAGES[locale]}<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><path d="m3 4.5 3 3 3-3"></path></svg></summary><div class="language-options" role="group" aria-label="{label}">{links}</div></details>'
    result = result.replace('<nav aria-label=', '<div class="header-language">'+switch+'</div><nav aria-label=',1)
    if filename == '404.html':
        result = result.replace('<title>','<meta name="robots" content="noindex"><title>',1)
    return result


def attach_not_found(pages):
    """Translate the shared Pages 404 without redirecting an unknown URL."""
    fragments = {}
    for locale, source in pages.items():
        fragments[locale] = {'body':re.search(r'<body[^>]*>(.*)</body>',source,re.S).group(1),
                             'title':re.search(r'<title>(.*?)</title>',source,re.S).group(1),
                             'messages':json.loads(re.search(r'<script id="keeper-i18n" type="application/json">(.*?)</script>',source,re.S).group(1))['messages']}
    source = pages['en']
    packet = '<script id="keeper-not-found" type="application/json">'+safe_json(fragments)+'</script><script>KeeperI18n.localizeNotFound()</script>'
    return source.replace('</body>',packet+'</body>')
