# Keeper eight-look selection — 2026-11-10

The owner requested a maximum of eight choices instead of the 128-pattern catalog. The eight-choice cap includes Classic cream and counts each P side separately.

- Classic cream — existing base checkout, no patterned reference.
- ST-12 — Indie band — `keeper-st-12`.
- ST-27 — Candy stripes — `keeper-st-27`.
- ST-31 — Quiet geometry — `keeper-st-31`.
- ST-42 — Soft daydream — `keeper-st-42`.
- ST-50 — Garden stitches — `keeper-st-50`.
- P-01-A — Sun & moon, left — `keeper-p-01-a`.
- P-01-B — Sun & moon, right — `keeper-p-01-b`.

Every choice remains one camera with the selected exterior, gift box, lanyard and manual: US$199 + US$30 shipping = US$229. There is no two-camera purchase option.

## Implementation

`scripts/content.json` contains the eight `active_choices`. The original 98 design records, 128 pattern records and all original image files remain archived there; only the active choices are rendered into product data and purchase links. Classic cream is an explicit eighth choice, not an extra ninth option.

The product page shows all eight choices directly in a four-column thumbnail grid. The full-catalog expansion, search, category filters and two-stage recommendation questionnaire are removed. The comparison page displays the same small catalog. Home, paired page, studio updates, example media article and metadata use the eight-choice copy in English, Chinese, Japanese and Korean.

The paired collection contains only P-01. Its original two-camera image remains intact, with A/left and B/right selection. An old inactive style URL shows a current-selection notice and blocks checkout until the visitor explicitly chooses an available look. An unselected P-01 URL still requires A/B.

The 26 photography ideas and 12 diary photographs remain. Where an existing scene depicts an exterior outside the active collection, the caption identifies it as a reference exterior and links to the current collection. It does not silently map that picture to another purchasable style.

No-JavaScript product pages provide eight named, static checkout links; the generic main button remains Classic cream and is identified as such. Four-language navigation, side-specific share URLs, consent controls and tracking remain.

## Verification and publication record

The build and site checker enforce the eight-choice cap, agreement across visual/static checkout options, original archive preservation, no active purchase links to inactive designs, four-language translations and the unchanged USD offer. JavaScript syntax and diff checks are required. Browser checks cover 320, 390 and 1440px on home, product, styles, pair and comparison pages; all eight selections in each language; retired URLs; P side selection; language parameters and no-JavaScript purchases.

The earlier design gate remains `ERROR (consistency.mjs could not walk 1440, 390)`; this small catalog update does not claim a new full gate or formal performance pass. Copy lint has no FAILs; the labelled fictional review name remains as an intentional example. The owner requested visible AI/sample labels and compact layout, which continue to take priority over conflicting skill defaults.

Resource version: `20261110-eight-looks`. Production results, commit/deployment links and screenshots are appended to the vault maintenance note `keeper-day-website-refresh-20261109.md` and evidence directory `attachments/keeper-day/website-eight-looks-20261110/` after release.
