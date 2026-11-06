#!/usr/bin/env python3
"""Optimize explicitly curated project assets without cropping or redrawing hardware.
Only run in the source vault. Published pages use the committed WebP files.
"""
from pathlib import Path
from PIL import Image, ImageOps
import json
ROOT=Path(__file__).resolve().parents[1]
VAULT=ROOT.parents[2]
SOURCE=VAULT/'attachments/keeper-day'
OUT=ROOT/'assets/collections'
OUT.mkdir(parents=True,exist_ok=True)
assets={}; groups={'pairs':[],'styles':[],'apps':[],'moments':[],'app_featured':['app-calendar','app-water','app-travel','app-anniversary']}
def add(key,source,title,copy,group,alt=None,label='DESIGN EXPLORATION',**extras):
    path=ROOT/'assets'/source.removeprefix('deployed:') if source.startswith('deployed:') else SOURCE/source
    assert path.is_file(),path
    with Image.open(path) as raw:
        im=ImageOps.exif_transpose(raw).convert('RGB')
        im.thumbnail((1440,1200) if group in ('pairs','apps','moments') else (720,960),Image.Resampling.LANCZOS)
        im.save(OUT/f'{key}.webp','WEBP',quality=86,method=6)
        width,height=im.size
    assets[key]={'source':str(path.relative_to(VAULT)),'title':title,'copy':copy,'alt':alt or f'{title} — Keeper {label.lower()}', 'label':label,'width':width,'height':height,**extras}
    groups[group].append(key)
# Paired surface designs: artwork does not imply connectivity or bundle availability.
pairs=[
('photos','p-16-mutual-photos-v2','You, through my eyes.','Your picture on mine. My picture on yours. A little portrait of being someone’s favorite person.'),
('sun-moon','p-01-sun-moon-v2','You’re my sun. I’m your moon.','Warm daylight and a midnight sky. Two different energies, one good pair.'),
('mountain-sea','p-02-mountain-sea-v2','Mountains meet the sea.','For the person who feels like both an adventure and a place to come home to.'),
('dawn-dusk','p-03-dawn-dusk-v2','From first light to last.','A soft beginning and a golden ending. Two halves of a day worth keeping.'),
('rain-rainbow','p-04-rain-rainbow-v2','After the rain, you.','A little weather, a little color. An optimistic pair for your everyday person.'),
('high-five','p-11-high-five-v2','My partner in everything.','For the small wins, the big plans and the friend who’s always on your side.'),
('cats','p-13-facing-cats-v2','A perfect little pair.','Two curious cats, facing each other. Quiet company with a playful side.'),
('pixels','p-21-pixel-partners-v2','Better in two-player mode.','A pixel-inspired pair for your favorite teammate, on screen and off.'),
('cities','p-25-two-cities-v2','Two cities. One story.','Different skylines, something shared. A visual idea for keeping someone close.'),
('lighthouse','p-07-wave-lighthouse-v2','You’re my way home.','A wave and a lighthouse, made to belong in the same little story.'),
('music','p-17-shared-music-v2','Our kind of soundtrack.','For the songs, the walks and the moments that become yours together.'),
('coffee','p-27-coffee-croissant-v2','Our usual, please.','Coffee and a croissant. A small nod to the routines you love sharing.')]
for k,f,t,c in pairs:add('pair-'+k,'product-stickers/'+f+'.png',t,c,'pairs',label='PAIRED ARTWORK CONCEPT')
# Single-device styles selected from the existing studio artwork.
styles=[
('pixels','st-03-pixel-world','Pixel world','A little retro color for the places you love.'),
('botanical','st-11-botanical-specimens','Botanical notes','Leafy details, a softer palette, and a little room to grow.'),
('swiss','st-31-swiss-grid','Quiet geometry','Clean lines and red accents for a more graphic kind of day.'),
('outdoor','st-46-outdoor-contours','Out of office','Contours and mountain colors for your next small adventure.'),
('stars','st-07-star-chart','Under the stars','A little night sky around your favorite view.'),
('scrapbook','st-05-scrapbook','The scrapbook','A warm, collected look for everyday memories.'),
('midcentury','st-33-midcentury','Sunday afternoon','Warm curves and earthy colors, right at home.'),
('terrazzo','st-35-terrazzo','Little pieces of color','A playful pattern with room for a quiet moment.'),
('waves','st-37-woodcut-waves','By the water','Blue waves around a view you wish you could stay in.'),
('ink','st-38-ink-landscape','A slower view','Soft landscape details for the contemplative ones.'),
('gradient','st-42-soft-gradient','Soft daydream','A gentle wash of color around a favorite scene.'),
('pet','st-48-pet-cyanotype','For your favorite face','Blue botanical details for the one who’s always happy to see you.')]
for k,f,t,c in styles:add('style-'+k,'product-stickers/'+f+'.png',t,c,'styles',label='SURFACE-ART CONCEPT')
# Readable, individual display scenes, followed by companion-app explorations.
apps=[
('calendar','screen-scenes-20261106/01-calendar-desk.png','Your day, at a glance.','A calendar and a small plan for the afternoon. An exploration of how a quiet desk display could feel.','Calendar','display'),
('water','screen-scenes-20261106/02-water-reminder.png','A little pause.','A gentle visual idea for a water break. A reminder concept, not an active notification feature.','A little pause','display'),
('travel','screen-scenes-20261106/03-boarding-info.png','A little travel companion.','A sample flight-information layout for a day on the move. Not live travel data or a boarding pass.','On the move','display'),
('anniversary','screen-scenes-20261106/04-anniversary.png','A date worth remembering.','A countdown concept for a day that belongs to the two of you. A little anticipation, kept in sight.','Our anniversary','display'),
('scenes','app/G-saved-scenes.png','01 — Choose your scene.','A saved-scenes concept for collecting favorite display combinations in one place: a photo, a date, a little information for the day.','Saved scenes','companion'),
('layouts','app/H-style-and-layout-editor.png','02 — Make it yours.','Explore Original, Warm Film and Soft Mono photo styles, plus layouts with room for a date or a note. Interface design, not released editing software.','Style & layout','companion'),
('widgets','app/I-widgets-and-schedules.png','03 — Add the little details.','Date, calendar, weather, quote, countdown and checklist previews, plus an exploration of scheduled scene changes.','Widgets','companion'),
('settings','app/J-device-sync-and-settings.png','04 — Review your settings.','A concept flow for checking changes and syncing device configuration. Connectivity and automatic syncing are not confirmed launch features.','Device settings','companion')]
for k,f,t,c,s,cat in apps:add('app-'+k,f,t,c,'apps',label='DISPLAY CONCEPT' if cat=='display' else 'COMPANION APP CONCEPT',short=s,category=cat)
# Lifestyle selections are finalized after visual review; no claims of customer use.
moments=[
('friends','marketing/14-the-good-stuff-stays.png','The people who make the day.','The ones you laugh with. The ones who turn an ordinary afternoon into a favorite memory.'),
('college','marketing/28-student-home.png','A new chapter. A familiar face.','A little reminder of home, wherever your next chapter takes you.'),
('desk','marketing/26-nyc-desk.png','A good place to pause.','A desk, a favorite photo, and a quiet moment in the middle of everything.'),
('pet','website-assets/moment-pet.webp','Yes, another photo of the dog.','Some faces never get old. Make a little room for your everyday favorite.'),
('wedding','marketing/20-take-the-moment-home.png','The day you’ll come back to.','A celebration, a familiar smile, a moment to keep close long after the day.'),
('birthday','marketing/17-gift-she-sees-every-day.png','A gift with someone in mind.','A birthday idea built around a favorite face. Illustrative gift packaging, not final product packaging.'),
('mother','marketing/25-mother-gift.png','For the person who feels like home.','A familiar face. A little thank-you. A gift idea for someone who means a lot.'),
('anniversary','screen-scenes-20261106/04-anniversary.png','Your day, kept close.','An anniversary display concept for the dates that belong to the two of you. Not a released widget.')]
for k,f,t,c in moments:add('moment-'+k,f,t,c,'moments',label='ILLUSTRATIVE LIFESTYLE SCENE')
(ROOT/'scripts/content.json').write_text(json.dumps({'assets':assets,**groups},ensure_ascii=False,indent=2)+'\n')
print(f'Prepared {len(assets)} images; {sum(p.stat().st_size for p in OUT.glob("*.webp"))/1024/1024:.2f} MiB total')
