from pathlib import Path
import hashlib
import json
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
VAULT = Path('/Users/json/笔记/拍立得')
SOURCE = VAULT / 'attachments/keeper-day/product-stickers'
SCENES = VAULT / 'attachments/keeper-day/website-refresh-20261109'
CWEBP = '/opt/homebrew/bin/cwebp'
single_names = 'Campus doodles|Jelly orbit|Pixel world|Comic strip|The scrapbook|Home team|Under the stars|Film album|Street color|One-line friends|Botanical notes|Indie band|Little clay friends|Memphis shapes|The reading room|Watercolor panda|Dinosaur field notes|Under the sea|Crayon forest|City blocks|Felt clouds|Paper birds|Little universe|Animal stamps|The insect garden|Treasure map|Candy stripes|Puzzle town|Little heroes|Shadow theater|Quiet geometry|Warm minimal|Sunday afternoon|Bauhaus shapes|Terrazzo|Architect’s notebook|By the water|A slower view|Art deco arches|Coffee etching|Office comic|Soft daydream|Daily routes|Woven days|Travel journal|Out of office|Postcards|Favorite face|Paper celebration|Garden stitches|Retro pixels — all over|Retro pixels — border|Retro pixels — emblem|Mechanical print — all over|Mechanical print — border|Mechanical print — emblem|Denim patches — all over|Denim patches — border|Denim patches — emblem|Midnight glass — all over|Midnight glass — border|Midnight glass — emblem|First drawing — all over|First drawing — border|First drawing — emblem|In good company — all over|In good company — border|In good company — emblem'.split('|')
pair_names = 'Sun & moon|Mountains & sea|First light & last|Rain & rainbow|Spring & autumn|Snow & campfire|Wave & lighthouse|Planet & comet|Flower & butterfly|Tree & bird|High five|Hand in hand|Facing cats|Cheers to us|Pass it on|You through my eyes|Our soundtrack|A little hug|Two otters|Paper letters|Two-player mode|Puzzle partners|Side by side|Camp companions|Two cities|Book & bookmark|Coffee & croissant|Vinyl & cassette|Departure & arrival|Two lights at home'.split('|')
assert len(single_names) == 68 and len(pair_names) == 30

def size(path):
    return struct.unpack('>II', path.read_bytes()[16:24])

def encode(source, target, width, quality=84):
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return
    subprocess.run([CWEBP, '-quiet', '-q', str(quality), '-m', '6', '-resize', str(width), '0', str(source), '-o', str(target)], check=True)

data = json.loads((ROOT/'scripts/content.json').read_text())
groups, variants = [], []
(ROOT/'assets/designs').mkdir(parents=True, exist_ok=True)
for filename in ['generation-prompts.json', 'generation-prompts-iteration-02.json', 'generation-prompts-paired-series.json']:
    for item in json.loads((SOURCE/filename).read_text())['variants']:
        key = item['id'].lower()
        number = int(key.split('-')[1])
        paired = key.startswith('p-')
        source = SOURCE/item.get('final_file', item['filename'])
        w, h = size(source)
        output_width = 960 if paired else 720
        name = (pair_names if paired else single_names)[number-1]
        record = {'id':key, 'name':name, 'name_zh':item['name'], 'kind':'paired' if paired else 'single',
                  'source':str(source.relative_to(VAULT)), 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                  'image':f'/assets/designs/{key}.webp', 'thumb':f'/assets/designs/{key}-360.webp',
                  'width':output_width, 'height':round(h*output_width/w)}
        groups.append(record)
        encode(source, ROOT/record['image'].lstrip('/'), output_width)
        encode(source, ROOT/record['thumb'].lstrip('/'), 360, 80)
        for side in (['a','b'] if paired else ['']):
            variants.append({'id':key+('-'+side if side else ''), 'group':key, 'name':name+(' · Side '+side.upper() if side else ''),
                             'side':side, 'image':record['image'], 'width':record['width'], 'height':record['height']})
data['designs'], data['variants'] = groups, variants
data['featured_designs'] = ['st-12','st-27','st-31','st-42','st-46','st-50']
data['featured_pairs'] = ['p-01','p-13','p-21']
data['lifestyle'] = []
(ROOT/'assets/everyday').mkdir(exist_ok=True)
for scene in json.loads((SCENES/'scenes.json').read_text()):
    source = SCENES/'final'/f'{scene["id"]}.png'
    record = {k:scene[k] for k in ['id','style','title','copy']}
    record.update({'image':f'/assets/everyday/{scene["id"]}.webp','width':1440,'height':960,
                   'source':str(source.relative_to(VAULT)), 'provenance':'AI-generated environment with original product pixels composited from a locked source layer; not a customer photo or a camera sample.'})
    if source.exists():
        for width in [480,960,1440]:
            suffix = '' if width == 1440 else '-'+str(width)
            encode(source, ROOT/f'assets/everyday/{scene["id"]}{suffix}.webp', width)
        record['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    data['lifestyle'].append(record)
assert len(groups) == 98 and len(variants) == 128 and len({v['id'] for v in variants}) == 128
(ROOT/'scripts/content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'design_images':len(groups),'selectable_designs':len(variants),'lifestyle_images':len(list((ROOT/'assets/everyday').glob('*[0-9a-z].webp')))},indent=2))
