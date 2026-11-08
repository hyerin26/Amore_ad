# VESSL 다운로드 모델 실험

기존 모델 3종을 VESSL의 개인 작업 폴더에 다운로드하고 같은 입력으로 실행하는 경로입니다.
실제 생성에는 서버의 localhost Ollama만 사용하며 외부 생성 API나 HF 무료 추론 한도를 쓰지 않습니다.

## 실행 대상과 저장 형식

- `gemma3n:e4b-it-q4_K_M`: Gemma 3n E4B IT 계열, 약 9.8GB.
- `gemma3:12b-it-q4_K_M`: Gemma 3 12B IT 계열, 약 8.2GB.
- `qwen3-vl:4b-instruct-q4_K_M`: Qwen3-VL 4B Instruct 계열, 약 3.3GB.

Ollama의 Q4_K_M 배포본을 사용합니다. 정확한 모델 digest·양자화·실제 바이트 수는
각 `download.json`과 `model_info.json`을 기준으로 확인합니다. BF16 공개 데모와 정밀도가 다릅니다.
세 모델은 총 약 21.3GB이며 실행기와 임시 저장 공간은 별도입니다.

작업 폴더는 서버의 `/root/osulloc-copy-test/`입니다.
`models/`에 가중치를, `runtime/`에 실행기를 두어 기존 모델/프로젝트와 구분합니다.
기존 HF 캐시나 프로젝트를 삭제하지 않습니다. 가중치·실행기·접속 토큰은 Git에 넣지 않습니다.

## 입력과 실행

상품은 **랑드샤 베스트 티 4종 세트**, 기간은 **12월 한 달**이며 연도·가격·할인·사은품은 미정입니다.
크리스마스·가을·송년·신년을 각각 hero 1구좌로 실행합니다. 가을은 감성 콘셉트,
신년은 12월의 새해맞이 준비입니다. 최신 오설록 메인과 기존 오설록 프로모션 발췌문을 전달합니다.
입력 해시는 기존 CPU 실험과 동일하게 계산하고 결과마다 입력 스냅샷을 보존합니다.

생성 설정은 온도 0.7, top_p 0.95, top_k 50, seed 42, 컨텍스트 4096,
최대 출력 1024토큰, 대화 이력 없음, JSON 강제 문법 없음입니다.
Ollama `/api/ps`의 VRAM 배치를 응답마다 기록하여 실제 GPU 사용 여부를 확인합니다.

서버에서 실행하는 예시입니다.

```bash
export OLLAMA_HOST=127.0.0.1:11435
export OLLAMA_MODELS=/root/osulloc-copy-test/models
export OLLAMA_NO_CLOUD=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
/root/osulloc-copy-test/runtime/bin/ollama serve
```

다른 서버 터미널에서 `copy-model-test/`로 이동한 후:

```bash
python3 run_ollama_models.py \
  --models-dir /root/osulloc-copy-test/models \
  --output runs/vessl-20261108/results
python3 report_run.py \
  --results runs/vessl-20261108/results \
  --output runs/vessl-20261108 \
  --label 'VESSL 4비트 다운로드 모델 재실험'
```

## 결과 해석

`results/<model>/<theme>.json`에 원문·입력·모델 digest·양자화·설정·시간·GPU 배치를 보존합니다.
`environment.json`에는 GPU 종류·드라이버·Ollama 버전·디스크 상태를 저장합니다.
다운로드나 로드가 실패하면 `load_error.json`에 남기고 문구를 대신 작성하지 않습니다.
기본 검사 통과는 담당자 승인이나 의미적 출처 충실함을 보증하지 않습니다.

Ollama의 총 응답 시간에는 첫 모델 로드가 포함될 수 있습니다.
세부 `load_duration`, `prompt_eval_duration`, `eval_duration`도 함께 보존하므로
모델 로드 시간과 문구 추론 시간을 구분해 보세요.

공식 근거:
- https://docs.ollama.com/linux
- https://docs.ollama.com/api/chat
- https://ollama.com/library/gemma3n:e4b
- https://ollama.com/library/gemma3:12b
- https://ollama.com/library/qwen3-vl:4b-instruct-q4_K_M

## 완료된 실행

최신 결과는 [runs/vessl-20261108/REPORT.md](runs/vessl-20261108/REPORT.md)에 있습니다.
지정 모델 3종 × 4주제에서 최종 문구 12건을 얻었고 기본 규칙 10건이 통과했습니다.
실험은 GPU 0 한 장에서 실행했으며, 모든 응답의 GPU 배치를 기록했습니다.
`pull_elapsed_seconds`는 해당 클라이언트의 pull 호출 시간입니다. 병렬 선행 다운로드를
사용했으므로 모델 전체의 최초 전송 시간으로 해석하지 않습니다.

기본 `qwen3-vl:4b`는 Thinking을 가리켜 비교에서 제외했습니다. 정확한 Instruct 태그와
모델 정체성 검사로 재실행했으며 제외 기록은 `runs/vessl-tag-check-20261108/`에 보존했습니다.
