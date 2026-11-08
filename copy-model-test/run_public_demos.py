# -*- coding: utf-8 -*-
"""Run free public Gradio Space APIs. No purchase or local weight download; optional HF free-account token.
Python standard library only. Space availability and anonymous ZeroGPU quota vary.
"""
import argparse, datetime, hashlib, json, os, re, time, uuid, urllib.request, urllib.error
from pathlib import Path
HERE=Path(__file__).resolve().parent
MODELS={
 'gemma3n_e4b':{'model':'google/gemma-3n-E4B-it','space':'huggingface-projects/gemma-3n-E4B-it','host':'https://huggingface-projects-gemma-3n-e4b-it.hf.space','endpoint':'generate','sampling':'Space source sets do_sample=False; bf16; max_new_tokens=512'},
 'gemma3_12b':{'model':'google/gemma-3-12b-it','space':'huggingface-projects/gemma-3-12b-it','host':'https://huggingface-projects-gemma-3-12b-it.hf.space','endpoint':'run','sampling':'Space leaves sampling at model generation defaults; bf16; max_new_tokens=512'},
 'qwen3vl_4b':{'model':'Qwen/Qwen3-VL-4B-Instruct','space':'akhaliq/Qwen3-VL-4B-Instruct','host':'https://akhaliq-qwen3-vl-4b-instruct.hf.space','endpoint':'chat_fn','sampling':'Space source sets temperature=0.7, do_sample=True, top_p=0.95; max_new_tokens=512'}
}
for size in ['4b','8b','14b']:
 MODELS['qwen3_'+size]={'model':'Qwen/Qwen3-'+size.upper(),'space':'Qwen/Qwen3-Demo','host':'https://qwen-qwen3-demo.hf.space','endpoint':'add_message','remote_model':'qwen3-'+size,'sampling':'Official demo provider-backed endpoint; thinking_budget=1K; sampling and precision not exposed; fresh session per request; no user API key'}
MODELS.update({
 'gemma2_2b':{'model':'google/gemma-2-2b-it','space':'huggingface-projects/gemma-2-2b-it','host':'https://huggingface-projects-gemma-2-2b-it.hf.space','endpoint':'generate','adapter':'text','sampling':'bf16; max_new_tokens=512; temperature=0.7, top_p=0.95, top_k=50, repetition_penalty=1.2'},
 'llama32_3b':{'model':'meta-llama/Llama-3.2-3B-Instruct','space':'huggingface-projects/llama-3.2-3B-Instruct','host':'https://huggingface-projects-llama-3-2-3b-instruct.hf.space','endpoint':'generate','adapter':'text','sampling':'bf16; max_new_tokens=512; temperature=0.7, top_p=0.95, top_k=50, repetition_penalty=1.2'},
 'gemma4_e4b':{'model':'google/gemma-4-e4b-it','space':'huggingface-projects/gemma-4-e4b-it','host':'https://huggingface-projects-gemma-4-e4b-it.hf.space','endpoint':'chat','adapter':'gemma4','sampling':'bf16; max_new_tokens=512; temperature=0.7, top_p=0.95; thinking=False'},
})
SYSTEM='''입력 주제에 맞는 오설록 광고 문구를 새로 작성하세요. 입력을 복사해 반환하지 마세요.
확정 사실: 상품 '랑드샤 베스트 티 4종 세트', 기간 '12월 한 달'. 가격·할인·사은품·세부 맛·효능은 미정이므로 쓰지 마세요. 과거 레퍼런스는 어조와 표현 구조만 참고하세요. 과거 혜택과 협업을 이번 행사로 옮기지 마세요.
제목 28자, 설명 60자, 버튼 14자 이내. 설명에 정확한 상품명을 포함하세요. 지정한 주제만 표현하세요. 오설록 출처 1~2개와 참고 요소를 적으세요.
출력은 다음 구조의 JSON 하나입니다. 다른 입력 필드를 출력하지 마세요.
{"theme_id":"입력 theme_id","id":"hero","layout":"hero","title":"주제에 맞는 제목","subtitle":"상품명을 포함한 설명","cta":"버튼 문구","period":"12월 한 달","reference_ids":["참고한 ID"],"evidence":"참고한 표현 구조","details_needed":[]}'''

def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def make_cases():
 reqs=json.loads((HERE/'inputs/requests.json').read_text(encoding='utf-8'));cases=[]
 notes={'christmas':'크리스마스 선물과 함께하는 티타임','autumn':'행사기간은 12월이며, 가을의 여운을 떠올리는 감성 콘셉트','year_end':'한 해를 마무리하며 고마움을 전하는 송년 선물','new_year':'행사기간은 12월이며, 다가올 새해를 준비하는 선물'}
 for r in reqs:
  fresh=next(x for x in r['references'] if x['reference_id'].startswith('osulloc-004#'))
  editorial_id=next(s for s in r['slots'] if s['id']=='editorial')['suggested_reference_ids'][0]
  editorial=next(x for x in r['references'] if x['reference_id']==editorial_id)
  refs=[]
  for ref in [fresh,editorial]:
   if ref['reference_id'] in {x['reference_id'] for x in refs}:continue
   snippet=ref['text'][:160]
   refs.append({'reference_id':ref['reference_id'],'brand':ref['brand'],'role':ref['role'],'text':snippet})
  cases.append({'theme_id':r['theme_id'],'theme':r['theme'],'concept':notes[r['theme_id']],'product_facts':r['product_facts'],'references':refs})
 dump(HERE/'inputs/single_slot_cases.json',cases)
 for c in cases:(HERE/'prompts'/f"{c['theme_id']}_hero.txt").write_text(SYSTEM+'\n\n'+json.dumps(c,ensure_ascii=False),encoding='utf-8')
 return cases

def call_space(model,case,timeout=180):
 text=SYSTEM+'\n\n'+json.dumps(case,ensure_ascii=False)
 if model.get('adapter')=='text':data=[text,512,0.7,0.95,50,1.2]
 elif model.get('adapter')=='gemma4':data=[text,[],[],False,512,280,'',0.7,0.95,64,1.0]
 elif model['endpoint']=='add_message':data=[text,{'model':model['remote_model'],'sys_prompt':'You are a helpful assistant.','thinking_budget':1}]
 else:data=[{'text':text,'files':[]},[]] if model['endpoint']=='chat_fn' else [{'text':text,'files':[]},'You are a helpful assistant.',512]
 url=model['host']+'/gradio_api/call/'+model['endpoint']
 headers={'Content-Type':'application/json','User-Agent':'amoread-copy-benchmark/1.0'}
 if os.environ.get('HF_TOKEN'):headers['Authorization']='Bearer '+os.environ['HF_TOKEN']
 request=urllib.request.Request(url,json.dumps({'data':data}).encode(),headers)
 job=json.load(urllib.request.urlopen(request,timeout=30));eid=job['event_id']
 events=[];kind=None;final=None
 with urllib.request.urlopen(urllib.request.Request(url+'/'+eid,headers=headers),timeout=timeout) as stream:
  for raw in stream:
   line=raw.decode().rstrip('\r\n')
   if line.startswith('event:'):kind=line[6:].strip()
   if line.startswith('data:'):
    value=json.loads(line[5:].strip());events.append({'event':kind,'data':value})
    if kind=='error':raise RuntimeError('Space inference error: '+json.dumps(value,ensure_ascii=False))
    if kind=='complete':final=value;break
 if final is None:raise RuntimeError('SSE ended without completion')
 if model['endpoint']=='add_message':
  messages=final[1].get('value',[]) if isinstance(final[1],dict) else final[1]
  assistant=next(m for m in reversed(messages) if m.get('role')=='assistant')
  raw=''.join(c.get('content','') for c in assistant.get('content',[]) if c.get('type')=='text')
  if not raw or '<span' in raw:raise RuntimeError('Official demo returned no model answer: '+raw[:300])
 elif model['endpoint']=='chat_fn':
  # Published chat_fn returns [cleared textbox, updated message history].
  history=final[1];raw=next(m['content'] for m in reversed(history) if m.get('role')=='assistant')
 else:
  raw=final[0]
  if isinstance(raw,dict) and 'content' in raw:raw=raw['content']
 if isinstance(raw,str) and re.match(r'Sorry, I encountered an error:|Error:',raw):
  raise RuntimeError('Model did not run: '+raw)
 return raw,{'event_id':eid,'completion':final}

def main():
 p=argparse.ArgumentParser();p.add_argument('--models',nargs='+',choices=list(MODELS),default=['gemma3n_e4b','gemma3_12b','qwen3vl_4b','gemma2_2b','llama32_3b','gemma4_e4b']);p.add_argument('--themes',nargs='+');p.add_argument('--prepare-only',action='store_true');p.add_argument('--retry-errors',action='store_true');a=p.parse_args();cases=make_cases()
 if a.prepare_only:return
 for key in a.models:
  model=MODELS[key]
  for case in cases:
   if a.themes and case['theme_id'] not in a.themes:continue
   target=HERE/'results'/key/(case['theme_id']+'.json')
   expected=hashlib.sha256((SYSTEM+'\n\n'+json.dumps(case,ensure_ascii=False)).encode()).hexdigest()
   if target.exists() and json.loads(target.read_text()).get('input_sha256')!=expected:raise RuntimeError('Input changed; archive previous results before running: '+str(target))
   if target.exists() and (json.loads(target.read_text()).get('status')=='ok' or not a.retry_errors):print('cached attempt',key,case['theme_id'],flush=True);continue
   print('running',key,case['theme_id'],flush=True);start=time.monotonic()
   result={'model_key':key,**model,'theme_id':case['theme_id'],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'transport':'public Gradio SSE API, authenticated HF free quota; token not stored' if os.environ.get('HF_TOKEN') else 'public Gradio SSE API, anonymous, no HF token','input_case':case,'input_sha256':hashlib.sha256((SYSTEM+'\n\n'+json.dumps(case,ensure_ascii=False)).encode()).hexdigest()}
   try:
    raw,meta=call_space(model,case);result.update(status='ok',raw_output=raw,transport_response=meta)
   except Exception as e:result.update(status='error',error=str(e))
   result['elapsed_wall_seconds']=round(time.monotonic()-start,3);dump(target,result)
   print(result['status'],key,case['theme_id'],result['elapsed_wall_seconds'],str(result.get('error',''))[:350],flush=True)
   if result['status']=='error' and re.search(r'quota|runs limit',result.get('error',''),re.I):
    print('ZeroGPU quota reached; stopping the whole public-demo run without automatic retries.',flush=True);return
if __name__=='__main__':main()
