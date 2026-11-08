"""Optional larger-model baseline: publicly advertised free community endpoint.
No API key. Runs only four requests and stops on rate limits/errors.
The 27B BF16 hosted model is NOT a tested laptop quantization.
"""
import datetime,hashlib,json,time,urllib.request
from pathlib import Path
from run_public_demos import HERE,SYSTEM,make_cases,dump
BASE='https://g9hnto0u7lvbu837.us-east-2.aws.endpoints.huggingface.cloud/v1'
MODEL='Qwen/Qwen3.8-27B'

def main():
 for case in make_cases():
  target=HERE/'results/qwen38_27b'/f"{case['theme_id']}.json"
  if target.exists():print('cached',case['theme_id'],flush=True);continue
  text=SYSTEM+'\n\n'+json.dumps(case,ensure_ascii=False)
  payload={'model':MODEL,'messages':[{'role':'user','content':text}],'max_tokens':512,'temperature':0.7,'top_p':0.8,'presence_penalty':1.5,'reasoning_effort':'none','stream':False}
  r={'model_key':'qwen38_27b','model':MODEL,'space':'victor/Qwen3.8-27B-free-endpoint','theme_id':case['theme_id'],'sampling':'Hosted BF16; temperature=0.7, top_p=0.8, presence_penalty=1.5, reasoning_effort=none; max_tokens=512','transport':'public advertised free community OpenAI-compatible endpoint; no token','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':hashlib.sha256(text.encode()).hexdigest()};start=time.monotonic();print('running',case['theme_id'],flush=True)
  try:
   response=json.load(urllib.request.urlopen(urllib.request.Request(BASE+'/chat/completions',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=180));raw=response['choices'][0]['message']['content']
   if not raw:raise RuntimeError('Empty message content')
   r.update(status='ok',raw_output=raw,usage=response.get('usage'),finish_reason=response['choices'][0].get('finish_reason'))
  except urllib.error.HTTPError as e:r.update(status='error',error=str(e),error_body=e.read().decode()[:2000])
  except Exception as e:r.update(status='error',error=str(e))
  r['elapsed_wall_seconds']=round(time.monotonic()-start,3);dump(target,r);print(r['status'],case['theme_id'],r['elapsed_wall_seconds'],r.get('error',''),flush=True)
  if r['status']=='error':break
if __name__=='__main__':main()
