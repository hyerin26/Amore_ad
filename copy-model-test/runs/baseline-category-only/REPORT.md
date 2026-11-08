# 오설록 시즌 카피 — 실제 공개 모델 테스트

레퍼런스 194건과 tea_ad의 실제 title/subtitle/cta 계약을 읽어 입력을 구성했습니다. 이번 실행 범위는 4개 시즌 × 모델별 메인 비주얼 1구좌입니다.

## 실행 상태

| 모델 | 시즌 | 상태 | 글자 수(title/subtitle/cta) | 구조·기본 규칙 | 추가 검토 | 경과(초) |
|---|---|---|---|---|---|---:|
| google/gemma-3-12b-it | 가을 | ok | 11/31/8 | 통과 | - | 12.338 |
| google/gemma-3-12b-it | 크리스마스 | ok | 14/33/8 | 통과 | weak_explicit_season_signal | 21.168 |
| google/gemma-3-12b-it | 신년 | ok | 11/26/7 | 통과 | weak_explicit_season_signal | 10.29 |
| google/gemma-3-12b-it | 연말(송년) | ok | 12/32/6 | 통과 | weak_explicit_season_signal | 8.425 |
| google/gemma-3n-E4B-it | 가을 | ok | 13/26/11 | 통과 | - | 15.004 |
| google/gemma-3n-E4B-it | 크리스마스 | ok | 20/21/7 | 통과 | reference_season_misattribution: cited snippets do not document Christmas; weak_explicit_season_signal | 16.201 |
| google/gemma-3n-E4B-it | 신년 | ok | 15/17/12 | 미통과/미실행 | wrong_theme_id; weak_explicit_season_signal | 13.317 |
| google/gemma-3n-E4B-it | 연말(송년) | ok | 17/20/7 | 통과 | weak_explicit_season_signal | 13.126 |
| Qwen/Qwen3.8-27B | 크리스마스 | error | -/-/- | 미통과/미실행 | - | 0.907 |
| Qwen/Qwen3-VL-4B-Instruct | 가을 | ok | 13/25/4 | 통과 | - | 6.607 |
| Qwen/Qwen3-VL-4B-Instruct | 크리스마스 | ok | 14/27/7 | 통과 | weak_explicit_season_signal | 9.758 |
| Qwen/Qwen3-VL-4B-Instruct | 신년 | error | -/-/- | 미통과/미실행 | - | 1.708 |
| Qwen/Qwen3-VL-4B-Instruct | 연말(송년) | ok | 13/36/5 | 통과 | - | 9.406 |

통과는 JSON 내용·글자 수·숫자/금지 표현·입력 출처 ID 같은 기계 검사 결과입니다. 카피의 매력·브랜드 적합성·근거의 의미적 충실함을 보증하지 않습니다. strict_json 여부는 evaluation.json에서 별도로 기록합니다.
공개 데모끼리 생성 설정이 달라 엄밀한 모델 순위로 해석하지 않습니다. 경과 시간에는 네트워크와 무료 GPU 대기가 포함됩니다.

## google/gemma-3-12b-it / 가을

- 제목: 가을날의 편안한 여유
- 설명: 따스한 차 한 잔으로 깊어가는 가을, 마음을 채워보세요.
- 버튼: 선물 보러 가기
- 모델이 밝힌 참고 이유: 오설록의 과거 자료에서 차를 미식 경험으로 연결하고, 따뜻하고 편안한 분위기를 조성하는 표현을 참고했습니다.
- 출처:
  - [osulloc-003#s01](https://www.osulloc.com/kr/ko/life/event/view/12412): 차, 미식의 발견 | Beyond Tea, Into Gourmet 차는 미식을 완성하고, 때로는 미식 그 자체가 됩니다. 손종원 셰프가 오설록 대표 블렌디드 티로 제안하는 새로운 미식의 경험
  - [osulloc-003#s04](https://www.osulloc.com/kr/ko/life/event/view/12412): Chef Son's tea recipes 한 잔으로 즐기던 차를, 오늘은 한 접시의 맛으로 만나보세요. Honey Pear Baesuk | 삼다 꿀배숙 오설록 삼다 꿀배 티와 함께 한국 전통 후식인
- 확인할 사실: 선물 카테고리 내 대표적인 차 종류는 무엇인가?, 가을 시즌을 대표하는 차의 특징은 무엇인가?

## google/gemma-3-12b-it / 크리스마스

- 제목: 따스한 겨울, 향긋한 선물
- 설명: 소중한 순간을 더욱 특별하게, 오설록 티로 마음을 전하세요.
- 버튼: 선물 보러 가기
- 모델이 밝힌 참고 이유: osulloc-003#s06에서 '미식의 순간을 함께할 티'라는 표현과 선물에 대한 언급을 참고하여 따뜻하고 선물에 집중된 문구를 구성했습니다.
- 출처:
  - [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설
- 확인할 사실: 시즌 차 종류 정보
- 검토 표시: weak_explicit_season_signal

## google/gemma-3-12b-it / 신년

- 제목: 따스한 겨울, 오설록
- 설명: 싱그러운 녹차 향으로 일상에 포근함을 더하세요.
- 버튼: 선물 찾아보기
- 모델이 밝힌 참고 이유: osulloc-002의 '조용히 다가온 연말'이라는 문구를 참고하여 차분하고 따뜻한 분위기를 표현하고자 했습니다.
- 출처:
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 시즌 차 종류 정보
- 검토 표시: weak_explicit_season_signal

## google/gemma-3-12b-it / 연말(송년)

- 제목: 따스한 겨울 티 한 잔
- 설명: 마음까지 녹이는 오설록의 선물, 특별한 겨울을 준비하세요.
- 버튼: 차 쇼핑하기
- 모델이 밝힌 참고 이유: osulloc-002의 '조용히 다가온 연말' 문구를 참고하여 차분하고 따뜻한 분위기를 표현했습니다.
- 출처:
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 선물 카테고리의 구체적인 상품 종류
- 검토 표시: weak_explicit_season_signal

## google/gemma-3n-E4B-it / 가을

- 제목: 가을, 차 한 잔의 여유
- 설명: 따스한 햇살 아래, 깊어지는 풍미를 느껴보세요.
- 버튼: 가을 차를 만나보세요
- 모델이 밝힌 참고 이유: 과거 자료에서 차를 통해 미식의 경험을 제안하는 분위기와 가을 시즌을 연결하여 차분하고 따뜻한 느낌을 표현했습니다.
- 출처:
  - [osulloc-003#s01](https://www.osulloc.com/kr/ko/life/event/view/12412): 차, 미식의 발견 | Beyond Tea, Into Gourmet 차는 미식을 완성하고, 때로는 미식 그 자체가 됩니다. 손종원 셰프가 오설록 대표 블렌디드 티로 제안하는 새로운 미식의 경험
- 확인할 사실: 확인할 사실

## google/gemma-3n-E4B-it / 크리스마스

- 제목: 따스한 겨울, 오설록으로 전하는 마음
- 설명: 소중한 사람에게, 정성 가득한 차 선물
- 버튼: 선물 찾아보기
- 모델이 밝힌 참고 이유: 과거 크리스마스 시즌 프로모션에서 따뜻한 분위기와 선물에 대한 강조, 그리고 차 선물 카테고리를 활용한 문구 스타일을 참고했습니다.
- 출처:
  - [osulloc-001#s01](https://www.osulloc.com/kr/ko/life/event/view/12413): 블랙프라이데이 마감 블랙프라이데이 마감까지 남은 시간 12 DAYS : 00 HRS : 44 MINS : 41 SECS BLACK FRIDAY UP TO 50%
  - [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설
- 확인할 사실: 상품명·가격·할인·사은품·기간
- 검토 표시: reference_season_misattribution: cited snippets do not document Christmas; weak_explicit_season_signal

## google/gemma-3n-E4B-it / 신년

- 제목: 따스한 겨울, 오설록과 함께
- 설명: 소중한 분께 전하는 마음을 담아
- 버튼: 선물로 마음을 전하세요
- 모델이 밝힌 참고 이유: 과거 프로모션에서 시즌의 분위기를 따뜻하고 차분하게 표현하고, 선물에 대한 언급을 통해 차/티 선물 카테고리를 강조한 점을 참고했습니다.
- 출처:
  - [osulloc-001#s01](https://www.osulloc.com/kr/ko/life/event/view/12413): 블랙프라이데이 마감 블랙프라이데이 마감까지 남은 시간 12 DAYS : 00 HRS : 44 MINS : 41 SECS BLACK FRIDAY UP TO 50%
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 시즌(겨울)에 맞는 비주얼 방향, 타겟 고객층
- 검토 표시: weak_explicit_season_signal

## google/gemma-3n-E4B-it / 연말(송년)

- 제목: 따스한 겨울, 함께 나누는 마음
- 설명: 소중한 사람에게 전하는 오설록의 선물
- 버튼: 선물 찾아보기
- 모델이 밝힌 참고 이유: 과거 연말 프로모션에서 따뜻한 분위기와 선물에 대한 강조가 나타나며, 출석체크 이벤트는 연말의 일상을 되돌아보는 느낌을 준다.
- 출처:
  - [osulloc-001#s01](https://www.osulloc.com/kr/ko/life/event/view/12413): 블랙프라이데이 마감 블랙프라이데이 마감까지 남은 시간 12 DAYS : 00 HRS : 44 MINS : 41 SECS BLACK FRIDAY UP TO 50%
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 상품 종류, 가격대, 선물 포장 옵션
- 검토 표시: weak_explicit_season_signal

## Qwen/Qwen3.8-27B / 크리스마스

실행 오류 또는 JSON 해석 실패: HTTP Error 400: Bad Request

## Qwen/Qwen3-VL-4B-Instruct / 가을

- 제목: 가을의 향기, 한 잔으로
- 설명: 차와 티가 담아낸 계절의 따뜻함을 선물하세요.
- 버튼: 선물하기
- 모델이 밝힌 참고 이유: osulloc-003#s01의 '차, 미식의 발견' 문체를 따뜻하고 시즌별 감성으로 재해석, 29cm-041#s06의 제품 소개 형식을 참고해 시즌적 차별화 문구 구성
- 출처:
  - [osulloc-003#s01](https://www.osulloc.com/kr/ko/life/event/view/12412): 차, 미식의 발견 | Beyond Tea, Into Gourmet 차는 미식을 완성하고, 때로는 미식 그 자체가 됩니다. 손종원 셰프가 오설록 대표 블렌디드 티로 제안하는 새로운 미식의 경험
  - [29cm-041#s06](https://www.29cm.co.kr/content/showcase/7295): SHOWCASE RECOMMEND ITEM fluffy haze cardigan 알파카와 울을 섬세하게 블렌딩한 원사에 정교한 후가공을 더해 완성한 컬리 텍스처. 미니멀한 실루엣 속 자개 히든 버튼
- 확인할 사실: 상품명, 가격, 할인, 사은품, 기간

## Qwen/Qwen3-VL-4B-Instruct / 크리스마스

- 제목: 겨울에 딱 좋은 차 한 잔
- 설명: 선물로 전하는 따뜻한 향기, 함께하는 시간의 시작
- 버튼: 선물 선택하기
- 모델이 밝힌 참고 이유: osulloc-003#s06에서 '차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요'의 감성과 29cm-057#s05에서 '따뜻한 선물을 전해보세요'의 따뜻한 분위기를 참고해 시즌 차이와 선물의 감정을 강조했음
- 출처:
  - [osulloc-003#s06](https://www.osulloc.com/kr/ko/life/event/view/12412): Find my taste 차의 맛을 따라, 나와 선물할 사람의 취향을 골라보세요 혜택 1.티 단품&티 세트 최대 30% 혜택 손종원 셰프 협업 기념 10월 15일부터 11월 15일까지 진행하는 오설
  - [29cm-057#s05](https://www.29cm.co.kr/content/showcase/7238): SHOWCASE RECOMMEND ITEM 양말 뚱냥이 사쉐 홀리데이 시즌을 맞아 사랑스러운 뚱냥이가 빨간 양말 속으로 쏙 들어왔어요. 소중한 사람에게 따뜻한 선물을 전해보세요. 따뜻한 뚱냥이 바디
- 확인할 사실: 상품명, 가격, 할인, 사은품, 기간
- 검토 표시: weak_explicit_season_signal

## Qwen/Qwen3-VL-4B-Instruct / 신년

실행 오류 또는 JSON 해석 실패: Model did not run: Sorry, I encountered an error: 'You have exceeded your ZeroGPU runs limit. Subscribe to Hugging Face PRO to get 40 min of ZeroGPU quota a day - https://huggingface.co/subscribe/pro?from=ZeroGPU'

## Qwen/Qwen3-VL-4B-Instruct / 연말(송년)

- 제목: 연말의 향기, 한 잔으로
- 설명: 차와 티로 마무리하는 한 해. 따뜻한 향기로 마음을 감싸는 순간을
- 버튼: 선물 선택
- 모델이 밝힌 참고 이유: 연말의 향기를 강조하고, 차/티 선물 카테고리의 따뜻한 분위기를 전달하는 문구로, 출석체크 기능과 관련된 문장에서 '연말의 페이지 한 잔으로 가다듬는 매일의 일상'을 참고해 시즌 차이를 명확히 표현했습니다.
- 출처:
  - [osulloc-002#s01](https://www.osulloc.com/kr/ko/life/event/view/12426): 2026년 11월 출석체크 조용히 다가온 연말의 페이지 한 잔으로 가다듬는 매일의 일상 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2
- 확인할 사실: 상품명, 가격, 할인, 사은품, 기간

## 실행 중 확인된 제약

최초 Hugging Face Inference Providers 비교는 크레딧 부족으로 실패했습니다. 그 경로의 Qwen3.5 9B·Gemma 3 4B·Llama 3.1 8B 결과를 생성한 것처럼 취급하지 않습니다. 무료 Space는 다른 모델이며 정확한 모델/Space를 각 결과 파일에 기록했습니다.
크리스마스·신년의 직접 레퍼런스가 적어 관련 차·선물·일상 표현을 참고했습니다. 이미지 OCR은 하지 않았습니다. 실제 상품·혜택·기간은 입력되지 않아 일반 카피로만 시험했습니다.
모델이 출처 ID를 출력했다는 사실만으로 올바르게 참고했다고 판정하지 않습니다. 레퍼런스 의미를 잘못 설명한 경우는 별도 검토 표시를 남겼습니다.
