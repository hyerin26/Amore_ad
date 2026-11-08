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

Generated index lives in `reference/data/` (195 records across 11 malls; originally 175 pages: kurly 78, 29cm 94, osulloc 3).

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


## 저장 필드와 연결 규칙

전체 자료 구조는 [루트 README](../README.md)에 있습니다.

### `index.jsonl` — 전체 검색용 목록

파일 전체가 하나의 JSON 배열인 형식이 아닙니다. 각 줄을 별도로 JSON 파싱합니다.
각 줄에는 `id`, `brand`, `url`, `resolved_url`, `host`, `path_hint`, `title`,
`page_title`, `status`, `collected_date`, `meta_file`, `html_file`, `html_bytes`,
`n_sections`, `n_images`가 있습니다. `n_images`는 이미지 출현 횟수가 아니라
`image_assets`의 자산 수입니다. `html_bytes`는 UTF-8 HTML 파일의 바이트 수입니다.

### `brands.json` — 몰별 집계

최상위 키가 몰 식별자입니다. 수집 날짜·시간대·대상 URL·수집 범위·상태별 건수,
링크 수집 방법, 섹션 추론 방법, 이미지 분류 방법과 건수가 저장됩니다.
기존 몰과 추가 몰은 선택적 부가 필드가 다를 수 있습니다.

### `pages/<id>.json` — 페이지 상세

| 배열/필드 | 주요 하위 필드 | 해석 |
| --- | --- | --- |
| `sections[]` | `id`, `order`, `role`, `role_evidence` | 페이지 안에서의 섹션 ID, 순서, 역할, 추론 근거 |
| `sections[]` | `headings`, `text` | DOM 제목 요소와 해당 구간의 텍스트 |
| `sections[]` | `dom_path`, `dom_id` | 보관된 HTML 조각에서의 위치와 HTML id 속성 |
| `sections[]` | `image_ids`, `relationship_indexes` | 같은 페이지의 이미지 ID와 링크 배열 인덱스 |
| `image_assets[]` | `id`, `url`, `alt`, `tags`, `tag_evidence` | 이미지 식별자, URL, 대체 텍스트, 분류와 근거 |
| `image_assets[]` | `section_ids`, `alternate_urls` | 속한 섹션들, 노출된 대체 이미지 URL |
| `images[]` | `alt`, `url`, `tags`, `image_id` | 이미지 출현별 정보와 자산 참조. 동일 자산이 반복될 수 있음 |
| `relationships[]` | `source_url`, `label`, `element` | 출발 페이지, 링크/버튼 문구, 요소 종류 |
| `relationships[]` | `destination_url`, `destination_type` | 목적지 URL과 종류. 목적지를 모르면 URL은 `null` |
| `relationships[]` | `status`, `raw_target` | 검증 상태와 마크업에 선언된 원래 대상. `raw_target`은 선택 필드 |
| `source_revisit` | `resolved_url`, `status`, `title` | 원본 페이지 확인 시 관찰된 URL, 상태, 제목 |

참조는 **한 페이지 JSON 내부**에서 해석합니다. 서로 다른 페이지의 `s01` 또는
`i0001`은 다른 개체입니다. `relationships`는 배열 위치를 사용하므로 재정렬하면
`relationship_indexes`도 함께 갱신해야 합니다. 이미지 URL이 여러 구간에 등장하면
해당 자산의 `section_ids`에 여러 섹션이 기록됩니다.

`dom_path`는 요소만 세는 1부터 시작하는 경로입니다. 추가 자료의 `[1]`은 보관된
HTML의 최상위 요소이고, `[1, 2]`는 그 요소의 두 번째 자식 요소입니다. 텍스트 노드와
주석은 자식 번호에 포함하지 않습니다. 섹션의 `order`도 1부터 시작하지만,
`relationship_indexes`는 0부터 시작합니다.

대표 섹션 역할은 `hero`, `section_navigation`, `coupon_offer`, `benefit_overview`,
`sale_offer`, `product_list`, `participation_event`, `terms`, `related_promotions`,
`brand_story`, `content`입니다. 대표 이미지 태그는 `promotion_banner`,
`event_information`, `product_photo`, `editorial_image`, `ui_asset`, `unknown`입니다.
이미지 픽셀을 직접 해석한 분류가 아니므로 `role_evidence`와 `tag_evidence`를 함께 봅니다.

이미지 실물·스크린샷은 이 저장소에 저장하지 않습니다. HTML 안의 이미지 src는 상대
경로일 수 있으며, JSON의 이미지 URL은 관찰된 페이지 URL을 기준으로 절대 경로화합니다.
본문 미확보 레코드는 JSON만 존재하고 `html_file`은 `null`입니다.

### Python으로 연결 읽기

저장소 최상위 폴더에서 실행하는 예시입니다.

```python
import json
from pathlib import Path

base = Path("reference/data")
rows = [json.loads(line) for line in (base / "index.jsonl").read_text(encoding="utf-8").splitlines()]
row = next(row for row in rows if row["id"] == "kolonmall-001")
page = json.loads((base / row["meta_file"]).read_text(encoding="utf-8"))
assets = {asset["id"]: asset for asset in page["image_assets"]}

coupon = next(section for section in page["sections"] if section["role"] == "coupon_offer")
coupon_images = [assets[image_id] for image_id in coupon["image_ids"]]
coupon_links = [page["relationships"][index] for index in coupon["relationship_indexes"]]
print(coupon["id"], coupon["text"])
print([image["url"] for image in coupon_images])
print([link["destination_url"] for link in coupon_links])
```

## 오설록 메인 및 이벤트 재확인 — 2026-11-08

`osulloc-004`는 https://www.osulloc.com/kr/ko 메인 프로모션을 13개 섹션으로
분리한 추가 레코드입니다. 전체는 195페이지·988섹션입니다. 기존 194개 레코드는 보존했습니다.
진행 중 이벤트 목록은 기존 상세 3건(12413, 12426, 12412)만 노출했습니다.
`data/revisits/20261108/manifest.json`과 HTML 4개에 최신 상세·목록 확인 근거를 보관합니다.
같은 URL을 새 프로모션으로 중복 등록하지 않습니다. 최신 관찰 가격은 과거 자료이며
문구 실험의 12월 행사 가격이나 할인으로 사용하지 않습니다.

```bash
python3 reference/validate_osulloc_refresh.py
```

브라우저에서 수집한 main.json, listing.json, 12413.json, 12426.json, 12412.json을
입력으로 삼는 재현 코드는 `import_osulloc_refresh.py`입니다. 이미 등록된 ID는 덮어쓰지 않습니다.
초기 DOM·alt·HTML 구조를 사용하며 이미지 OCR이나 참여/쿠폰 발급은 하지 않습니다.
