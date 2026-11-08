# 기본 태그 해석 확인 기록 — 요청 모델 비교에서 제외

최초 `qwen3-vl:4b`를 내려받았으나 실제 `model_info.json`의 `details.parent_model`은
`dhiltgen/qwen3-vl:4b-thinking-q4_K_M-llamacpp`였습니다. 요청된 기존 모델은
**Qwen3-VL-4B-Instruct**이므로 이 4건을 요청 모델의 실험 결과로 집계하지 않습니다.

4건 모두 서버 요청은 완료됐지만 출력 1024토큰 한도에서 최종 `message.content`가 비어 있었습니다.
API 전송 성공과 문구 확보를 구분합니다. 원래의 최종 출력 문자열은 수정하지 않았습니다.
모델 메타데이터의 잘못된 초기 Instruct 라벨은 `original_model_label`에 남기고,
실제 Thinking 모델명과 `provenance_correction`, `excluded_from_requested_comparison=true`를 기록했습니다.

정확한 재실험은 `qwen3-vl:4b-instruct-q4_K_M`으로 수행하며
`../vessl-20261108/`에 별도로 저장합니다. 실행기에 모델 정체성 검사를 추가해
Thinking 모델을 Instruct 결과로 조용히 대체하지 않도록 했습니다.

태그 대응은 [Ollama 공식 태그 목록](https://ollama.com/library/qwen3-vl/tags)과
실제 다운로드한 `model_info.json`을 함께 확인했습니다. Instruct의 품질 실패 점수로
이 진단 기록을 사용하지 않습니다.
