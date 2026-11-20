---
type: Note
status: Active
url: https://keeper.day/
---

# Keeper · a pocket camera with a color e-paper display

Static GitHub Pages website for keeper.day, built with the existing Python page builder and plain CSS/JavaScript. No runtime framework or environment variables.

## Offer

Owner-confirmed November 9, 2026: one camera with the selected exterior, gift box, lanyard and instruction manual. USD199 + USD30 worldwide shipping = USD229. Existing shipping, cancellations, returns and support terms remain in their policy source. The checkout link and commercial inputs are in `scripts/commerce.json`.

68 ST looks and 30 P pairs are available. A (left) and B (right) are each one-camera choices: 98 source images, 128 selectable designs, plus the existing Classic cream camera. A paired illustration does not change order quantity.

## Pages

- `/`: camera-in-use hero and visible offer, viewfinder/shutter/photo explanation, everyday photography, color e-paper, exterior choices, paired looks, gift package and questions.
- `/camera.html?style=st-31`: exterior selector, product gallery, price and purchase.
- `/styles.html`: all 98 design images; search by name or number and filter individual/paired looks.
- `/together.html`: all 30 pairs with separate A/B selections.
- `/moments.html`: two active camera-use scenes and eight American everyday settings, linked to the relevant exterior.
- `/gifting.html`, `/support.html`, `/terms.html`, `/privacy.html`: existing gift, support and retail policies.
- `/little-apps.html`: clearly described interface concepts.

## Sources and build

- `scripts/content.json` is the shared image, design and variant manifest. It contains 98 design groups, 128 variant records, eight lifestyle records and two camera-use story records.
- `scripts/prepare_refresh_assets.py` reads existing original product images and final scene PNGs from the local project vault and emits responsive WebP assets. Its vault path and converter path are explicit constants.
- `scripts/storefront.py` renders retail content, design cards, catalogs and the selector payload. `scripts/build_site.py` renders shared navigation, metadata, footer and the 11 pages.
- `storefront.js` handles progressive gallery, search/filter, selection and sharing. Static catalog purchase links also work without JavaScript.
- `consent.js` keeps optional analytics and chat off until consent. Preserve the existing GA4, Meta, Clarity, HubSpot and support identifiers.

Run:

```sh
python3 scripts/prepare_refresh_assets.py
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check storefront.js
node --check site.js
node --check consent.js
git diff --check
```

## Selected design in Stripe

Payment Links retain the existing fixed price, shipping and one-camera quantity. The selected design is passed as `client_reference_id=keeper-st-31` or `keeper-p-01-b`. Find that reference on the paid Checkout Session or its `checkout.session.completed` event (`data.object.client_reference_id`) to identify the exterior for fulfillment. Classic cream uses the original link without a patterned-design reference. The public website does not contain payment secrets.

The shared URL is `/camera.html?style=<variant>`. Product selection updates the image, side explanation, name, URL and all current-purchase buttons. Incomplete paired identifiers ask for A/B; unknown identifiers ask the visitor to select a valid design. No-JavaScript buyers use each design’s own static Buy one link.

## Camera-led marketing

Introduce Keeper as a pocket camera. Start with the person or scene someone wants to photograph, show framing and the physical red shutter, then show a favorite photograph retained on color e-paper. Portability, exteriors and gifts support taking the camera along. Interface ideas remain in the studio sketchbook.

The November 9 follow-up adds two horizontal, two-handed photography scenes using ST-46 and ST-27. Original product bodies are rotated as a whole and uniformly scaled/translated. Only original screen interiors show matching simulated subject photographs; explicit hand masks preserve natural shutter contact. Visible body pixels outside those areas and a one-pixel antialias boundary match the locked layer. Sources, prompts, masks and proof are in the vault at `attachments/keeper-day/camera-marketing-20261109`.

## Photography replacement

The eight new lifestyle scenes use built-in Imagegen environments and original product layers composited with uniform scale/translation. Original pixels, generation prompts, intermediate layers and pixel-verification records are kept in the project vault under `attachments/keeper-day/website-refresh-20261109`. Final PNG dimensions are 1536×1024; published WebP sizes are 480, 960 and 1440 wide. Artwork and screen images are illustrative, not customer photographs or camera sample output.

For the camera-use hero and gifting scene, replace the corresponding PNG under `camera-marketing-20261109/final/`; the other eight remain under `website-refresh-20261109/final/`. Replace with a real photograph, update its provenance/caption, and run the asset and page builders. Do not rerun the scene composer over replaced real photographs. Increment the builder resource version, run checks and verify Pages plus an ordinary browser refresh. Preserve `CNAME` as `keeper.day`.

## Languages and automatic selection

English keeps the existing root URLs. Simplified Chinese, Japanese and Korean have complete static pages under `/zh/`, `/ja/` and `/ko/`. The build generates 44 HTML pages, with 40 indexable URLs in the sitemap. Each language has its own canonical, alternate-language links, metadata, alt text and share text.

Unspecified root URLs use a saved manual choice, then the first supported `navigator.languages` preference, and otherwise English. All `zh-*` preferences use Simplified Chinese. An explicit language directory always wins. `?lang=en` explicitly requests English, including in English share URLs. The selector preserves the current page, query parameters, design/side and fragment. The interface preference is stored separately from optional analytics consent as `keeper-language-v1`; browser storage failure leaves language links and core shopping available.

The four `scripts/locales/*.json` catalogs contain `text` (exact source copy), `ui` (named message templates) and `designs` (98 names keyed by permanent design ID). The HTML localizer operates at build time; it does not call a translation service. `scripts/content.json` remains the language-independent image/variant source. All four design names and IDs are indexed for search. JavaScript reads the current page's generated message catalog; no display text should be added directly to interactive handlers.

To change copy, update the English template and matching keys in all four catalogs, keep message placeholders identical, then run the existing build and checks. A missing key, blank translation or placeholder mismatch blocks the build. English price text is consistently rendered with the US$ prefix. Checkout keeps one camera and the same price; only `locale=en/zh/ja/ko` and the selected `client_reference_id` vary.

The shared GitHub Pages 404 includes generated language fragments. Its small bootstrap changes the content in place for unknown paths, retaining the failing URL and HTTP 404 status. No-JavaScript visitors can use the static language links; every translated catalog includes all 128 direct purchase choices.

Stripe's standard checkout interface follows the selected locale. Product names/custom text configured in Stripe, HubSpot conversation content and transactional emails remain provider-managed. Original images, including any words within images, are reused.

Frontend refinement (9 November): compact header with the current language visible, larger touch targets, text/price/action before the hero photograph on phones, and a purchase bar that yields to visible page actions. Resource version `20261109-frontend-1`. See `docs/frontend-polish-20261109.md` for decisions and separate project/skill validation results.

Language picker follow-up (9 November): a single current-language dropdown now sits in the header at every screen size. It uses native details/summary and four static language links, with keyboard, Escape, outside-click and mutual menu closing. Automatic matching, remembered choice and current product URL parameters are preserved. Resource version `20261109-language-menu-1`.

Camera-brand redesign (9 November): campaign hero, camera-first product layout, four-language copy, retained 128-style selection and responsive street imagery. Version `20261109-camera-brand-2`. Project asset sources, image prompt, replacement and validation records are kept in the vault maintenance note.

## 2026-11-20 · New home page and product page

The home page (`/`, `/zh/`, `/ja/`, `/ko/`) and the product page (`/camera.html` and its three translations) use the 2026-11-20 design. `scripts/redesign/build.py` writes them from `scripts/redesign/copy/<lang>.json`, with `keeper.css`, `keeper.js`, the page kit in `assets/kit/` and this design's own pictures in `assets/redesign/`. Every other page still comes from `scripts/build_site.py`.

The earlier 2026-11-11 design of both pages is kept, not removed: `scripts/build_site.py` now writes it beside the new pages as `index-20261111.html` and `camera-20261111.html` in each language, marked noindex and left out of the sitemap. It never writes `index.html` or `camera.html` again.

The new pages keep the site's working parts: `consent.js` and the optional-services block from `scripts/components.json` (analytics and chat load only after consent), `language.js` with its `keeper-i18n` packet, the script policy, canonical and hreflang links, the Product data, the `checkout_click` event, the `#choose-style` anchor and `?style=<id>` links from every other page, and the Stripe Payment Link with `client_reference_id=keeper-<id>` for every printed look. `scripts/check_site.py` checks the new picker (the same eight choices and localized names) and the kept copies.

Run, after the existing build:

```sh
python3 scripts/build_site.py
python3 scripts/redesign/build.py
python3 scripts/check_site.py
```

## 2026-11-20 · Brighter photos on the home page and product page

The owner found the scene photos on the new pages dark and muddy, with faces that did not look clean. Each of the 21 scene photos was regenerated as a bright commercial photograph from the original (the original was the reference image; daylight, clean whites, clean skin; Keeper's shell, buttons and orientation kept), with Codex image generation and with Gemini (`gemini-3.1-flash-image`). The owner picked one version per photo: 20 from Codex, the self-portrait from Gemini.

- New files: `assets/redesign/photos-20261120/`, at the same sizes as the photos they replace (1440×960 or 960×640). Average brightness went from 94–137 to 128–184 (0–255).
- `scripts/redesign/build.py` maps the old paths to the new files in `REFRESHED`; only the eight pages it builds use them. The old photos stay in place, unchanged, for the rest of the site.
- `storefront/full-kit.webp` was bright already and is unchanged. Prompts, candidates and the review page are in the owner's notes (`拍立得/attachments/keeper-day/website-photo-refresh-20261120/`).

## 2026-11-20 · Brighter photos on the other pages

The same refresh for the older pages (about, gifting, the three guides, learn, moments and press, in four languages). Their pictures come from two families: the inspiration photos (`assets/inspiration/20261110/`) and the photo-diary pictures taken with Keeper (`assets/photo-diary/20261110/`). Each was regenerated with Codex image generation from the original, with the brief used for the home page; the photo-diary pictures show no camera. The owner picked one version per photo: 23 regenerated, the desk photo (15) kept as it was, and a clear-skin edit for the flower portrait (24). The twelve inspiration photos already refreshed on the home page reuse the owner's earlier pick; 14 was bright already and is unchanged.

- New files: `assets/inspiration/20261120/` and `assets/photo-diary/20261120/`, with the same names and sizes as the originals (inspiration 240/480/960/1440, photo-diary 480/960/1440/full). Average brightness of the regenerated photos went from 94–138 to 128–190 (0–255).
- `scripts/build_site.py` points a page at the 20261120 file wherever one exists (`brighter()`); the kept 2026-11-11 designs (`index-20261111.html`, `camera-20261111.html`) keep the originals. The 20261110 files stay in place, unchanged.
- The pages listed a 240-wide size that some inspiration photos never had, a broken srcset entry since 2026-11-10. The refreshed photos have it in the new folder; for the originals still in use (01, 09, 13, 22 and 26 on the kept 2026-11-11 designs, and photo 14 everywhere) a 240 copy scaled from the original's 480 file was added beside them. No page now lists an image file that does not exist.

## 2026-11-20 · Faster home page and product page

The owner found the site slow. Measured in headless Chrome (`perf.mjs`, Chinese home page, before → after): 3.58 MB and 57 requests at load → 27–29 requests at load, and 2.0–2.2 MB at 1440 px / 1.07 MB at 390 px after scrolling the whole page; fonts 728 KB in 10 files → 138 KB in 2; first paint no longer waits for Google Fonts. The new bright photos and the scripts were not the cause (no long tasks).

- **Fonts.** The Google Fonts stylesheet loads without holding up the first paint (`media="print"` switched on load, with a `<noscript>` copy); the text shows in the fallback serif and sans until Fraunces and Figtree arrive. Noto Serif SC/JP/KR is no longer fetched: the Chinese, Japanese and Korean pages use the reader's system serif, which `keeper.css` already names (Songti SC, Hiragino Mincho, AppleMyungjo).
- **One kit stylesheet.** `assets/kit/kit-bundle.css` is the six kit stylesheets in their old order, written by `scripts/redesign/build.py` on every build; the six files are unchanged.
- **Photo sizes.** `scripts/redesign/make_sizes.py` adds 960 and 480-wide copies beside each photo in `assets/redesign/photos-20261120/`, and 240-wide copies of the look picker's swatches in `assets/redesign/swatches-20261120/` (they show at about 78 px). The build lists the sizes in `srcset` (`sizes="auto, …"` for lazy pictures). Existing files are unchanged.
- **Lazy pictures stay lazy.** `assets/kit/system.js` no longer switches every lazy picture to eager once the page has loaded (2.6 MB at once), and the photo list beside the stories fetches its photos when it comes within a screen, not at page start. The home page's look picker and order picture load lazily.
- Cloudflare does not cache the HTML (`cf-cache-status: DYNAMIC`); a Cache Rule for the HTML in the Cloudflare dashboard is the owner's to set.

Also in this change, not yet in use: the owner asked for no Black people in the photos. Both builds prefer a recast copy where one exists (`photos-20261120-recast/`, `inspiration/20261120-recast/`, `photo-diary/20261120-recast/`, `assets/og-card-20261120.webp`, `assets/redesign/share-20261120.jpg`). None exists yet, so no page changes until the owner picks the recast photos.
