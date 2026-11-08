# -*- coding: utf-8 -*-
"""Run isolated hero requests against a user-supplied llama.cpp GGUF model.
Weights/runtime are outside the repository. Standard library, no credentials.
"""
import argparse,datetime,hashlib,json,subprocess,time,urllib.request
from pathlib import Path
from run_public_demos import HERE,SYSTEM,make_cases,dump

def main():
 p=argparse.ArgumentParser();p.add_argument('--server',type=Path,required=True);p.add_argument('--weights',type=Path,required=True);p.add_argument('--model',required=True);p.add_argument('--key',required=True);p.add_argument('--quantization',required=True);p.add_argument('--port',type=int,default=8794);a=p.parse_args()
 weight_hash=hashlib.sha256()
 with a.weights.open('rb') as weights_file:
  for chunk in iter(lambda:weights_file.read(1024*1024),b''):weight_hash.update(chunk)
 cases=make_cases();url=f'http://127.0.0.1:{a.port}';logpath=HERE/'results'/a.key/'server.log';logpath.parent.mkdir(parents=True,exist_ok=True)
 version=subprocess.check_output([str(a.server.resolve()),'--version'],stderr=subprocess.STDOUT,text=True).strip()
 with logpath.open('w') as log:
  proc=subprocess.Popen([str(a.server.resolve()),'-m',str(a.weights.resolve()),'--host','127.0.0.1','--port',str(a.port),'-c','4096','-t','4','-ngl','0','--device','none','--no-kv-offload','--no-op-offload','--fit','off','--parallel','1'],stdout=log,stderr=log)
  try:
   deadline=time.monotonic()+180
   while time.monotonic()<deadline:
    if proc.poll() is not None:raise RuntimeError('llama-server exited; inspect server.log')
    try:
     with urllib.request.urlopen(url+'/health',timeout=2) as r:
      if r.status==200:break
    except Exception:time.sleep(.5)
   else:raise TimeoutError('llama-server did not become ready')
   for c in cases:
    target=HERE/'results'/a.key/(c['theme_id']+'.json')
    prompt=SYSTEM+'\n\n'+json.dumps(c,ensure_ascii=False)
    ih=hashlib.sha256(prompt.encode()).hexdigest()
    if target.exists():
     old=json.loads(target.read_text())
     if old.get('input_sha256')!=ih:raise RuntimeError('Input changed; archive previous results before running: '+str(target))
     if old.get('status')=='ok':continue
    print('running',a.model,c['theme_id'],flush=True);start=time.monotonic()
    out={'model_key':a.key,'model':a.model,'space':None,'theme_id':c['theme_id'],'input_case':c,'input_sha256':ih,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'transport':'local llama.cpp CPU, 4 threads, Apple Silicon arm64; no external inference','sampling':f'{a.quantization}; temperature=0.7, top_p=0.95, seed=42, max_tokens=1024; no JSON grammar; no history; thinking disabled','runtime_version':version,'weights_filename':a.weights.name,'weights_sha256':weight_hash.hexdigest()}
    payload={'model':a.model,'messages':[{'role':'user','content':prompt}],'temperature':.7,'top_p':.95,'seed':42,'max_tokens':1024,'stream':False,'chat_template_kwargs':{'enable_thinking':False}}
    try:
     req=urllib.request.Request(url+'/v1/chat/completions',json.dumps(payload).encode(),{'Content-Type':'application/json'})
     with urllib.request.urlopen(req,timeout=300) as response:data=json.load(response)
     out.update(status='ok',raw_output=data['choices'][0]['message']['content'],finish_reason=data['choices'][0]['finish_reason'],usage=data.get('usage'),timings=data.get('timings'))
    except Exception as e:out.update(status='error',error=str(e))
    out['elapsed_wall_seconds']=round(time.monotonic()-start,3);dump(target,out);print(out['status'],c['theme_id'],out['elapsed_wall_seconds'],flush=True)
  finally:
   proc.terminate()
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
if __name__=='__main__':main()
