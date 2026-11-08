# VESSL 4비트 다운로드 모델 재실험

상품: **랑드샤 베스트 티 4종 세트** · 기간: **12월 한 달(연도 미정)**. 크리스마스·가을·송년·신년 각 hero 1구좌를 비교합니다. 가을은 감성 콘셉트, 신년은 12월의 새해 준비입니다. 가격·할인·사은품은 미정입니다.

실제 응답 12건 / 기본 규칙 통과 10건 / 경고 없는 기계 검사 10건. 이는 담당자의 문구 승인이나 의미적 출처 충실함을 보증하지 않습니다.

| 모델 | 주제 | 상태 | 기본 규칙 | 검토 사항 | 추론 시간(초) |
|---|---|---|---|---|---:|
| google/gemma-3-12b-it | 가을 | ok | 통과 | - | 2.587 |
| google/gemma-3-12b-it | 크리스마스 | ok | 통과 | - | 5.92 |
| google/gemma-3-12b-it | 신년 | ok | 통과 | - | 2.898 |
| google/gemma-3-12b-it | 연말(송년) | ok | 통과 | - | 2.701 |
| google/gemma-3n-E4B-it | 가을 | ok | 통과 | - | 3.274 |
| google/gemma-3n-E4B-it | 크리스마스 | ok | 통과 | - | 6.67 |
| google/gemma-3n-E4B-it | 신년 | ok | 통과 | - | 2.119 |
| google/gemma-3n-E4B-it | 연말(송년) | ok | 미통과/미실행 | conflicting_schedule_claim; unsupported_numeric_claim | 2.612 |
| Qwen/Qwen3-VL-4B-Instruct | 가을 | ok | 미통과/미실행 | unconfirmed_purchase_flow | 1.178 |
| Qwen/Qwen3-VL-4B-Instruct | 크리스마스 | ok | 통과 | - | 3.528 |
| Qwen/Qwen3-VL-4B-Instruct | 신년 | ok | 통과 | - | 1.078 |
| Qwen/Qwen3-VL-4B-Instruct | 연말(송년) | ok | 통과 | - | 1.099 |

## 주제별 제목 비교

| 주제 | google/gemma-3-12b-it | google/gemma-3n-E4B-it | Qwen/Qwen3-VL-4B-Instruct |
|---|---|---|---|
| 크리스마스 | 소중한 순간, 티로 축복하세요 | 크리스마스, 오설록과 함께하는 따뜻한 티타임 | 크리스마스 선물, 티타임으로 완성 |
| 가을 | 가을, 그 여운을 담다 | 12월, 오설록과 함께 떠나는 가을의 여운 | 가을의 마지막 숨결, 지금 만나보세요 |
| 연말(송년) | 따스한 마음을 담아 | 2023년, 감사한 순간을 선물하세요 | 연말의 감사, 한 잔으로 전해 |
| 신년 | 새해맞이, 마음을 전하세요 | 새해, 오설록과 함께 시작하세요 | 신년을 위한 최고의 선물 |

## google/gemma-3-12b-it / 가을

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: b92b218582c521ba287f38f1d6057dcd3c6cbff036f13cac97b5d861f5e58ec3

- 제목: 가을, 그 여운을 담다
- 설명: 랑드샤 베스트 티 4종 세트로 깊어지는 가을의 향긋함.
- 버튼: 따뜻한 티 한 잔
- 기간: 12월 한 달
- 모델의 참고 이유: 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 / Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요.
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인 배숙을 현대적인 감성으로 재해석한 레시피를 만들어봤어요. 삼다 꿀배숙 레시피 영상 재생 
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"autumn\", \"id\":\"hero\",\"layout\":\"hero\",\"title\":\"가을, 그 여운을 담다\",\"subtitle\":\"랑드샤 베스트 티 4종 세트로 깊어지는 가을의 향긋함.\",\"cta\":\"따뜻한 티 한 잔\",\"period\":\"12월 한 달\",\"reference_ids\":[\"osulloc-004#s02\",\"osulloc-003#s04\"],\"evidence\":\"11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 / Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요.\",\"details_needed\":[]}\n```"
```

## google/gemma-3-12b-it / 크리스마스

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: b92b218582c521ba287f38f1d6057dcd3c6cbff036f13cac97b5d861f5e58ec3

- 제목: 소중한 순간, 티로 축복하세요
- 설명: 랑드샤 베스트 티 4종 세트로 따뜻한 크리스마스 티타임을 선물하세요.
- 버튼: 지금 바로 만나보기
- 기간: 12월 한 달
- 모델의 참고 이유: '11.02 - 11.16 일 년만에 돌아온' 표현을 활용하여 특별함을 강조, 'Find my taste'에서 영감을 얻어 선물 대상의 취향을 고려하는 메시지 추가
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설록몰 이벤트 미식의 순간을 함께할 티 단품 최대 30% 다양한 미식의 세계를 만들 티 세트
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"christmas\", \"id\":\"hero\",\"layout\":\"hero\",\"title\":\"소중한 순간, 티로 축복하세요\",\"subtitle\":\"랑드샤 베스트 티 4종 세트로 따뜻한 크리스마스 티타임을 선물하세요.\",\"cta\":\"지금 바로 만나보기\",\"period\":\"12월 한 달\",\"reference_ids\":[\"osulloc-004#s02\", \"osulloc-003#s06\"],\"evidence\":\"'11.02 - 11.16 일 년만에 돌아온' 표현을 활용하여 특별함을 강조, 'Find my taste'에서 영감을 얻어 선물 대상의 취향을 고려하는 메시지 추가\",\"details_needed\":[]}\n```"
```

## google/gemma-3-12b-it / 신년

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: b92b218582c521ba287f38f1d6057dcd3c6cbff036f13cac97b5d861f5e58ec3

- 제목: 새해맞이, 마음을 전하세요
- 설명: 다가오는 새해, 소중한 분께 랑드샤 베스트 티 4종 세트로 따뜻한 새해를 선물하세요.
- 버튼: 새해 선물 준비
- 기간: 12월 한 달
- 모델의 참고 이유: 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이
2026년 11월 출석체크 조용히 다가온 연말의 페이지
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"new_year\", \"id\":\"hero\", \"layout\":\"hero\", \"title\":\"새해맞이, 마음을 전하세요\", \"subtitle\":\"다가오는 새해, 소중한 분께 랑드샤 베스트 티 4종 세트로 따뜻한 새해를 선물하세요.\", \"cta\":\"새해 선물 준비\", \"period\":\"12월 한 달\", \"reference_ids\":[\"osulloc-004#s02\", \"osulloc-002#s01\"], \"evidence\":\"11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이\\n2026년 11월 출석체크 조용히 다가온 연말의 페이지\", \"details_needed\":[]}\n```"
```

## google/gemma-3-12b-it / 연말(송년)

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: b92b218582c521ba287f38f1d6057dcd3c6cbff036f13cac97b5d861f5e58ec3

- 제목: 따스한 마음을 담아
- 설명: 소중한 분께 랑드샤 베스트 티 4종 세트로 감사를 전하세요.
- 버튼: 마음을 전하세요
- 기간: 12월 한 달
- 모델의 참고 이유: '11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이'의 이벤트성 강조, '2026년 11월 출석체크 조용히 다가온 연말의 페이지'의 따뜻한 분위기
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"year_end\", \"id\":\"hero\", \"layout\":\"hero\", \"title\":\"따스한 마음을 담아\", \"subtitle\":\"소중한 분께 랑드샤 베스트 티 4종 세트로 감사를 전하세요.\", \"cta\":\"마음을 전하세요\", \"period\":\"12월 한 달\", \"reference_ids\":[\"osulloc-004#s02\", \"osulloc-002#s01\"], \"evidence\":\"'11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이'의 이벤트성 강조, '2026년 11월 출석체크 조용히 다가온 연말의 페이지'의 따뜻한 분위기\", \"details_needed\":[]}\n```"
```

## google/gemma-3n-E4B-it / 가을

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 0a377808afeaafcbf5dcc2b1844594a1b60a50cd18e7e3e469cfd64e7bb7faa5

- 제목: 12월, 오설록과 함께 떠나는 가을의 여운
- 설명: 랑드샤 베스트 티 4종 세트로 깊어지는 풍미를 경험하세요.
- 버튼: 지금 만나보기
- 기간: 12월 한 달
- 모델의 참고 이유: 감성적인 문장 구조 및 가을의 여운을 떠올리게 하는 표현
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인 배숙을 현대적인 감성으로 재해석한 레시피를 만들어봤어요. 삼다 꿀배숙 레시피 영상 재생 
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\n  \"theme_id\": \"autumn\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"12월, 오설록과 함께 떠나는 가을의 여운\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트로 깊어지는 풍미를 경험하세요.\",\n  \"cta\": \"지금 만나보기\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-003#s04\"],\n  \"evidence\": \"감성적인 문장 구조 및 가을의 여운을 떠올리게 하는 표현\",\n  \"details_needed\": []\n}\n```"
```

## google/gemma-3n-E4B-it / 크리스마스

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 0a377808afeaafcbf5dcc2b1844594a1b60a50cd18e7e3e469cfd64e7bb7faa5

- 제목: 크리스마스, 오설록과 함께하는 따뜻한 티타임
- 설명: 랑드샤 베스트 티 4종 세트로 특별한 선물을 준비하세요.
- 버튼: 지금 바로 만나보기
- 기간: 12월 한 달
- 모델의 참고 이유: 따뜻한 분위기 연출, 선물 강조, 티의 다양성 어필
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설록몰 이벤트 미식의 순간을 함께할 티 단품 최대 30% 다양한 미식의 세계를 만들 티 세트
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\n  \"theme_id\": \"christmas\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"크리스마스, 오설록과 함께하는 따뜻한 티타임\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트로 특별한 선물을 준비하세요.\",\n  \"cta\": \"지금 바로 만나보기\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-003#s06\"],\n  \"evidence\": \"따뜻한 분위기 연출, 선물 강조, 티의 다양성 어필\",\n  \"details_needed\": []\n}\n```"
```

## google/gemma-3n-E4B-it / 신년

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 0a377808afeaafcbf5dcc2b1844594a1b60a50cd18e7e3e469cfd64e7bb7faa5

- 제목: 새해, 오설록과 함께 시작하세요
- 설명: 랑드샤 베스트 티 4종 세트로 특별한 선물을 준비하세요.
- 버튼: 선물 찾아보기
- 기간: 12월 한 달
- 모델의 참고 이유: 과거 레퍼런스 어조 및 표현 구조 참고
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"new_year\",\"id\":\"hero\",\"layout\":\"hero\",\"title\":\"새해, 오설록과 함께 시작하세요\",\"subtitle\":\"랑드샤 베스트 티 4종 세트로 특별한 선물을 준비하세요.\",\"cta\":\"선물 찾아보기\",\"period\":\"12월 한 달\",\"reference_ids\":[\"osulloc-002#s01\"],\"evidence\":\"과거 레퍼런스 어조 및 표현 구조 참고\",\"details_needed\":[]}\n```"
```

## google/gemma-3n-E4B-it / 연말(송년)

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 0a377808afeaafcbf5dcc2b1844594a1b60a50cd18e7e3e469cfd64e7bb7faa5

- 제목: 2023년, 감사한 순간을 선물하세요
- 설명: 오설록 랑드샤 베스트 티 4종 세트로 따뜻한 송년의 마음을 전하세요.
- 버튼: 선물하기
- 기간: 12월 한 달
- 모델의 참고 이유: 과거 레퍼런스 어조 및 표현 구조 참고
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"```json\n{\"theme_id\":\"year_end\", \"id\":\"hero\", \"layout\":\"hero\", \"title\":\"2023년, 감사한 순간을 선물하세요\", \"subtitle\":\"오설록 랑드샤 베스트 티 4종 세트로 따뜻한 송년의 마음을 전하세요.\", \"cta\":\"선물하기\", \"period\":\"12월 한 달\", \"reference_ids\":[\"osulloc-004#s02\", \"osulloc-002#s01\"], \"evidence\":\"과거 레퍼런스 어조 및 표현 구조 참고\", \"details_needed\":[]}\n```"
```

## Qwen/Qwen3-VL-4B-Instruct / 가을

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 84f7ed8042fa7cdbd902f7dcb7d0370e032095047cc3244179f263b77b5bc318

- 제목: 가을의 마지막 숨결, 지금 만나보세요
- 설명: 랑드샤 베스트 티 4종 세트, 12월 한 달의 따뜻한 기대감을 선사합니다
- 버튼: 지금 예약
- 기간: 12월 한 달
- 모델의 참고 이유: 감성적 시선과 한정 기간 표현, 레퍼런스의 흐름과 어조를 참고
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인 배숙을 현대적인 감성으로 재해석한 레시피를 만들어봤어요. 삼다 꿀배숙 레시피 영상 재생 
- 추가 확인: 추가 항목 미출력

```json
"{\n  \"theme_id\": \"autumn\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"가을의 마지막 숨결, 지금 만나보세요\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트, 12월 한 달의 따뜻한 기대감을 선사합니다\",\n  \"cta\": \"지금 예약\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-003#s04\"],\n  \"evidence\": \"감성적 시선과 한정 기간 표현, 레퍼런스의 흐름과 어조를 참고\",\n  \"details_needed\": []\n}"
```

## Qwen/Qwen3-VL-4B-Instruct / 크리스마스

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 84f7ed8042fa7cdbd902f7dcb7d0370e032095047cc3244179f263b77b5bc318

- 제목: 크리스마스 선물, 티타임으로 완성
- 설명: 랑드샤 베스트 티 4종 세트, 12월 한 달 특별 기획
- 버튼: 이제 바로 구매
- 기간: 12월 한 달
- 모델의 참고 이유: 선착순, 쿠폰, 혜택 기간 표현 활용
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설록몰 이벤트 미식의 순간을 함께할 티 단품 최대 30% 다양한 미식의 세계를 만들 티 세트
- 추가 확인: 추가 항목 미출력

```json
"{\n  \"theme_id\": \"christmas\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"크리스마스 선물, 티타임으로 완성\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트, 12월 한 달 특별 기획\",\n  \"cta\": \"이제 바로 구매\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-003#s06\"],\n  \"evidence\": \"선착순, 쿠폰, 혜택 기간 표현 활용\",\n  \"details_needed\": []\n}"
```

## Qwen/Qwen3-VL-4B-Instruct / 신년

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 84f7ed8042fa7cdbd902f7dcb7d0370e032095047cc3244179f263b77b5bc318

- 제목: 신년을 위한 최고의 선물
- 설명: 랑드샤 베스트 티 4종 세트, 12월 한 달 특별 기간
- 버튼: 이제 바로 확인
- 기간: 12월 한 달
- 모델의 참고 이유: 선착순, 쿠폰, 출석체크 형식의 참여 유도 문구
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"{\n  \"theme_id\": \"new_year\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"신년을 위한 최고의 선물\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트, 12월 한 달 특별 기간\",\n  \"cta\": \"이제 바로 확인\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-002#s01\"],\n  \"evidence\": \"선착순, 쿠폰, 출석체크 형식의 참여 유도 문구\",\n  \"details_needed\": []\n}"
```

## Qwen/Qwen3-VL-4B-Instruct / 연말(송년)

설정: Q4_K_M; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history · 모델 revision: 84f7ed8042fa7cdbd902f7dcb7d0370e032095047cc3244179f263b77b5bc318

- 제목: 연말의 감사, 한 잔으로 전해
- 설명: 랑드샤 베스트 티 4종 세트, 한 해를 마무리하는 송년 선물
- 버튼: 지금 선물하기
- 기간: 12월 한 달
- 모델의 참고 이유: 선착순 쿠폰 도전, 출석체크 형식의 연말 기념 문구
- 출처 [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처 [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 이번 달 출석현황 총 0 회
- 추가 확인: 추가 항목 미출력

```json
"{\n  \"theme_id\": \"year_end\",\n  \"id\": \"hero\",\n  \"layout\": \"hero\",\n  \"title\": \"연말의 감사, 한 잔으로 전해\",\n  \"subtitle\": \"랑드샤 베스트 티 4종 세트, 한 해를 마무리하는 송년 선물\",\n  \"cta\": \"지금 선물하기\",\n  \"period\": \"12월 한 달\",\n  \"reference_ids\": [\"osulloc-004#s02\", \"osulloc-002#s01\"],\n  \"evidence\": \"선착순 쿠폰 도전, 출석체크 형식의 연말 기념 문구\",\n  \"details_needed\": []\n}"
```

이전 CPU·공개 데모 결과는 별도 폴더에 보존합니다. 설정·양자화·장비·입력이 다른 결과를 같은 모델 순위로 취급하지 않습니다. 다운로드·모델 로드 시간은 문구 추론 시간에서 제외하며 결과 JSON에 별도로 남깁니다.
