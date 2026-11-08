# Amore_ad

Amorepacific Industry-Academia Cooperation Project

## 프로모션 레퍼런스 자료

쇼핑몰의 공개 프로모션 페이지를 수집한 자료입니다. 페이지별 HTML 본문과
JSON 메타데이터를 분리해 저장하며, JSON에서 섹션·이미지·링크 관계를 확인할 수 있습니다.

현재 **11개 몰, 194개 페이지 레코드**가 있습니다. 기존 175건에 2026-11-08
요청 URL 19건을 추가했습니다. 새 자료는 본문 수집 16건, 앱 안내 1건,
본문 미확보 2건이며, 본문을 확보한 구간과 앱 안내 조각을 **264개 섹션**으로 나눴습니다.
기존 자료까지 합친 전체 섹션 수는 975개입니다.

## 자료가 저장된 위치

```text
reference/
├── README.md                           # 수집 범위·예외·필드 설명·실행 방법
├── data/
│   ├── index.jsonl                      # 전체 페이지 목록: 한 줄에 페이지 한 건
│   ├── brands.json                      # 몰별 수집 정보와 건수·방법
│   └── pages/
│       ├── kolonmall-001.json           # 페이지 정보, 섹션, 이미지, 링크 관계
│       ├── kolonmall-001.html           # 해당 페이지의 보관된 본문 DOM
│       └── ...
├── promotion_urls_20261108.json          # 추가 수집 대상으로 전달된 19개 URL
├── section_review_20261108.md            # 추가 자료의 섹션별 검토표
├── build_reference_index.py             # 전체 몰별 덤프 → 새 인덱스 생성
├── import_promotion_snapshots.py         # 브라우저 스냅샷 → 새 페이지 레코드 추가
├── section_inference.py                 # HTML 구획·제목·문맥으로 섹션 추론
└── validate_promotion_references.py      # 추가 19건의 구조·연결 검증
```

페이지 ID는 `<몰 식별자>-<3자리 번호>` 형식입니다. 예를 들어 `kolonmall-001`은
`pages/kolonmall-001.json`에 상세 정보가 있고, `html_file`로 대응하는 HTML을 가리킵니다.
`meta_file`, `html_file` 경로는 `reference/data/`를 기준으로 해석합니다.
본문 미확보 레코드는 `html_file`이 `null`이며 HTML 파일이 없습니다.

### 자료 읽는 순서

1. `reference/data/index.jsonl`에서 `brand`, `title`, `status`, `url`로 페이지를 찾습니다.
2. 해당 줄의 `meta_file`이 가리키는 JSON을 엽니다.
3. `sections`에서 쿠폰·상품 목록·참여 이벤트·유의사항 등의 구간을 확인합니다.
4. 섹션의 `image_ids`로 `image_assets`를, `relationship_indexes`로 `relationships`를 조회합니다.
5. 보관 당시 HTML 구조를 확인하려면 `html_file`을 읽습니다.

| 페이지 JSON 필드 | 저장된 내용 |
| --- | --- |
| `id`, `brand`, `collected_date` | 페이지 ID, 몰 식별자, 수집일 |
| `url`, `resolved_url` | 전달받은 URL과 실제로 도착한 URL |
| `title`, `listing_label`, `description`, `text` | 페이지 제목, 목록 라벨, 설명, 본문 텍스트 |
| `status`, `capture_note` | 수집 상태와 예외 설명. `capture_note`는 필요한 경우에만 존재 |
| `sections` | 구간별 역할·텍스트·DOM 경로·이미지 ID·링크 관계 인덱스 |
| `images` | HTML에 노출된 이미지 출현 정보 |
| `image_assets` | URL별 이미지 자산, 분류 근거, 속한 섹션, 대체 URL |
| `relationships` | 링크·버튼 등의 라벨, 목적지, 유형, 검증 상태 |
| `html_file` | 보관된 본문 HTML 경로. 본문이 없으면 `null` |

섹션의 `image_ids: ["i0141"]`은 같은 JSON의 `image_assets`에서
`id == "i0141"`인 항목을 뜻합니다. `relationship_indexes: [117, 118]`은
같은 JSON의 `relationships[117]`, `relationships[118]`을 뜻하며 **0부터 시작**합니다.
`image_assets[].section_ids`에는 이미지가 속한 섹션 ID가 역으로 저장됩니다.

### 수집 상태와 해석 범위

- `captured`: 프로모션 본문을 확보했습니다.
- `app_handoff`: 앱 이동 안내 등이 확인된 상태입니다. HTML이 있어도 전체 앱 화면을 수집했다는 뜻은 아닙니다.
- `body_unavailable`: 본문 미제공 또는 다른 목록으로 이동하여 해당 프로모션 본문을 확보하지 못했습니다.

이미지는 **원본 파일을 내려받아 저장한 것이 아니라 URL과 메타데이터**로 저장되어 있습니다.
외부 이미지가 삭제되면 표시되지 않을 수 있습니다. HTML은 수집 당시 DOM 자료이며,
사이트 전체를 오프라인으로 재현하는 파일은 아닙니다.

섹션 역할과 이미지 태그는 HTML·제목·문맥을 근거로 추론했습니다. 이미지 속 글자 OCR은
수행하지 않았습니다. 추가 19건은 노출된 초기 DOM을 기준으로 하며, 별도 탭·페이지네이션·
상품 상세 본문은 수집하지 않았습니다. `declared_in_html`은 마크업에 목적지가 있다는 뜻이고,
`unverified`는 목적지를 확정하지 못했다는 뜻입니다. 새 자료에는 실제 클릭 검증을 뜻하는
`click_verified`를 부여하지 않았습니다.

상세 필드와 예외는 [reference/README.md](reference/README.md), 구간별 결과는
[섹션 검토표](reference/section_review_20261108.md)를 참고하세요.
