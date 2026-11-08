"""Deterministic format/fact/citation checks, not an LLM or human quality score."""
import argparse, difflib, html, json, re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
LIMITS={'title':28,'subtitle':60,'cta':14}
SEASONS={'christmas':['크리스마스','성탄'],'autumn':['가을','낙엽','선선'],'year_end':['연말','송년','한 해','감사'],'new_year':['신년','새해','시작']}

def parse_output(raw):
 if isinstance(raw,dict):return raw,True,[]
 try:return json.loads(raw),True,[]
 except (TypeError,json.JSONDecodeError):pass
 cleaned=raw.strip();notes=[]
 if cleaned.startswith('```'):
  cleaned=re.sub(r'^```(?:json)?\s*','',cleaned);cleaned=re.sub(r'\s*```$','',cleaned);notes.append('code_fence_removed')
 try:return json.loads(cleaned),False,notes
 except json.JSONDecodeError:raise ValueError('Response is not parseable JSON; raw output retained')

def evaluate(raw,case):
 issues=[];warnings=[]
 try:obj,strict,normalization=parse_output(raw)
 except ValueError as e:return {'parseable':False,'strict_json':False,'issues':[str(e)],'warnings':[],'passed':False}
 if not isinstance(obj,dict):return {'parseable':False,'strict_json':strict,'issues':['Root must be an object'],'warnings':[],'passed':False}
 if obj.get('theme_id')!=case['theme_id']:issues.append('wrong_theme_id')
 if obj.get('id')!='hero' or obj.get('layout')!='hero':issues.append('wrong_slot_contract')
 lengths={}
 for field,limit in LIMITS.items():
  v=obj.get(field);lengths[field]=len(v) if isinstance(v,str) else None
  if not isinstance(v,str) or not v.strip():issues.append('missing_'+field)
  elif len(v)>limit:issues.append(field+'_too_long')
 copy=' '.join(obj.get(f,'') for f in LIMITS if isinstance(obj.get(f),str))
 if re.search(r'\d|[%％]',copy):issues.append('unsupported_numeric_claim')
 if re.search(r'최저가|단독|무료|증정|선착순|할인|숙면|면역|치료|효능',copy):issues.append('unsupported_offer_or_effect_claim')
 if re.search(r'29CM|컬리|코오롱|카카오|신세계|W컨셉|덴마크|헤더먼트|뚱냥이',copy,re.I):issues.append('competitor_leak')
 allowed={r['reference_id']:r for r in case['references']};ids=obj.get('reference_ids')
 if not isinstance(ids,list) or not 1<=len(ids)<=2 or any(not isinstance(i,str) or i not in allowed for i in ids):issues.append('invalid_reference_ids')
 evidence=obj.get('evidence','')
 if not isinstance(evidence,str) or not evidence.strip():issues.append('missing_reference_evidence')
 else:
  cited_text=' '.join(allowed[i]['text'] for i in ids or [] if isinstance(i,str) and i in allowed)
  if any(s in evidence for s in ['과거 크리스마스','크리스마스 시즌 프로모션']) and not any(s in cited_text for s in ['크리스마스','성탄']):warnings.append('reference_season_misattribution: cited snippets do not document Christmas')
  if '가을 프로모션' in evidence and '가을' not in cited_text:warnings.append('reference_season_misattribution: cited snippets do not document autumn')
 if not any(k in copy for k in SEASONS[case['theme_id']]):warnings.append('weak_explicit_season_signal')
 source_text=' '.join(r['text'] for r in case['references']);compact=lambda s:re.sub(r'\s+','',s)
 longest=difflib.SequenceMatcher(None,compact(copy),compact(source_text),autojunk=False).find_longest_match(0,len(compact(copy)),0,len(compact(source_text))).size
 if longest>=18:warnings.append('long_reference_overlap_requires_review')
 if not isinstance(obj.get('details_needed'),list):issues.append('missing_details_needed')
 return {'parseable':True,'strict_json':strict,'normalization':normalization,'lengths':lengths,'issues':issues,'warnings':warnings,'max_reference_overlap_chars':longest,'passed':not issues,'review_ready':not issues and not warnings,'output':obj}

def main():
 cases={c['theme_id']:c for c in json.loads((HERE/'inputs/single_slot_cases.json').read_text())};rows=[]
 for file in sorted((HERE/'results').glob('*/*.json')):
  r=json.loads(file.read_text())
  if 'model_key' not in r or 'theme_id' not in r:continue
  item={k:r.get(k) for k in ['model_key','model','space','theme_id','status','sampling','elapsed_wall_seconds','error']}
  if r['status']=='ok':item['evaluation']=evaluate(r['raw_output'],cases[r['theme_id']])
  rows.append(item)
 summary={'method':'one initial sample per model/theme; deterministic checks only, no human preference scores','scope':'hero title/subtitle/cta for 4 seasons; full 4-layout prompts also prepared but not all executed','comparability':'Public demo sampling settings differ. Network/queue latency is not local inference speed. Hosted bf16/full-precision quality does not establish quantized laptop quality.','rows':rows}
 (HERE/'results/evaluation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 lines=['# 오설록 시즌 카피 — 실제 공개 모델 테스트','','레퍼런스 194건과 tea_ad의 실제 title/subtitle/cta 계약을 읽어 입력을 구성했습니다. 이번 실행 범위는 4개 시즌 × 모델별 메인 비주얼 1구좌입니다.','', '## 실행 상태','','| 모델 | 시즌 | 상태 | 글자 수(title/subtitle/cta) | 구조·기본 규칙 | 추가 검토 | 경과(초) |','|---|---|---|---|---|---|---:|']
 for r in rows:
  e=r.get('evaluation',{});lens=e.get('lengths',{});length='/'.join(str(lens.get(f,'-')) for f in LIMITS);warnings='; '.join(e.get('issues',[])+e.get('warnings',[])) or '-'
  lines.append(f"| {r['model']} | {cases[r['theme_id']]['theme']} | {r['status']} | {length} | {'통과' if e.get('passed') else '미통과/미실행'} | {warnings} | {r['elapsed_wall_seconds']} |")
 lines+=['','통과는 JSON 내용·글자 수·숫자/금지 표현·입력 출처 ID 같은 기계 검사 결과입니다. 카피의 매력·브랜드 적합성·근거의 의미적 충실함을 보증하지 않습니다. strict_json 여부는 evaluation.json에서 별도로 기록합니다.','공개 데모끼리 생성 설정이 달라 엄밀한 모델 순위로 해석하지 않습니다. 경과 시간에는 네트워크와 무료 GPU 대기가 포함됩니다.']
 for r in rows:
  lines+=['',f"## {r['model']} / {cases[r['theme_id']]['theme']}",'']
  e=r.get('evaluation',{});o=e.get('output')
  if not o:lines.append('실행 오류 또는 JSON 해석 실패: '+str(r.get('error') or e.get('issues')));continue
  lines += [f"- 제목: {o.get('title','')}",f"- 설명: {o.get('subtitle','')}",f"- 버튼: {o.get('cta','')}",f"- 모델이 밝힌 참고 이유: {o.get('evidence','')}",'- 출처:']
  for i in o.get('reference_ids') or []:
   ref=next((x for x in cases[r['theme_id']]['references'] if x['reference_id']==i),None)
   if ref:
    request=next(x for x in json.loads((HERE/'inputs/requests.json').read_text()) if x['theme_id']==r['theme_id']);source=next(x for x in request['references'] if x['reference_id']==i);lines.append(f"  - [{i}]({source['url']}): {ref['text'][:110]}")
  lines.append('- 확인할 사실: '+', '.join(map(str,o.get('details_needed') or [])))
  if e.get('warnings'):lines.append('- 검토 표시: '+'; '.join(e['warnings']))
 lines+=['','## 실행 중 확인된 제약','','최초 Hugging Face Inference Providers 비교는 크레딧 부족으로 실패했습니다. 그 경로의 Qwen3.5 9B·Gemma 3 4B·Llama 3.1 8B 결과를 생성한 것처럼 취급하지 않습니다. 무료 Space는 다른 모델이며 정확한 모델/Space를 각 결과 파일에 기록했습니다.','크리스마스·신년의 직접 레퍼런스가 적어 관련 차·선물·일상 표현을 참고했습니다. 이미지 OCR은 하지 않았습니다. 실제 상품·혜택·기간은 입력되지 않아 일반 카피로만 시험했습니다.','모델이 출처 ID를 출력했다는 사실만으로 올바르게 참고했다고 판정하지 않습니다. 레퍼런스 의미를 잘못 설명한 경우는 별도 검토 표시를 남겼습니다.']
 (HERE/'REPORT.md').write_text('\n'.join(lines)+'\n')
 # Standalone escaped, read-only HTML report. All source/model content is text.
 body=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>오설록 카피 모델 테스트</title><style>body{font-family:system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 22px;background:#f5f7f4;color:#21362b}article{background:white;border:1px solid #dbe3dc;border-radius:14px;padding:22px;margin:18px 0}h2{font-size:20px}.meta{color:#647067;font-size:13px}h3{font-size:28px;line-height:1.4}.cta{display:inline-block;border-radius:6px;background:#24553f;color:white;padding:9px 15px}.warning{color:#9b4d12}details{margin-top:18px}pre{white-space:pre-wrap}</style><h1>오설록 시즌 카피 모델 테스트</h1><p>실제 공개 데모 응답 · 메인 비주얼 4개 시즌 · 출처와 검증 표시</p><p class="meta">이 결과는 공식 브랜드 승인 문구가 아닙니다. 공개 데모 설정·정밀도가 달라 모델 순위를 확정하지 않습니다.</p>']
 for r in rows:
  e=r.get('evaluation',{});o=e.get('output');esc=lambda x:html.escape(str(x))
  body.append('<article><h2>'+esc(cases[r['theme_id']]['theme'])+' · '+esc(r['model'])+'</h2>')
  if o:
   body+=['<h3>'+esc(o.get('title',''))+'</h3><p>'+esc(o.get('subtitle',''))+'</p><span class="cta">'+esc(o.get('cta',''))+'</span>','<p class="meta">기본 규칙 '+('통과' if e['passed'] else '미통과')+' · 글자 수 '+esc(e['lengths'])+'</p>']
   if e['issues'] or e['warnings']:body.append('<p class="warning">'+esc('; '.join(e['issues']+e['warnings']))+'</p>')
   body.append('<details><summary>출처·모델의 참고 이유·확인할 사실</summary><pre>'+esc(json.dumps(o,ensure_ascii=False,indent=2))+'</pre></details>')
  else:body.append('<p class="warning">'+esc(r.get('error') or e.get('issues'))+'</p>')
  body.append('</article>')
 (HERE/'REPORT.html').write_text(''.join(body)+'</html>')
 print(json.dumps({'attempts':len(rows),'successful_transport':sum(r['status']=='ok' for r in rows),'basic_rule_passes':sum(r.get('evaluation',{}).get('passed',False) for r in rows)},ensure_ascii=False))
if __name__=='__main__':main()
