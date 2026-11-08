# -*- coding: utf-8 -*-
"""Create a separate Markdown/HTML report for a downloaded-model run."""
import argparse,html,json
from pathlib import Path
from evaluate import evaluate
from run_public_demos import HERE,dump

def report(results,output,label):
 output.mkdir(parents=True,exist_ok=True)
 cases={c['theme_id']:c for c in json.loads((HERE/'inputs/single_slot_cases.json').read_text())}
 sources={r['reference_id']:r for req in json.loads((HERE/'inputs/requests.json').read_text()) for r in req['references']}
 rows=[]
 for f in sorted(results.glob('*/*.json')):
  result=json.loads(f.read_text())
  if 'theme_id' not in result:continue
  row=dict(result);row.pop('input_case',None)
  if result.get('status')=='ok':row['evaluation']=evaluate(result['raw_output'],result.get('input_case',cases[result['theme_id']]))
  rows.append(row)
 summary={'run_label':label,'scope':'3 downloaded models x 4 themes, hero only; actual results below; missing/error files are not generated answers','results':[str(f.relative_to(results)) for f in sorted(results.glob('*/*.json'))],'attempts':len(rows),'responses':sum(r['status']=='ok' for r in rows),'basic_passes':sum(r.get('evaluation',{}).get('passed',False) for r in rows),'review_ready':sum(r.get('evaluation',{}).get('review_ready',False) for r in rows),'rows':rows}
 dump(output/'evaluation.json',summary)
 lines=[f'# {label}','','상품: **랑드샤 베스트 티 4종 세트** · 기간: **12월 한 달(연도 미정)**. 크리스마스·가을·송년·신년 각 hero 1구좌를 비교합니다. 가을은 감성 콘셉트, 신년은 12월의 새해 준비입니다. 가격·할인·사은품은 미정입니다.','',f"실제 응답 {summary['responses']}건 / 기본 규칙 통과 {summary['basic_passes']}건 / 경고 없는 기계 검사 {summary['review_ready']}건. 이는 담당자의 문구 승인이나 의미적 출처 충실함을 보증하지 않습니다.",'','| 모델 | 주제 | 상태 | 기본 규칙 | 검토 사항 | 추론 시간(초) |','|---|---|---|---|---|---:|']
 for r in rows:
  e=r.get('evaluation',{});issues=e.get('issues',[])+e.get('warnings',[])
  lines.append(f"| {r['model']} | {cases[r['theme_id']]['theme']} | {r['status']} | {'통과' if e.get('passed') else '미통과/미실행'} | {'; '.join(issues) or '-'} | {r['elapsed_wall_seconds']} |")
 names=list(dict.fromkeys(r['model'] for r in rows))
 if names:
  lines+=['','## 주제별 제목 비교','','| 주제 | '+' | '.join(names)+' |','|---|'+'---|'*len(names)]
  for tid,case in cases.items():
   titles=[]
   for name in names:
    row=next((r for r in rows if r['theme_id']==tid and r['model']==name),{})
    title=row.get('evaluation',{}).get('output',{}).get('title','응답/형식 확인 필요')
    titles.append(str(title).replace('|','/').replace('\n',' '))
   lines.append('| '+case['theme']+' | '+' | '.join(titles)+' |')
 for r in rows:
  lines+=['',f"## {r['model']} / {cases[r['theme_id']]['theme']}",'',f"설정: {r.get('sampling')} · 모델 revision: {r.get('revision','미기록')}",'']
  e=r.get('evaluation',{});o=e.get('output')
  if o:
   lines += [f"- 제목: {o.get('title','')}",f"- 설명: {o.get('subtitle','')}",f"- 버튼: {o.get('cta','')}",f"- 기간: {o.get('period','미출력')}",f"- 모델의 참고 이유: {o.get('evidence','')}"]
   for rid in o.get('reference_ids') or []:
    ref=sources.get(rid)
    if ref:lines.append(f"- 출처 [{rid}]({ref['url']}): {ref['text'][:160]}")
   lines.append('- 추가 확인: '+(', '.join(map(str,o.get('details_needed') or [])) or '추가 항목 미출력'))
  else:lines.append('실행/형식 오류: '+str(r.get('error') or e.get('issues')))
  lines+=['','```json',json.dumps(r.get('raw_output'),ensure_ascii=False),'```']
 errors=[]
 for f in sorted(results.glob('*/load_error.json')):
  data=json.loads(f.read_text());errors.append(data);lines+=['',f"## 모델 로드 실패: {data['model']}",'',data['error']]
 summary['load_errors']=errors;dump(output/'evaluation.json',summary)
 lines+=['','이전 CPU·공개 데모 결과는 별도 폴더에 보존합니다. 설정·양자화·장비·입력이 다른 결과를 같은 모델 순위로 취급하지 않습니다. 다운로드·모델 로드 시간은 문구 추론 시간에서 제외하며 결과 JSON에 별도로 남깁니다.']
 (output/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 body=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(label)+'</title><style>body{font-family:system-ui;max-width:1100px;margin:40px auto;padding:0 20px;background:#f4f6f2;color:#183b2c}article{background:white;padding:24px;margin:20px 0;border:1px solid #d5ded6;border-radius:12px}.warning{color:#98520d}pre{white-space:pre-wrap;overflow-wrap:anywhere}h3{font-size:26px}</style><h1>'+html.escape(label)+'</h1><p>랑드샤 베스트 티 4종 세트 · 12월 한 달 · 실제 다운로드 모델의 서버 추론</p>']
 for r in rows:
  e=r.get('evaluation',{});o=e.get('output');esc=lambda x:html.escape(str(x))
  body.append('<article><h2>'+esc(r['model'])+' / '+esc(cases[r['theme_id']]['theme'])+'</h2>')
  if o:
   body+=['<h3>'+esc(o.get('title',''))+'</h3><p>'+esc(o.get('subtitle',''))+'</p><p>버튼: '+esc(o.get('cta',''))+' · 기간: '+esc(o.get('period','미출력'))+'</p>','<p class="warning">'+esc('; '.join(e['issues']+e['warnings']) or '기계 검사 경고 없음; 담당자 검토 필요')+'</p>','<details><summary>근거와 원문</summary><pre>'+esc(json.dumps(o,ensure_ascii=False,indent=2))+'</pre></details>']
  else:body.append('<p class="warning">'+esc(r.get('error') or e.get('issues'))+'</p><details><summary>모델 원문</summary><pre>'+esc(r.get('raw_output',''))+'</pre></details>')
  body.append('</article>')
 for error in errors:body.append('<article><h2>'+html.escape(error['model'])+'</h2><p>'+html.escape(error['error'])+'</p></article>')
 (output/'REPORT.html').write_text(''.join(body)+'</html>',encoding='utf-8')
 print(json.dumps({k:summary[k] for k in ['attempts','responses','basic_passes','review_ready']},ensure_ascii=False))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--label',default='VESSL 다운로드 모델 재실험');a=p.parse_args();report(a.results,a.output,a.label)
