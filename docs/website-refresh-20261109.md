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
