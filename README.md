---
type: Note
status: Active
url: https://keeper.day/
---

# Keeper content-led website

## Information architecture

The site is a visual product story, not a single checkout landing page. Each collection is a permanent, directly linkable page.

| Page | Editorial purpose | Primary content |
| --- | --- | --- |
| `/` | Introduce the camera and the wider Keeper design world | Paired hero, standard camera, pair designs, switchable display scenes, personal styles, lifestyle album, preorder |
| `/camera.html` | Explain the standard camera and buying terms | Photo-preview switcher, e-paper, photo ritual, checkout breakdown, FAQ |
| `/together.html` | Make the existing paired design library visible | 12 complementary two-device artwork concepts |
| `/little-apps.html` | Show specific screen ideas and the current configuration direction | 4 standalone display scenes; G/H/I/J configuration concepts; preview switcher and category filters |
| `/styles.html` | Explore personal expression | 12 individual surface-art designs |
| `/moments.html` | Place Keeper in everyday life | 8 lifestyle/design scenes: friends, college, desk, pet, wedding, birthday, family gift, anniversary |
| `/terms.html`, `/privacy.html` | Legal and support | Existing policies; official support address |

## Asset selection and boundaries

The curated manifest contains 40 image entries. Existing project sources are converted to WebP with proportional resizing, never stretched, mirrored, redrawn or used to invent hardware geometry. Each entry records its source, dimensions, alt text and editorial caption in `scripts/content.json`.

- Paired artworks are concepts, not two-camera bundles, shipping editions or wireless photo-sharing demonstrations.
- App concepts use the current G → H → I → J direction: choose a scene, edit style/layout, choose widgets/schedules, review configuration. Historical A/B photo-transfer flows are deliberately excluded.
- Four independent display scenes show a calendar, water reminder, sample travel information and anniversary countdown. Weather, quotes, checklist and scheduling are shown inside the existing widget UI, not presented as released features.
- No complete focus-timer demo or music-player UI was found; neither is represented as an implemented feature.
- Complete lifestyle compositions replace narrow historic crops where possible. Advertising text embedded in the original artwork is retained rather than silently cropping away product/context. Full-image links let readers inspect details.
- AI lifestyle images are labeled illustrations, not customer photographs or testimonials. Gift packaging and accessories shown are not promised shipping contents.
- Product geometry in old generated artwork remains illustrative; the standard-camera page retains the original product reference layers.

## Commercial source of truth

One standard camera: US$199 + US$20 US shipping = US$219 paid in full today. US only. In development; expected August 2027. Full pre-shipment refund including shipping. Returns within 14 days of delivery, unused and in original packaging. Customer pays change-of-mind return shipping; studio pays shipping for quality issues. Concept artwork, finishes, companion apps and connectivity are not included launch promises.

Checkout remains the existing Stripe payment link. This rebuild does not change Stripe or HubSpot configuration. Official support: support@keeper.day.

## Build and maintenance

Hosting is plain static GitHub Pages: no runtime framework or npm installation is required.

- `scripts/prepare_assets.py`: run inside the original project vault with Pillow installed to regenerate curated WebP files and `scripts/content.json`.
- `scripts/build_site.py`: standard-library Python builder; generates the six editorial pages and sitemap from the manifest plus preserved product/checkout components in `scripts/components.json`.
- `scripts/check_site.py`: standard-library checks for internal links/anchors, image existence/alt attributes, duplicate IDs, one H1 per page, support address and required commercial terms.
- `experience.css`: collection/editorial layouts and responsive overrides.
- `site.js`: native mobile menu handling, product photo preview, display-scene preview, app category filtering, existing support chat and preorder analytics.

Commands from this repository:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check site.js
git diff --check
```

Edit generator/component inputs before rebuilding; direct generated-HTML edits will be overwritten. Update cache-busting versions after changing CSS/JS for a subsequent public release.

## Release review

Before publishing, check all six pages at 320, 390, 768 and 1440px; open the mobile menu; switch camera and app previews; verify all filters and full-image links; confirm checkout pricing without making a purchase; verify support/legal links. Publish only this nested repository (`meetu-studio/keeper.day`), never the surrounding notes repository. Confirm GitHub Pages deployment and all public URLs after push.
