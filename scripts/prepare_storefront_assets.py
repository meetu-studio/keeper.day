#!/usr/bin/env python3
"""Optimize owner-authorized, reference-conditioned AI photography from the vault."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json
ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT.parents[2]
OUT = ROOT / 'assets/storefront'
OUT.mkdir(exist_ok=True)
SOURCES = {
    'everyday-hero': 'storefront-20261108/01-everyday-hero.png',
    'gift-box': 'storefront-20261108/02-gift-box.png',
    'in-the-hand': 'storefront-20261108/03-in-the-hand.png',
    'at-home': 'storefront-20261108/04-at-home.png',
    'full-kit': 'storefront-kit-20261108/01-full-kit.png',
    'gift-opening': 'storefront-kit-20261108/02-gift-opening.png',
}
manifest = []
for key, relative in SOURCES.items():
    source = VAULT / 'attachments/keeper-day' / relative
    image = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    image.thumbnail((1440, 960), Image.Resampling.LANCZOS)
    dest = OUT / f'{key}.webp'
    image.save(dest, 'WEBP', quality=88, method=6)
    manifest.append({'key': key, 'source': 'attachments/keeper-day/' + relative,
                     'public': f'/assets/storefront/{key}.webp', 'width': image.width,
                     'height': image.height, 'bytes': dest.stat().st_size,
                     'provenance': 'AI-generated whole-scene visualization; not a production-camera sample or customer photo'})
    print(key, image.size, dest.stat().st_size)
(ROOT / 'scripts/storefront-assets.json').write_text(json.dumps(manifest, indent=2) + '\n')
# Branded share card: an intact photographic scene, not a pasted product cutout.
card = Image.new('RGB', (1200, 630), '#f7f3eb')
photo = Image.open(OUT / 'everyday-hero.webp').convert('RGB')
card.paste(ImageOps.fit(photo, (700, 630), centering=(0.55, 0.5)), (500, 0))
draw = ImageDraw.Draw(card)
font_root = Path('/System/Library/Fonts/Supplemental')
def font(size, bold=False):
    path = font_root / ('Arial Bold.ttf' if bold else 'Arial.ttf')
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)
draw.text((44, 42), 'keeper.day', font=font(34, True), fill='#26352e')
draw.multiline_text((44, 176), 'A little camera.\nA day worth\nkeeping.', font=font(49, True), fill='#26352e', spacing=10)
draw.text((44, 425), 'In stock. Gift box included.', font=font(23), fill='#455048')
draw.text((44, 474), '$199 + $30 worldwide shipping', font=font(21), fill='#455048')
card.save(ROOT / 'assets/og-card.webp', 'WEBP', quality=88, method=6)
