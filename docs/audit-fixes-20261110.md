# Keeper camera storefront audit fixes — 2026-11-10

Kind: product / tech. Existing paper white, ink and red palette; IBM Plex Sans; static photography; compact, varied sections. The approved compact layout, real contact details and visible AI/example labels take precedence over the skill defaults for screen-height sections, `.example` contacts and image captions.

## What changed

- Home order: camera hero and price → frame/shutter/photo sequence → four shopping routes → camera essentials → visual exteriors → e-paper → four photo-diary previews → six inspiration stories → style finder → combined gift/pairs/package → compact example reviews → media/cooperation → guides/updates → brand → community → service/FAQ → preview newsletter → purchase/footer.
- Phone hero uses category/title, photograph, price/CTA, supporting copy. At 390×844, the first-visit cookie controls, US$199 price, US$229 total and purchase action fit on screen in all four languages.
- Product gallery displays selection/quantity above the original image. Paired images retain both original cameras; A/left and B/right buttons outline the chosen side. Sticky purchase text repeats the side and one-camera quantity. A pair without a side requires selection before checkout.
- Replaced the 129-option native exterior select with seven visual shortcuts and an expandable searchable catalog. Names in all four languages and ST/P IDs are searchable. Static catalog links provide every patterned checkout without JavaScript; the main no-JS checkout remains Classic cream.
- Locale links update after style selection, browser history and anchor changes. Language remains the rightmost header control. Chat remains left on mobile, and an open HubSpot conversation hides the purchase bar.
- Confirmed by the owner for this update: direct phone connection for photo export; two charges a year, with usage-dependent battery life. No unverified phone model list, app workflow, weight or memory-card inclusion added. Product/support/guide copy agrees. Warranty text preserves statutory rights in the applicable sales region without inventing a worldwide fixed term.
- SolidCraft inspection identified the active 墨水屏拍立得 assembly, but native measurement was unavailable. No dimensions have been published from old notes or guessed from images.

## Images and replacement

No new scene generation or product repainting was needed. Existing original product images and approved scene library remain the source. The home uses distinct major scene assets: hero 03, photography process original shooting/shutter + 25, gifting 20, brand 15, guides carry 11/street 04/café 07, inspiration 01/09/13/18/22/26. The first shopping exterior changes to ST-11 to avoid repeating the ST-50 featured product.

The four main diary previews are friends-pizza, pets-dog, street-rain and family-birthday. Community previews retain outdoors-lake, friends-rooftop, pets-cat and details-diner. The gallery still contains all 26 inspiration scenes and 12 diary photographs.

Added 20 width-240 WebP derivatives from the existing width-480 assets (`cwebp -resize 240 0 -q 82`); no geometry or content edits. Editorial row previews and product thumbnails use these small resources. Existing 480/960/1440 assets remain. Photo `sizes` now reflects hero, two-column, three-column and small-row usage.

For real-photo replacement, retain each `scripts/editorial-content.json` image base, export matching responsive dimensions, update alt/source/placeholder status in all four languages, and remove the AI label only for the replaced real asset. Product design originals and P side mapping remain unchanged. The full original prompts, editable layers and shooting directions remain in the vault's `instax-inspired-20261110` and `website-shooting-references-20261109` asset libraries.

## Verification

- Static build and site checker: 76 pages, 4 languages, 98 design images, 128 patterned choices, no errors. Translation and placeholder matching enforced by the build.
- Browser: 4 languages × home/product/styles × 320/390/768/1024/1440 = 60 distinct layouts, no horizontal overflow or missing eager image. A long run stopped on its 55th screenshot; remaining Korean checks were completed in a fresh browser. The interrupted run is retained and not described as a complete pass.
- Each of 128 selections switched in every language: 512 dynamic checkout-reference and locale checks passed. P pending-side block, A/B highlight, catalog search, language-query preservation and no-JS checkout links passed.
- Browser language tests: zh-TW, ja-JP, ko-KR, en-GB, ordered mixed preferences, unsupported-language fallback, stored manual choice, explicit Japanese URL and explicit English query passed. Storage-disabled Japanese fallback passed separately.
- Menu Escape/focus, FAQ, cross-language name search, finder recommendations, gallery dialog keyboard close and copy-link fallback checked. Headless clipboard access fell back to a selectable URL; native clipboard success is not claimed.
- Desktop full-scroll browser observation: 12,508px page, no broken displayed image, about 1,906 KiB image transfer, largest image about 114 KiB. This is a local warmed browser observation, not a field-performance measurement or a complete performance-tool pass.
- Stripe hosted checkout was opened in the normal browser in English, Chinese, Japanese and Korean. All four showed the corresponding standard interface and a US$229 option. English USD selection confirmed US$199 item + US$30 shipping = US$229. The other three remained in the existing adaptive local-currency default; a CAPTCHA appeared in the normal browser, so no CAPTCHA was solved and no payment interaction was attempted. Client reference and locale were verified on the outgoing URLs; the reference is not a customer-visible Stripe line item.
- No customer data, chat messages or payments were submitted. Preview forms remain disabled. HubSpot did not load in the localhost test within 20 seconds; live chat loading remains for the post-deployment browser check.

## Design tool limits

`GATE: ERROR (consistency.mjs could not walk 1440, 390)`.

The layout checker again crashed with `Cannot read properties of undefined (reading 'map')`. The performance script produced no report after its Chrome process exited; only that run's remaining Node process was stopped. These tools are not marked passed. Independent browser evidence covers the layout and functional results listed above.

Existing waiver: the `.storefront` wrapper supplies centered 1280px content and equal gutters rather than the kit's `.wrap` class. Copy lint has zero FAILs. Retained warnings are actual studio-update dates, the explicitly labelled fictional review name Maya, and product/catalog em-dash separators. No kit files were altered to suppress findings.

## Release

Resource version: `20261110-camera-audit-fix`. Price, USD checkout, CNAME and consent-controlled tracking configuration remain unchanged. Commit/deployment links and ordinary-refresh production screenshots are recorded in the vault maintenance note `keeper-day-website-refresh-20261109.md` after deployment.
