---
type: Note
status: Implemented and locally verified
updated: 2026-11-09
---

# Keeper exterior collection and everyday website refresh

The existing 11-page in-stock storefront now presents 68 individual exterior looks and 30 paired illustrations. Paired A/left and B/right are separate one-camera selections, giving 128 patterned choices. Classic cream remains available. Each order includes one camera with the selected exterior, gift box, lanyard and manual: USD199 + USD30 worldwide shipping = USD229.

The homepage brings photographic context, featured exterior designs and paired looks into the main shopping flow. Search and collection filters cover all 98 original design images. Product selection updates the main image and thumbnail, name, side explanation, share URL and purchase links. `client_reference_id=keeper-<variant>` records the selection on the existing Stripe Checkout Session. All 128 direct design purchase links are present in static HTML for JavaScript-disabled browsing.

Eight new American everyday scenes cover a café, college, hiking, family birthday, work desk, skating, pets and a paired gift. They use built-in Imagegen environments with locked original product layers. The final source PNG opaque product regions were compared with the locked source layers with zero differing pixels across all eight images; published WebP assets are compressed derivatives. Photography remains identified as illustrative, not customer imagery or camera samples.

Local acceptance includes 55 layout cases across 11 pages at 320, 390, 430, 768 and 1440 CSS pixels; all 128 live selector mappings; paired-side selection; search/filter; actual clipboard write/read; gallery keyboard navigation; mobile menu/Escape; and static no-JavaScript purchase links. Existing analytics, support, optional-service consent, retail policies and domain configuration are retained.

Original prompts, source hashes, layers, image proofs, browser evidence and the complete Chinese maintenance note live in the local project vault. The repository README documents build, photo replacement and Stripe fulfillment lookup.

## November 9 follow-up: photography first

The homepage now opens on a hiker using a landscape Keeper to photograph two friends. Its category is “A pocket camera with color e-paper” and the headline is “Small camera. Everyday stories.” Framing, the physical red shutter and the resulting photograph appear before exterior shopping. A labeled original-product diagram distinguishes the small LCD viewfinder, shutter and large photo display. The gifting page leads with a parent photographing a family birthday. Product copy, galleries, social sharing and metadata follow the same camera story.

Two new ST-46/ST-27 camera-use scenes join the eight everyday images. Their source bodies are rotated and uniformly placed from existing product artwork, with no body repaint or perspective warp. Matching simulated photographs are restricted to the original screen interiors, and hand occlusions are restored above the body. PNG proof compares exposed body pixels outside these explicit masks and a one-pixel antialiasing boundary: zero differing pixels for both scenes. These remain AI-created scenes with simulated displays, not camera sample output.

Resource version: `20261109-camera-1`. Local verification passed 55 layouts, 128 variant mappings, paired A/B, filter/search, clipboard write/read, gallery keyboard, mobile menu/Escape, FAQ and no-JavaScript purchase links. USD pricing and checkout mechanics are unchanged. Release and production evidence are recorded in the local Chinese maintenance note.

## November 9 follow-up: four static languages

English retains the root URLs. Simplified Chinese, Japanese and Korean are available under `/zh/`, `/ja/` and `/ko/`: 44 complete HTML pages and 40 indexable sitemap URLs. Navigation, body copy, exterior names, image descriptions, policy text and dynamic messages use the same four static catalogs. Missing keys, empty translations and inconsistent named placeholders fail the build.

Unspecified root entries choose a saved manual preference, then the first supported browser language, with English fallback. Explicit language paths remain stable. English links use `?lang=en` when a fixed English selection is needed. Switching preserves the page, selected design/side, campaign parameters and fragment; browser storage failure does not prevent navigation or checkout. The shared 404 localizes in place and retains the failing URL and status.

All 128 patterned choices retain their IDs, A/left and B/right mapping, one-camera quantity and USD199 + USD30 = USD229 pricing. Stripe standard checkout receives the selected `locale`; its product configuration and reference IDs are preserved. Policy text now states that the selected ST/P exterior is included and one P side is one camera. The language preference is documented separately from optional-service consent.

Resource version: `20261109-i18n-1`. Local acceptance covers 176 desktop/mobile layouts, 512 variant mappings, all-language and full-width search, clipboard readback, A/B selection, no-JavaScript catalogs, FAQ, mobile menu/Escape and in-place 404. Eight targeted mobile header cases verify single-line menus after the Japanese narrow-screen correction. The existing camera-led imagery is reused. Production evidence is kept in the project maintenance note.
