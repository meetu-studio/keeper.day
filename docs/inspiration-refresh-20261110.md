# Keeper inspiration imagery — 2026-11-10

Resource version: `20261110-inspiration-live`.

## Published content

- All 26 Keeper scene images are used in the four-language everyday gallery. Seven theme filters, direct scene links, original style selection and copy/share controls accompany the photographs.
- Homepage: new friends image, six scene picks, gifting image and after-photo image. Product page: travel, friends and desk images. Gifting page: the new gift scene. Guide and brand image slots use the same configured library.
- The 12 existing candid photo ideas remain on the site. Original camera, exterior and standard package images remain available.
- Each generated scene is identified as AI-generated; screen photographs are simulated. These are not customer submissions or camera sample photographs. Gift wrapping in the new scene is styling, not the included package.
- New files: 26 × 480/960/1440px WebP, 3:2, 78 files total. Full compositions are preserved on mobile.

## Maintenance

- Image and scene mapping: `scripts/editorial-content.json`, `images` and `inspiration`.
- Copy: `scripts/locales/en.json`, `zh.json`, `ja.json`, `ko.json`. All scene names, prompts, labels and controls are translated.
- Each scene has an id, category, style, image base, title, story, alt, source and placeholder state. Change all repeated image-slot mappings when replacing a scene.
- To replace a photograph, export the same three sizes, update the image path and source, and translate the title/story/alt if needed. Remove the AI marker only after replacing the actual scene and screen with verified photography.
- Original PNGs, prompts, compositing SVG layers and shooting instructions live in the project vault under `attachments/keeper-day/instax-inspired-20261110/`. They are not duplicated in this public repository.
- Run `python3 scripts/build_site.py` and `python3 scripts/check_site.py`, then inspect desktop/mobile pages before publishing.

## Release checks

- Static check: 76 pages, four languages, 98 original designs, 128 choices and 512 localized checkout mappings passed.
- Scene audit: 26 unique scenes, 78 valid WebP dimensions, 104 localized scene share links and valid style ids passed.
- Browser: four languages × four pages × five widths (320, 390, 768, 1024, 1440), 80 layouts; no horizontal overflow or clipped scene compositions.
- Theme filtering, scene deep links, clipboard copy, language links preserving scene selection, and all 26 selection links without JavaScript passed in four languages.
- Mobile chat launcher is on the left (x=16–142) and checkout on the right (x=261–374) at 390px; checked after scrolling past the hero CTA. Live chat was not contacted.
- JavaScript syntax checks passed for editorial.js, storefront.js and language.js.
- design-taste-frontend: GATE: ERROR — consistency.mjs could not walk 1440, 390. No FAIL in checks that ran; four nonblocking copy warnings. The gate was not rerun. The independent browser checks above cover the changed layouts.
- No live payment was submitted. Checkout amount/configuration and tracking consent were not changed.

## Scene usage and replacement ids

- `01-self-portrait` — A smile in the garden. — `st-42` — `friends` — `/assets/inspiration/20261110/01-self-portrait-{480,960,1440}.webp`
- `02-nature-walk` — Bring the lake along. — `st-46` — `travel` — `/assets/inspiration/20261110/02-nature-walk-{480,960,1440}.webp`
- `03-favorite-people` — Friends outside the café. — `st-50` — `friends` — `/assets/inspiration/20261110/03-favorite-people-{480,960,1440}.webp`
- `04-color-walk` — Follow a color. — `st-31` — `travel` — `/assets/inspiration/20261110/04-color-walk-{480,960,1440}.webp`
- `05-two-perspectives` — A friend and their dog. — `p-01-a` — `pets` — `/assets/inspiration/20261110/05-two-perspectives-{480,960,1440}.webp`
- `06-your-city` — Your own street corner. — `st-12` — `travel` — `/assets/inspiration/20261110/06-your-city-{480,960,1440}.webp`
- `07-love-story` — Across the café table. — `st-50` — `friends` — `/assets/inspiration/20261110/07-love-story-{480,960,1440}.webp`
- `08-new-beginnings` — The first day at home. — `st-31` — `gifts` — `/assets/inspiration/20261110/08-new-beginnings-{480,960,1440}.webp`
- `09-graduation-news` — Keep graduation day. — `st-27` — `campus` — `/assets/inspiration/20261110/09-graduation-news-{480,960,1440}.webp`
- `10-thank-you` — A photograph to say thanks. — `st-50` — `gifts` — `/assets/inspiration/20261110/10-thank-you-{480,960,1440}.webp`
- `11-carry-a-photo` — Ready for a walk. — `st-42` — `pets` — `/assets/inspiration/20261110/11-carry-a-photo-{480,960,1440}.webp`
- `12-keys-to-a-day` — One look before you leave. — `st-48` — `pets` — `/assets/inspiration/20261110/12-keys-to-a-day-{480,960,1440}.webp`
- `13-notes-to-remember` — Notes from a walk. — `st-12` — `home` — `/assets/inspiration/20261110/13-notes-to-remember-{480,960,1440}.webp`
- `14-monthly-photo` — One photograph each month. — `st-31` — `home` — `/assets/inspiration/20261110/14-monthly-photo-{480,960,1440}.webp`
- `15-desk-photo` — Back at your desk. — `st-42` — `home` — `/assets/inspiration/20261110/15-desk-photo-{480,960,1440}.webp`
- `16-reason-to-go` — A reason to go again. — `st-46` — `travel` — `/assets/inspiration/20261110/16-reason-to-go-{480,960,1440}.webp`
- `17-college-life` — Between classes. — `st-27` — `campus` — `/assets/inspiration/20261110/17-college-life-{480,960,1440}.webp`
- `18-birthday-person` — Today is their day. — `p-01-a` — `gifts` — `/assets/inspiration/20261110/18-birthday-person-{480,960,1440}.webp`
- `19-place-at-the-table` — Around the brunch table. — `st-50` — `food` — `/assets/inspiration/20261110/19-place-at-the-table-{480,960,1440}.webp`
- `20-gift-a-memory` — Put a memory in the gift. — `p-01-a` — `gifts` — `/assets/inspiration/20261110/20-gift-a-memory-{480,960,1440}.webp`
- `21-adventure-diary` — The morning at camp. — `st-46` — `travel` — `/assets/inspiration/20261110/21-adventure-diary-{480,960,1440}.webp`
- `22-food-diary` — Remember this breakfast. — `st-27` — `food` — `/assets/inspiration/20261110/22-food-diary-{480,960,1440}.webp`
- `23-weekend-tasting` — A slow weekend table. — `st-12` — `food` — `/assets/inspiration/20261110/23-weekend-tasting-{480,960,1440}.webp`
- `24-flowers-and-photo` — Keep the flowers in bloom. — `st-50` — `home` — `/assets/inspiration/20261110/24-flowers-and-photo-{480,960,1440}.webp`
- `25-frame-the-day` — A familiar face at home. — `st-31` — `pets` — `/assets/inspiration/20261110/25-frame-the-day-{480,960,1440}.webp`
- `26-holiday-memory` — After the decorations come down. — `p-01-a` — `gifts` — `/assets/inspiration/20261110/26-holiday-memory-{480,960,1440}.webp`
