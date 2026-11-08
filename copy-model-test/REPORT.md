# 오설록 시즌 카피 — 실제 로컬 모델 테스트

레퍼런스 195건과 tea_ad의 실제 title/subtitle/cta 계약을 읽어 입력을 구성했습니다. 이번 실행 범위는 4개 시즌 × 모델별 메인 비주얼 1구좌입니다.

실험 조건: **랑드샤 베스트 티 4종 세트 / 12월 한 달(12월 1일~31일, 연도 미정)**. 과거 행사의 가격·할인·사은품은 이번 행사 사실이 아닙니다. 가을·신년은 기간과 별개인 콘셉트 비교입니다. 이전 실험은 runs/baseline-category-only에 보존했습니다.

## 실행 상태

| 모델 | 시즌 | 상태 | 글자 수(title/subtitle/cta) | 구조·기본 규칙 | 추가 검토 | 경과(초) |
|---|---|---|---|---|---|---:|
| Qwen/Qwen2.5-0.5B-Instruct | 가을 | ok | 7/7/7 | 미통과/미실행 | missing_exact_product_name; weak_explicit_season_signal | 1.712 |
| Qwen/Qwen2.5-0.5B-Instruct | 크리스마스 | ok | 40/7/7 | 미통과/미실행 | title_too_long; unsupported_numeric_claim; unsupported_offer_or_effect_claim; product_name_in_title_instead_of_subtitle; weak_explicit_season_signal | 3.301 |
| Qwen/Qwen2.5-0.5B-Instruct | 신년 | ok | 7/7/7 | 미통과/미실행 | missing_exact_product_name; weak_explicit_season_signal | 1.343 |
| Qwen/Qwen2.5-0.5B-Instruct | 연말(송년) | ok | 13/26/7 | 미통과/미실행 | missing_exact_product_name | 1.498 |
| Qwen/Qwen2.5-1.5B-Instruct | 가을 | ok | 15/15/4 | 통과 | product_name_in_title_instead_of_subtitle; placeholder_reference_evidence | 3.645 |
| Qwen/Qwen2.5-1.5B-Instruct | 크리스마스 | ok | 15/19/2 | 통과 | product_name_in_title_instead_of_subtitle; placeholder_reference_evidence | 4.667 |
| Qwen/Qwen2.5-1.5B-Instruct | 신년 | ok | 15/13/4 | 미통과/미실행 | unsupported_offer_or_effect_claim; product_name_in_title_instead_of_subtitle; placeholder_reference_evidence; weak_explicit_season_signal | 3.776 |
| Qwen/Qwen2.5-1.5B-Instruct | 연말(송년) | ok | 15/21/4 | 통과 | product_name_in_title_instead_of_subtitle; placeholder_reference_evidence; weak_explicit_season_signal | 3.77 |

통과는 JSON 내용·글자 수·숫자/금지 표현·입력 출처 ID 같은 기계 검사 결과입니다. 카피의 매력·브랜드 적합성·근거의 의미적 충실함을 보증하지 않습니다. 상품명·기간 포함 여부도 확인합니다. strict_json 여부는 evaluation.json에서 별도로 기록합니다.
상품명이 제목에 있으면 사실 누락으로 처리하지 않고, 설명에 넣으라는 프롬프트 지침 위반을 별도 경고합니다. 현재 로컬 모델은 CPU 4스레드·Q4_K_M·고정 seed로 실행했습니다. 모델 크기와 프롬프트에 따른 비교이며 품질 순위나 다른 사내 컴퓨터 속도로 일반화하지 않습니다. 과거 공개 데모의 시간은 네트워크·큐를 포함하므로 로컬 시간과 직접 비교하지 않습니다.

## Qwen/Qwen2.5-0.5B-Instruct / 가을

- 제목: 12월 한 달
- 설명: 12월 한 달
- 버튼: 12월 한 달
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인
- 확인할 사실: 추가 항목 미출력
- 검토 표시: weak_explicit_season_signal

## Qwen/Qwen2.5-0.5B-Instruct / 크리스마스

- 제목: 12월 한 달 기간 '랑드샤 베스트 티 4종 세트'로 선착순 30% 혜택
- 설명: 12월 한 달
- 버튼: 12월 한 달
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설
- 확인할 사실: 12월 한 달, 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요, 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요, 11.02 - 11.16 일 년만에 돌아온
- 검토 표시: product_name_in_title_instead_of_subtitle; weak_explicit_season_signal

## Qwen/Qwen2.5-0.5B-Instruct / 신년

- 제목: 12월 한 달
- 설명: 12월 한 달
- 버튼: 12월 한 달
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 12월 한 달
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 추가 항목 미출력
- 검토 표시: weak_explicit_season_signal

## Qwen/Qwen2.5-0.5B-Instruct / 연말(송년)

- 제목: 12월 한 달 연말 선물
- 설명: 12월 한 달 기간 '12월 한 달'의 레퍼런스
- 버튼: 12월 한 달
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 12월 한 달
- 출처:
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
- 확인할 사실: 추가 항목 미출력

## Qwen/Qwen2.5-1.5B-Instruct / 가을

- 제목: 랑드샤 베스트 티 4종 세트
- 설명: 가을의 여운을 풍기는 차세트
- 버튼: 구매하기
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 참고한 ID와 표현 구조
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인
- 확인할 사실: 추가 항목 미출력
- 검토 표시: product_name_in_title_instead_of_subtitle; placeholder_reference_evidence

## Qwen/Qwen2.5-1.5B-Instruct / 크리스마스

- 제목: 랑드샤 베스트 티 4종 세트
- 설명: 크리스마스 선물로 티 타임 즐기세요
- 버튼: 구매
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 참고한 표현 구조
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설
- 확인할 사실: 추가 항목 미출력
- 검토 표시: product_name_in_title_instead_of_subtitle; placeholder_reference_evidence

## Qwen/Qwen2.5-1.5B-Instruct / 신년

- 제목: 랑드샤 베스트 티 4종 세트
- 설명: 12월 한 달 특가 할인
- 버튼: 구매하기
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 참고한 표현 구조
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 추가 항목 미출력
- 검토 표시: product_name_in_title_instead_of_subtitle; placeholder_reference_evidence; weak_explicit_season_signal

## Qwen/Qwen2.5-1.5B-Instruct / 연말(송년)

- 제목: 랑드샤 베스트 티 4종 세트
- 설명: 12월 한 달 동안 즐거운 추억 만들기
- 버튼: 구매하기
- 기간: 12월 한 달
- 모델이 밝힌 참고 이유: 참고한 표현 구조
- 출처:
  - [osulloc-004#s02](https://www.osulloc.com/kr/ko): 11.02 - 11.16 일 년만에 돌아온, 오설록 블랙 프라이데이 매일 10시, 20시 선착순 50% 쿠폰에 도전하세요 자세히 보기
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 추가 항목 미출력
- 검토 표시: product_name_in_title_instead_of_subtitle; placeholder_reference_evidence; weak_explicit_season_signal

## 공개 데모 재실행과 입력 개선

12월 조건으로 기존 Gemma 3n E4B·Gemma 3 12B·Qwen3-VL 4B를 재실행했으나 인증 후에도 무료 GPU 할당량이 없어 새 응답을 얻지 못했습니다. Qwen3 공식 데모 4B·8B·14B도 서버 오류였습니다. runs/december-public-attempt에 원문 실패를 보존했습니다.
따라서 Qwen2.5 0.5B·1.5B의 공식 Q4_K_M 모델을 내려받아 CPU에서 실행했습니다. 긴 다중 시즌 지침의 첫 8개 응답은 runs/december-local-long-prompt에, 한 주제·오설록 출처 2개로 줄인 재실험 8개 응답은 현재 results에 보존합니다. 기존 대형 모델과 같은 조건의 재비교가 완료됐다는 뜻은 아닙니다.
Gemma 2 2B·Llama 3.2 3B·Gemma 4 E4B 어댑터도 추가했지만 무료 GPU 한도 소진 후에는 실행하지 않았습니다. 어댑터 추가와 응답 확보를 구분합니다.

## 실행 중 확인된 제약

최초 Hugging Face Inference Providers 비교는 크레딧 부족으로 실패했습니다. 그 경로의 Qwen3.5 9B·Gemma 3 4B·Llama 3.1 8B 결과를 생성한 것처럼 취급하지 않습니다. 무료 Space는 다른 모델이며 정확한 모델/Space를 각 결과 파일에 기록했습니다.
크리스마스·신년의 직접 레퍼런스가 적어 관련 차·선물·일상 표현을 참고했습니다. 이미지 OCR은 하지 않았습니다. 가상 실험 상품은 랑드샤 베스트 티 4종 세트, 기간은 12월 한 달입니다. 가격·할인·사은품은 미정입니다. 가을은 감성 콘셉트, 신년은 새해맞이 준비입니다.
모델이 출처 ID를 출력했다는 사실만으로 올바르게 참고했다고 판정하지 않습니다. 레퍼런스 의미를 잘못 설명한 경우는 별도 검토 표시를 남겼습니다.
