# -*- coding: utf-8 -*-
"""Pull three original model families and run saved hero cases on a private Ollama server.
No generation is sent to HF/paid APIs. Downloaded weights remain in OLLAMA_MODELS.
"""
import argparse,datetime,hashlib,json,platform,shutil,subprocess,time,urllib.error,urllib.request
from pathlib import Path
from run_public_demos import HERE,SYSTEM,dump
MODELS={
 'gemma3n_e4b':{'model':'google/gemma-3n-E4B-it','tag':'gemma3n:e4b-it-q4_K_M'},
 'gemma3_12b':{'model':'google/gemma-3-12b-it','tag':'gemma3:12b-it-q4_K_M'},
 'qwen3vl_4b':{'model':'Qwen/Qwen3-VL-4B-Instruct','tag':'qwen3-vl:4b-instruct-q4_K_M'},
}

def validate_identity(key,info):
 if key=='qwen3vl_4b' and 'thinking' in info.get('details',{}).get('parent_model','').lower():
  raise ValueError('Resolved Qwen model is Thinking, not requested Instruct; refusing to generate.')

def api(base,path,data=None,timeout=900):
 req=urllib.request.Request(base+path,None if data is None else json.dumps(data).encode(),{'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def pull(base,tag):
 req=urllib.request.Request(base+'/api/pull',json.dumps({'model':tag,'stream':True}).encode(),{'Content-Type':'application/json'})
 last=0
 with urllib.request.urlopen(req,timeout=900) as response:
  for line in response:
   row=json.loads(line)
   if row.get('error'):raise RuntimeError(row['error'])
   if time.monotonic()-last>25 or row.get('status')=='success':
    print(tag,row.get('status'),row.get('completed'),row.get('total'),flush=True);last=time.monotonic()

def run(args):
 # Only a local loopback service, optionally reached through an SSH tunnel.
 from urllib.parse import urlparse
 if urlparse(args.base_url).hostname not in ('127.0.0.1','localhost','::1'):raise ValueError('Use a loopback Ollama server; external generation is disallowed by this runner.')
 cases=json.loads((HERE/'inputs/single_slot_cases.json').read_text(encoding='utf-8'))
 args.output.mkdir(parents=True,exist_ok=True)
 hardware={'platform':platform.platform(),'python':platform.python_version(),'ollama':api(args.base_url,'/api/version'),'models_directory':str(args.models_dir),'disk_before':dict(zip(['total','used','free'],shutil.disk_usage(args.models_dir))),'run_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:hardware['gpu_inventory']=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.free','--format=csv'],text=True)
 except (FileNotFoundError,subprocess.CalledProcessError):hardware['gpu_inventory']='not available'
 dump(args.output/'environment.json',hardware)
 options={'temperature':.7,'top_p':.95,'top_k':50,'seed':42,'num_predict':1024,'num_ctx':4096}
 for key in args.models:
  spec=MODELS[key];tag=spec['tag'];start=time.monotonic();print('pulling',tag,flush=True)
  try:
   pull(args.base_url,tag)
   tags=api(args.base_url,'/api/tags')['models'];tag_meta=next(r for r in tags if r['name']==tag)
   info=api(args.base_url,'/api/show',{'model':tag});dump(args.output/key/'model_info.json',info)
   dump(args.output/key/'download.json',{'source_model':spec['model'],'tag':tag,**tag_meta,'pull_elapsed_seconds':round(time.monotonic()-start,3),'storage':'persistent models directory; no weights committed to Git'})
   quant=info.get('details',{}).get('quantization_level',tag_meta.get('details',{}).get('quantization_level'))
   validate_identity(key,info)
  except Exception as exc:
   dump(args.output/key/'load_error.json',{'model':spec['model'],'status':'load_error','error':type(exc).__name__+': '+str(exc)[:2000]});print('download failed',key,type(exc).__name__,flush=True);continue
  for case in cases:
   prompt=SYSTEM+'\n\n'+json.dumps(case,ensure_ascii=False);ih=hashlib.sha256(prompt.encode()).hexdigest();target=args.output/key/(case['theme_id']+'.json')
   if target.exists():
    old=json.loads(target.read_text())
    if old.get('input_sha256')!=ih or old.get('revision')!=tag_meta['digest'] or old.get('generation_config')!=options:raise RuntimeError('Input/model/settings changed; preserve previous run in another folder.')
    if old.get('status')=='ok':print('cached',key,case['theme_id'],flush=True);continue
   row={'model_key':key,'model':spec['model'],'ollama_tag':tag,'revision':tag_meta['digest'],'quantization':quant,'space':None,'theme_id':case['theme_id'],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_case':case,'input_sha256':ih,'transport':'VESSL downloaded model, private localhost Ollama inference; no external generation API','sampling':f'{quant}; temperature=.7, top_p=.95, top_k=50, seed=42, max_tokens=1024, num_ctx=4096; no JSON grammar, no history','generation_config':options,'environment_file':'environment.json','download_file':key+'/download.json'}
   begin=time.monotonic();print('running',key,case['theme_id'],flush=True)
   try:
    payload={'model':tag,'messages':[{'role':'user','content':prompt}],'stream':False,'options':options,'keep_alive':'5m'}
    if 'thinking' in info.get('capabilities',[]):payload['think']=False
    response=api(args.base_url,'/api/chat',payload)
    if not response.get('done') or response.get('error'):raise RuntimeError(str(response.get('error') or 'Generation did not finish'))
    running=api(args.base_url,'/api/ps')
    row.update(status='ok',raw_output=response['message']['content'],request_think=payload.get('think'),finish_reason=response.get('done_reason'),input_tokens=response.get('prompt_eval_count'),output_tokens=response.get('eval_count'),timings={k:response[k] for k in ['total_duration','load_duration','prompt_eval_duration','eval_duration'] if k in response},gpu_placement=running)
    if not any(m.get('size_vram',0)>0 for m in running.get('models',[])):row['runtime_warning']='No GPU placement verified; do not claim GPU inference for this response.'
   except Exception as exc:row.update(status='error',error=type(exc).__name__+': '+str(exc)[:2000])
   row['elapsed_wall_seconds']=round(time.monotonic()-begin,3);dump(target,row);print(row['status'],key,case['theme_id'],row['elapsed_wall_seconds'],flush=True)
  # Unload this model's memory; keep the downloaded model files on disk.
  try:api(args.base_url,'/api/generate',{'model':tag,'keep_alive':0})
  except Exception as exc:print('unload warning',type(exc).__name__,flush=True)
 hardware['disk_after']=dict(zip(['total','used','free'],shutil.disk_usage(args.models_dir)));dump(args.output/'environment.json',hardware)
 print('Run finished:',args.output,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base-url',default='http://127.0.0.1:11435');p.add_argument('--models',nargs='+',choices=list(MODELS),default=list(MODELS));p.add_argument('--models-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
