"""Smaller copies of the home and product pages' photos, so a browser can pick the size it needs (srcset).
For every <name>-1440.webp or <name>-960.webp in each photo folder, make <name>-960.webp and <name>-480.webp beside it
when they are smaller than the source and do not exist yet. Existing files are never touched.
Run: python3 -I scripts/redesign/make_sizes.py   (from the site root; 2026-11-20)"""
import pathlib, subprocess, sys, tempfile
SITE = pathlib.Path(__file__).resolve().parents[2]
FOLDERS = ['assets/redesign/photos-20261120', 'assets/redesign/photos-20261120-recast']


def size(p):
    w, h = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(p)],
                          capture_output=True, text=True, check=True).stdout.strip().split(',')
    return int(w), int(h)


made = 0
with tempfile.TemporaryDirectory() as tmp:
    for folder in FOLDERS:
        d = SITE / folder
        if not d.is_dir():
            continue
        for src in sorted(d.glob('*.webp')):
            base, _, tail = src.stem.rpartition('-')
            if tail not in ('1440', '960'):
                continue
            W, H = size(src)
            for w in (960, 480):
                out = d / f'{base}-{w}.webp'
                if w >= W or out.exists():
                    continue
                h = round(H * w / W / 2) * 2
                png = pathlib.Path(tmp) / 'p.png'
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-vf', f'scale={w}:{h}:flags=lanczos,format=rgb24', str(png)], check=True)
                subprocess.run(['cwebp', '-quiet', '-q', '82', '-m', '6', '-metadata', 'none', str(png), '-o', str(out)], check=True)
                assert size(out) == (w, h), out
                made += 1
    # the look picker's swatches show at about 78 px; a 240-wide copy covers a 3x phone (the old 360-659 px files stay)
    SWATCHES = {'classic': 'product-flowers.webp', 'st-12': 'designs/st-12-360.webp', 'st-27': 'designs/st-27-360.webp',
                'st-31': 'designs/st-31-360.webp', 'st-42': 'designs/st-42-360.webp', 'st-50': 'designs/st-50-360.webp',
                'p-01-a': 'redesign/p-01-a.webp', 'p-01-b': 'redesign/p-01-b.webp'}
    sw = SITE / 'assets/redesign/swatches-20261120'
    sw.mkdir(exist_ok=True)
    for lid, rel in SWATCHES.items():
        out = sw / f'{lid}-240.webp'
        if out.exists():
            continue
        src = SITE / 'assets' / rel
        W, H = size(src)
        h = round(H * 240 / W / 2) * 2
        png = pathlib.Path(tmp) / 'p.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-vf', f'scale=240:{h}:flags=lanczos,format=rgb24', str(png)], check=True)
        subprocess.run(['cwebp', '-quiet', '-q', '84', '-m', '6', '-metadata', 'none', str(png), '-o', str(out)], check=True)
        made += 1
print('made', made, file=sys.stderr)
