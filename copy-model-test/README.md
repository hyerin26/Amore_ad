# 오설록 레퍼런스 기반 카피 모델 테스트

이 폴더는 실제 수집 레퍼런스와 `EunseongOH/tea_ad`의 디자인/데이터 계약을 읽어
문구 추천 요청을 만들고, 공개 모델의 응답과 실패를 기록하는 재현 가능한 실험입니다.

## 이번 실행 결과

- 실제 생성 모델 3종, 4개 주제, 문구 응답 11건을 확보했습니다.
- Gemma 3n E4B: 4/4 응답. 신년의 주제 ID 오류 1건.
- Gemma 3 12B: 4/4 응답. 시즌 구분과 미확정 상품 표현은 추가 검토가 필요합니다.
- Qwen3-VL 4B Instruct: 3/4 응답. 신년은 무료 사용량 제한으로 생성되지 않았습니다.
- 전체 11건 중 기본 규칙 검사 10건 통과. 출처의 의미적 충실함과 카피 매력은 별도 검토입니다.
- [판단과 개선점](FINDINGS.md), [실제 문구와 출처](REPORT.md), [HTML 보기](REPORT.html).
- 코드의 검증 테스트 8개가 통과했습니다. 실제 노트북에서의 모델 추론은 아직 측정하지 않았습니다.

## 저장소 안의 위치

이 실험의 코드·입력·프롬프트·원문 결과·보고서·검증은 모두 `copy-model-test/` 안에 있습니다.
전체 수집 원본은 저장소의 기존 `reference/data/`를 사용하며, 실험에 실제 전달한
레퍼런스 발췌문과 원본 URL은 이 폴더의 `inputs/requests.json`에 보존했습니다.
`tea_ad` 저장소 전체는 복제해 포함하지 않고, 확인한 필드·레이아웃과 근거 파일 해시를
`inputs/design_contract.json`, `source_evidence/`에 저장했습니다.

아래 실행 명령은 `copy-model-test/` 폴더에서 실행하는 기준입니다.

## 입력으로 읽은 자료

- `Amore_ad/reference/data`: 194개 페이지 JSON과 섹션. 검색 대상으로 사용할 수 있는 텍스트 구간 576개.
- `tea_ad` main: 브라우저에서 인증된 접근으로 ZIP을 내려받아 읽었습니다.
  관찰한 커밋은 `21c378f97d07c0428ef49dd2bd8b2a006b55026a`입니다.
- `src/app.js`: 실제 구좌 레이아웃 `hero`, `grid2`, `grid3`, `split`, `benefit`, `editorial`,
  실제 문구 필드 `title`, `subtitle`, `cta`를 확인했습니다.
- `AGENTS.md`, `design/UX_WRITING.md`, 데이터/상태 계약, 마스터 맥락 문서를 읽었습니다.
- 원본 디자인 프로그램과 기존 레퍼런스 데이터는 변경하지 않았습니다. 기획안의
  localStorage, 가격, 상품, Undo/Redo에도 추천 결과를 자동 적용하지 않습니다.

UX_WRITING.md의 해요체는 업무 UI의 규칙이며 소비자용 공식 오설록 카피 규칙은 아닙니다.
이번의 차분하고 따뜻한 문체, 제목 28자·설명 60자·버튼 14자 제한은 실험용 설정입니다.

## 이번 실행 범위

- 주제: 크리스마스, 가을, 연말(송년), 신년.
- **실제로 실행하는 무료 비교의 단위는 주제별 `hero` 1구좌**입니다.
- 구좌마다 title/subtitle/cta, 참고 출처 ID, 참고 이유, 추가 확인할 사실을 받습니다.
- 전체 4구좌(hero/grid2/benefit/editorial) 요청도 `inputs/payload.json`과
  `prompts/all_themes.txt`에 준비했습니다. 이 파일이 존재한다고 4구좌 전부의 모델 추론을
  실행한 것은 아닙니다. 실제 결과 범위는 REPORT와 results의 상태를 기준으로 확인합니다.
- 실제 SKU·가격·할인·사은품·기간은 입력받지 않았으므로 만들지 않도록 제한했습니다.
- 과거 레퍼런스의 혜택을 이번 행사 사실로 옮기는 것을 금지했습니다.

## 파일 구조

```text
prepare.py                   레퍼런스 검색 및 디자인 계약/프롬프트 생성
run_public_demos.py          무료 공개 HF Space API 실행; 한도 오류 자동 반복 안 함
run_api.py                   향후 HF/로컬 OpenAI 호환 서버/Ollama 연결
local_token_input.py         필요 시 무료 계정 토큰을 메모리에서만 받는 로컬 입력창
run_community_endpoint.py    더 큰 모델의 선택적 무료 엔드포인트 시도; 현재 중지됨
evaluate.py                 JSON/길이/금지 주장/출처 ID 검증 및 보고서 생성
inputs/design_contract.json  확인한 실제 필드·레이아웃과 근거 파일 해시
inputs/requests.json         시즌별 구좌 및 검색된 레퍼런스(원본 URL 포함)
inputs/single_slot_cases.json 실제 hero 비교 입력
inputs/payload.json          전체 4구좌 비교를 위한 API 요청
prompts/                    모델에 넣은 요청문
results/<model>/<theme>.json 원문 응답 또는 오류, 정확한 모델/Space, 설정, 소요 시간
results/evaluation.json     기계 검증 결과와 해석의 한계
source_evidence/             입력 근거 해시 및 민감정보 없는 오류/빈 입력창 화면
REPORT.md / REPORT.html      사람이 확인하는 결과표
tests/                      잘못된 숫자·출처·주제·오류 응답을 거르는 검증 테스트
```

`raw_output`은 수정하지 않은 모델 응답입니다. 코드펜스를 제거해 JSON으로 읽은 경우에도
원문과 `strict_json=false`를 남깁니다. 서버가 에러 문구를 정상 HTTP 응답으로 감싸더라도
문구 추천 성공으로 집계하지 않습니다. 실패 파일에 추천 문구를 대신 만들어 넣지 않습니다.

## 실행 방법

Python 3.9 이상에서 표준 라이브러리만으로 실행할 수 있습니다.
원본 폴더를 직접 지정하면 입력부터 다시 만들 수 있습니다.

```bash
python3 prepare.py --reference /path/to/Amore_ad/reference/data --design /path/to/tea_ad
python3 run_public_demos.py --prepare-only
python3 run_public_demos.py
python3 evaluate.py
python3 -m unittest discover -s tests -v
```

현재 결과 파일이 있으면 기본 실행은 다시 호출하지 않습니다. 무료 할당량이 회복됐거나
로그인으로 인증한 후에만 `--retry-errors`를 사용하세요. ZeroGPU 한도가 나타나면 해당
Space의 추가 호출을 멈춥니다. 유료 크레딧을 자동 구매하거나 계정/네트워크를 바꿔 한도를
우회하는 로직은 없습니다.

무료 계정 인증이 필요할 때:

```bash
python3 local_token_input.py
```

터미널에 표시된 127.0.0.1 주소를 본인 브라우저에서 열어 HF **읽기(Read) 토큰**을 넣습니다.
토큰은 저장하지 않고 인증된 무료 Space 실행 프로세스의 메모리/환경에서만 사용합니다.
이 입력창은 유료 HF Inference Providers를 호출하지 않습니다. 테스트가 끝나면 서버를
Ctrl+C로 종료합니다. 입력창/토큰 설정 화면을 캡처하거나 토큰을 저장소에 커밋하지 마세요.

향후 로컬 Ollama에서 전체 4주제·4구좌 프롬프트 실행 예시:

```bash
python3 run_api.py --backend ollama --model <설치한-모델-태그> --output results/ollama-full.json
```

로컬 OpenAI 호환 서버 예시(`--base-url`은 `/v1`까지):

```bash
python3 run_api.py --backend openai-compatible --base-url http://127.0.0.1:8000/v1 --model <서버-모델-ID> --output results/local-full.json
```

`run_api.py`의 전체 구좌 응답은 모델 원문을 저장합니다. hero 전용의 `evaluate.py`가
전체 4구좌 응답을 평가한 것으로 간주하지 마세요. 필요한 경우 동일한 제약 검사를 각
campaign/section에 확장해 적용해야 합니다.

## 비교 결과 해석

- 처음 선택했던 Qwen3.5 9B·Gemma 3 4B·Llama 3.1 8B의 유료 라우팅 경로는
  크레딧 부족으로 실패했습니다. 이 모델들의 성공 결과는 없습니다.
- 무료 실행 모델은 `run_public_demos.py`의 MODELS에 있는 정확한 모델들입니다.
  일부가 실패하면 보고서에 그대로 남깁니다. 무료 데모 서비스는 일시 중지되거나
  한도가 바뀔 수 있습니다.
- 데모별 샘플링 설정이 다르고 양자화도 통제하지 못하므로 엄밀한 모델 순위는 아닙니다.
  시간은 네트워크·큐·원격 추론을 합친 벽시계 시간이며 노트북 추론 속도가 아닙니다.
- HF에서 좋은 문구가 나와도 사내 PC의 4비트 양자화 모델 품질/메모리/속도를 별도로
  확인해야 합니다. 멀티모달 모델은 이번에 텍스트만 사용했습니다.
- 입력 레퍼런스를 검색했다는 것, 모델이 출처 ID를 말했다는 것만으로 의미적으로
  올바르게 참고했다고 판정하지 않습니다. source_season 관련 경고와 실제 원문을 함께 봅니다.
- 기존 레퍼런스는 이미지 OCR을 하지 않아 이미지 안 카피가 빠질 수 있습니다.
  크리스마스·신년 직접 사례도 부족합니다. 현재 검색은 단순 키워드/역할 기반이라
  출산 선물처럼 시즌 관련성이 낮은 사례가 섞일 수 있어 검색 품질 개선이 필요합니다.
- 자동 통과는 구조·글자 수·숫자/금지 표현·출처 ID 검사 결과입니다. 현업의 문체·기획
  적합성 평가는 별도이며 이번 실험에는 사람의 채택률/점수를 만들어 넣지 않았습니다.

공식 자료:
- https://huggingface.co/spaces/huggingface-projects/gemma-3n-E4B-it
- https://huggingface.co/spaces/huggingface-projects/gemma-3-12b-it
- https://huggingface.co/spaces/akhaliq/Qwen3-VL-4B-Instruct (커뮤니티 데모, 원본 모델은 Qwen)
- https://huggingface.co/docs/inference-providers/pricing
