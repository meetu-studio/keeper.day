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
