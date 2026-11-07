---
type: Note
status: Active
url: https://keeper.day/
---

# Keeper in-stock storefront

## The current offer

Owner-confirmed on November 8, 2026: **US$199 camera + US$30 worldwide shipping = US$229**. In stock. The standard package includes **one camera, one gift box, one lanyard and one instruction manual**.

[Commerce configuration](<scripts/commerce.json>) is the single commercial input. The verified live [Stripe checkout](https://buy.stripe.com/4gM7sK5cwdrh09Oe1Q6kg01?locale=en) offers 232 destinations and quantity one. Stripe may offer optional local-currency conversion; USD checkout is US$229. Destination customs taxes/duties and issuer fees are not included in that amount. See [checkout verification](<docs/stripe-in-stock-review.md>).

No specific dispatch/transit SLA, warranty duration, measured runtime, storage-card inclusion, weight, dimensions, charging time or included cable is promised. Existing order commitments remain unaffected by the new offer. Cancellation before shipment refunds the full camera price and shipping; requests for unused returns in original packaging are accepted within 14 days after delivery. For eligible change-of-mind returns, refund US$199 only: original US$30 outbound shipping is not refunded. Buyer pays non-quality return shipping; studio covers quality-issue return shipping. See [policy source](<scripts/policies.py>).

## Information architecture

| Route | Purpose |
| --- | --- |
| `/` | Product-first introduction, immediate price/buy link, practical benefits, included kit, how it works, everyday uses and answers |
| `/camera.html` | Product gallery, direct purchase, package contents, e-paper education, functional specifications and buying questions |
| `/gifting.html` | Gift-box presentation, included items, recipient/use ideas and gift timing guidance |
| `/support.html` | Camera, ordering, shipping, cancellations, returns and support contact |
| `/moments.html` | Photographic everyday album with clear AI provenance |
| `/terms.html`, `/privacy.html` | Current retail terms and privacy disclosures |
| `/together.html`, `/styles.html`, `/little-apps.html` | Clearly separated design-studio collections, linked in the footer rather than presented as purchasable features |

The 42-entry legacy collection manifest remains available, including the two previously approved natural American lifestyle scenes. App concepts, skins and paired artwork are not released-product promises or purchase options. No invented customer reviews, ratings, press logos, stock counters or discount anchors are used.

## Photography and provenance

New photographic WebP assets are in [the storefront asset folder](<assets/storefront/>). Complete AI-generated compositions are conditioned on original hardware references; no pasted product cutouts are used. The generated images depict the cream portrait body, main color e-paper display, red lower-left button and separate lower-right LCD. They are visualizations, not measured hardware evidence, customer photographs or production-camera sample output. A small site-wide disclosure and more specific gallery language preserve that distinction.

The owner's confirmed contents list, not incidental image props, defines the supplied package. Generated gift-box styling is illustrative; ribbon, fitted trays and environmental props are not additional promised accessories. Photography can later be replaced without changing the purchase model.

## Build and maintenance

Plain static GitHub Pages. No runtime framework, database or npm install is needed.

- [Page builder](<scripts/build_site.py>): shared header/footer, metadata, Product/InStock structured data, ten content pages, a 404 page and sitemap.
- [Storefront bodies](<scripts/storefront.py>): product-first homepage, product, gifting and support page content.
- [Commerce input](<scripts/commerce.json>): price, shipping, included items and verified checkout URL.
- [Retail policy source](<scripts/policies.py>) and [privacy source](<scripts/privacy-body.html>): legal-page bodies.
- [Storefront styles](<storefront.css>) and [interactions](<storefront.js>): responsive product layouts and accessible gallery/purchase controls.
- [Privacy controls](<consent.js>) and [privacy layout](<consent.css>): optional analytics, advertising and HubSpot remain inert until consent; footer settings can withdraw it.
- [Shared interactions](<site.js>): navigation, support chat and checkout-click analytics. A click is never recorded as a paid purchase.
- [Release checks](<scripts/check_site.py>): links, anchors, image dimensions/alt text, headings, analytics identifiers, price consistency and rejection of stale commercial text.
- [Collection asset builder](<scripts/prepare_assets.py>): regenerates legacy curated assets from the original vault sources using Pillow.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check site.js
node --check storefront.js
node --check consent.js
git diff --check
```

Edit source modules, not generated HTML. Update cache-busting version for later public releases. Preserve GA `G-783F93X4HE`, Meta `1113554937986944`, Clarity `z98vqpb6j4`, HubSpot portal `247894352`, and support@keeper.day.

## Release gates

Check every public page at mobile and desktop widths, keyboard navigation, mobile menu, gallery selection, sticky purchase bar, image decoding and overflow. Verify exact Stripe URL, USD229 total and destination choices without making a purchase. Confirm legal/support paths and distinguish actual features from concepts. Publish only this nested `meetu-studio/keeper.day` repository, never the surrounding notes vault. Verify the production deployment and current assets after publication; local build success alone is not release proof.
