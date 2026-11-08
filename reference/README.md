# reference parser

Converts per-brand promotion dumps (`<brand>_promotions.json`, each with a `pages` array) into one flat, brand-tagged reference index.

```bash
python3 reference/build_reference_index.py <dir with *_promotions.json> <output dir>
```

Output:

- `index.jsonl` - one line per page (id, brand, url, title, status, file paths, sizes)
- `brands.json` - per-brand collection metadata
- `pages/<brand>-NNN.json` - page record without html
- `pages/<brand>-NNN.html` - rendered promotion body DOM

Generated index lives in `reference/data/` (175 pages: kurly 78, 29cm 94, osulloc 3).

## Additional promotions collected on 2026-11-08

The index now contains **194 records**: the original 175 records are unchanged,
plus the 19 explicitly supplied URLs in `promotion_urls_20261108.json`.

| Brand | Added | captured | app_handoff | body_unavailable |
| --- | ---: | ---: | ---: | ---: |
| kolonmall | 2 | 1 | 0 | 1 |
| kakao_gift | 2 | 2 | 0 | 0 |
| shinsegaev | 5 | 4 | 0 | 1 |
| zigzag | 2 | 2 | 0 | 0 |
| hankkitongsal | 2 | 2 | 0 | 0 |
| dongwonmall | 2 | 2 | 0 | 0 |
| cjthemarket | 1 | 0 | 1 | 0 |
| wconcept | 3 | 3 | 0 | 0 |

Exceptions observed in the public browser:

- `kolonmall-002` (`Special/259545`): no promotion body; dialog says the mall
  homepage will be opened. Revisited with the same result.
- `shinsegaev-004` (`disp_ctg_no=2610264136`): redirects to the general event
  listing. The listing is not archived as this promotion's body.
- `cjthemarket-001`: desktop page provides coupon/payment images and QR/app
  instructions. The available fragment is archived, with `app_handoff` status;
  the full app event was not collected. A narrow viewport still showed this state.

Capture scope: public browser-rendered promotion roots in their initial loaded
state. Scripts, tracking iframes, SVG icons, hidden form values and inline event
handlers are removed. Product bodies, additional pagination/tab states, image
OCR and live click verification are outside this capture. Image assets come from
loaded/lazy image attributes, srcset and inline CSS URLs; external CSS images
and lazy images without an exposed URL can be absent. Sections are inferred from
authored DOM modules, headings and local context, including nested wrappers.
DOM order is not a visual layout claim.
Unresolved controls remain `unverified`; relative link and image URLs resolve
against the observed final page URL. `url` preserves the exact supplied URL,
including query parameters and fragments; `resolved_url` records redirects.

The importer adds records with the existing page/index field conventions and
refuses to overwrite existing page IDs. It accepts local browser snapshot JSON
(`url`, `title`, `html`, optional `text`, `description`, `og_image`), keyed as
`<brand>-NNN.json`; raw full-page snapshots containing tracking code are kept
outside the repository. Install `beautifulsoup4` to run:

```bash
python3 reference/import_promotion_snapshots.py <snapshot-dir> \
  reference/promotion_urls_20261108.json reference/data
```

The original `build_reference_index.py` creates a fresh index from complete
per-brand dumps. Do not run it against only the new brands over the checked-in
index, because it replaces `brands.json` and `index.jsonl`.


## Section enrichment correction

The 2026-11-08 additions have been reprocessed into **264 sections** across the
16 captured pages and the one app-handoff fragment. The two unavailable pages
have no invented sections. The original 175 records and their HTML remain
unchanged.

`section_inference.py` identifies authored section modules per mall, traverses
nested layout wrappers and retains interstitial headings, navigation, notices,
and other content as separate sections. Each section includes the original
field conventions: `id`, `order`, `role`, `role_evidence`, `headings`, `text`,
`dom_path`, `dom_id`, `image_ids`, and `relationship_indexes`. Existing role,
image-tag and destination-type vocabulary is used. Images link back through
`image_assets[].section_ids`; srcset variants are listed as alternate URLs when
exposed. Role and image classification are evidence-based inferences, not OCR.
A section with insufficient evidence keeps the `content` role or `unknown`
image tag.

The source repository contains the original index converter and data, but not
the original browser collector or section-inference implementation. This update
reproduces its recorded HTML/headings/local-context method and output conventions
using the archived public browser DOM; it does not claim to run an unavailable
original collector. No new live-click verification is implied. Hidden dialog
markup and mobile/desktop variants can be present in the archived DOM; their
text is not proof that a benefit was issued or that a user performed an action.

Regeneration was staged in a separate directory with the original index and
brand metadata, validated, then only the 19 added records and aggregate metadata
were replaced. The importer continues to refuse overwriting an existing page ID.
To check the resulting section coverage and relationships:

```bash
python3 reference/validate_promotion_references.py
```

The validator checks DOM path resolution, non-overlapping section subtrees,
complete text coverage, reciprocal section/image mappings, relationship indexes,
index byte counts and aggregate metadata. It fails if any available added page
falls back to one whole-body section. See `section_review_20261108.md` for the
per-page counts and a readable section inventory.
