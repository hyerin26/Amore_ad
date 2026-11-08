# 오설록 레퍼런스 기반 카피 모델 테스트

`tea_ad`의 실제 `title`·`subtitle`·`cta` 필드와 수집 레퍼런스를 이용하는 문구 추천 실험입니다.
현재 실험은 **랑드샤 베스트 티 4종 세트 / 12월 한 달(12월 1일~31일, 연도 미정)**을
네 콘셉트에 공통으로 입력합니다. 가격·할인·사은품·맛별 세부 구성은 지정하지 않았습니다.
현재 소형 모델 2종 × 4주제의 새 응답 8건을 얻었으며 기본 규칙은 3건 통과했습니다.
긴 입력으로 실행한 첫 8건도 별도 보존합니다. 검토 경고 없는 승인 문구를 확보했다는 뜻은 아닙니다.
가을은 계절 감성 콘셉트, 신년은 12월의 새해맞이 준비로 해석합니다.
이 조건은 사용자가 정한 가상 실험이며 실제 오설록 행사 공지가 아닙니다.

## 결과와 이전 실험

- [현재 문구·검사 결과](REPORT.md), [HTML 보고서](REPORT.html), [해석과 개선점](FINDINGS.md).
- `runs/baseline-category-only/`: 상품·기간 미정이었던 이전 실험의 입력·원문·보고서.
  당시 Gemma 3n E4B 4건, Gemma 3 12B 4건, Qwen3-VL 4B 3건의 실제 응답을 얻었습니다.
- `runs/december-public-attempt/`: 12월 조건으로 공개 데모를 재호출한 기록.
  인증 후에도 기존 모델은 무료 GPU 한도에 걸렸고, Qwen3 공식 데모의 4B·8B·14B는
  서버 오류로 실패했습니다. 이 경로에서 새 문구가 생성됐다고 집계하지 않습니다.
- `runs/december-local-long-prompt/`: 긴 다중 시즌 지침으로 실행한 로컬 모델 2종 × 4주제.
  입력 복사와 주제 혼동을 확인한 후 단일 주제·오설록 출처 2개로 입력을 단순화했습니다.
- `results/`: 같은 상품·기간으로 간결한 단일 주제 입력을 사용해 **실제로 로컬에서 실행한 모델**의 원문·설정·시간·검사 결과.
  모델별 실제 성공 여부는 REPORT와 해당 JSON의 `status`를 기준으로 봅니다.

## 레퍼런스 저장 방식

전체 원본은 저장소의 `reference/data/`에 있습니다. 현재 195개 페이지 레코드이며,
오설록 이벤트 3개와 새 메인 페이지 1개가 포함됩니다. 새 메인은 `osulloc-004`이고
13개 섹션으로 나눠 HTML 위치·이미지·링크 관계를 보존했습니다.
`reference/data/revisits/20261108/`에는 기존 이벤트 3개와 목록의 최신 DOM도 보관합니다.
이벤트 목록의 3건은 이미 `osulloc-001..003`에 있어 새 이벤트처럼 중복 등록하지 않았습니다.
이미지 OCR은 하지 않았으며 화면에 없는 프로모션을 추정해서 추가하지 않았습니다.

검색은 단순 키워드·섹션 역할·오설록 가산점 방식입니다. 카운트다운 숫자 구간은 제외하고,
각 실제 요청에 최신 오설록 메인 배너를 포함합니다. 전체 구좌 준비 자료에는 외부 몰 사례도 포함합니다. 현재 소형 모델용 hero 입력은
주제 혼동을 줄이기 위해 오설록 발췌문 2개로 좁혔습니다.
`inputs/requests.json`에 출처 URL·텍스트·파일 해시를, `single_slot_cases.json`에 모델에
전달한 발췌문을 보존합니다. 과거 레퍼런스의 가격·쿠폰·협업은 현재 행사 사실이 아닙니다.

## 파일 구조

```text
prepare.py                    수집 자료 검색·입력 및 전체 구좌 프롬프트 생성
run_public_demos.py           공개 데모 호출; 할당량 오류 시 전체 호출 중단
run_local_gguf.py             로컬 llama.cpp CPU 실행; 모델 파일은 외부 경로 지정
run_api.py                    향후 Ollama / 호환 추론 서버 어댑터
local_token_input.py          필요 시 읽기 토큰을 메모리에서만 받는 localhost 입력창
evaluate.py                   구조·상품명·기간·숫자·출처 검사 및 보고서 생성
inputs/                       현재 상품·기간·주제·구좌·레퍼런스와 디자인 계약
prompts/                      실제 hero 요청과 전체 구좌용 요청
results/<model>/<theme>.json   모델 원문, 입력 스냅샷·해시, 설정, 실행 시간
source_evidence/              원본 계약과 모델 출처·실행 근거
runs/                         이전 실험 및 실패한 공개 데모 시도 보존
REPORT.md / REPORT.html       현재 실험 결과
FINDINGS.md                    품질 검토와 한계
tests/                        알려진 사실 허용·허위 숫자/기간/출처 검증
```

`tea_ad` 전체 코드를 포함하지 않고, 확인한 커밋·필드·레이아웃·근거 파일 해시만 저장합니다.
관찰 커밋은 `21c378f97d07c0428ef49dd2bd8b2a006b55026a`입니다.
원본 기획 프로그램이나 localStorage·가격·Undo 이력은 변경하지 않습니다.
UX_WRITING의 해요체는 업무 UI 지침이며 공식 소비자 마케팅 문체로 간주하지 않습니다.
차분하고 따뜻한 문체와 제목 28자·설명 60자·버튼 14자 제한은 이번 실험의 설정입니다.

## 실행

아래는 이 폴더에서 실행합니다. Python 3.9 이상, Python 코드는 표준 라이브러리를 씁니다.
레퍼런스 수집/검증 스크립트는 별도로 beautifulsoup4가 필요합니다.

```bash
python3 prepare.py --reference ../reference/data --design /path/to/tea_ad
python3 run_public_demos.py --prepare-only
```

실제 비교 단위는 주제별 **hero 1구좌**입니다. 전체 4구좌 요청도 준비하지만,
`prompts/all_themes.txt`가 있다는 이유로 4구좌 모두를 실행했다고 간주하지 않습니다.

로컬 GGUF를 내려받고, 자신의 OS에 맞는 공식 [llama.cpp](https://github.com/ggml-org/llama.cpp)를
준비한 뒤 실행합니다. 모델·실행기는 Git 저장소 밖에 둡니다.

```bash
python3 run_local_gguf.py --server /path/to/llama-server \
  --weights /path/to/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --model Qwen/Qwen2.5-1.5B-Instruct --key qwen25_15b_local --quantization Q4_K_M
python3 evaluate.py
python3 -m unittest discover -s tests -v
```

실제로 추가 실행한 모델은 Qwen2.5 0.5B와 1.5B의 공식 Q4_K_M입니다.
0.5B는 성능의 하한을 확인하는 소형 기준선이며 최종 배포 추천으로 간주하지 않습니다.

0.5B 비교는 `--weights`, `--model`, `--key`를 각각 해당 모델 값으로 바꿉니다.
현재 로컬 실행은 CPU 4스레드, GPU/KV/연산 오프로딩 없음, 컨텍스트 4096,
온도 0.7·top_p 0.95·seed 42·최대 출력 1024토큰이며 JSON 강제 문법은 쓰지 않습니다.
각 요청은 대화 이력이 없고 모델 응답을 수정하지 않습니다. 모델마다 양자화·크기가 다르므로
이 결과를 모델 계열 전체의 순위로 일반화하지 마세요.

무료 공개 데모의 할당량이 있을 때:

```bash
python3 run_public_demos.py --models gemma3n_e4b gemma3_12b qwen3vl_4b
# 추가 어댑터: gemma2_2b, llama32_3b, gemma4_e4b
# 인증이 필요할 때만 실행: python3 local_token_input.py
```

추가 어댑터가 있다는 것은 해당 모델에서 새 응답을 얻었다는 뜻이 아닙니다.
무료 GPU 한도에 걸리면 다른 Space로 옮겨 한도를 우회하지 않고 전체 실행을 멈춥니다.
토큰은 파일/결과에 저장하지 않고 유료 추론이나 결제는 호출하지 않습니다.
이미 성공한 같은 입력은 다시 실행하지 않습니다. 입력이 달라지면 이전 결과를
별도 실행 폴더에 보존한 후 새 실험을 시작해야 합니다.

## 검사와 해석

상품명·허용 날짜를 제외한 숫자, 미확정 혜택·효능·타사 문구, 잘못된 주제/구좌/출처,
누락된 상품명·기간을 검사합니다. 코드펜스를 벗겨 읽으면 `strict_json=false`로 남깁니다.
기계 검사를 통과해도 카피 매력·브랜드 적합성·근거의 의미적 충실함은 별도 검토 대상입니다.
작은 모델의 실패도 원문 그대로 보존하고 사람이 작성한 문구로 대체하지 않습니다.

공식 다운로드 및 라이선스는 `source_evidence/model_sources_december.json`을 참고하세요.
소형 모델의 로컬 실행 시간과 공개 데모의 네트워크·큐 포함 시간을 직접 비교하지 않습니다.
