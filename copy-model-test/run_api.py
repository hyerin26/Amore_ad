"""Run the prepared 4-theme/4-layout payload against your future server or HF.
No dependency beyond Python 3.9+. Credentials are read only from environment.
"""
import argparse,json,os,time,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--backend',choices=['hf','openai-compatible','ollama'],required=True);p.add_argument('--model',required=True);p.add_argument('--base-url');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 payload=json.loads((HERE/'inputs/payload.json').read_text());token=None
 if a.backend=='hf':
  url='https://router.huggingface.co/v1/chat/completions';token=os.environ.get('HF_TOKEN')
  if not token:p.error('Set HF_TOKEN locally; never put it in a source file or chat.')
  payload['model']=a.model
 elif a.backend=='openai-compatible':
  if not a.base_url:p.error('--base-url is required')
  url=a.base_url.rstrip('/')+'/chat/completions';payload['model']=a.model;token=os.environ.get('MODEL_API_KEY')
 else:
  url=(a.base_url or 'http://127.0.0.1:11434').rstrip('/')+'/api/chat';payload={'model':a.model,'messages':payload['messages'],'stream':False,'format':'json','options':{'temperature':0.7,'num_predict':6400,'num_ctx':16384}}
 headers={'Content-Type':'application/json'}
 if token:headers['Authorization']='Bearer '+token
 start=time.monotonic();response=json.load(urllib.request.urlopen(urllib.request.Request(url,json.dumps(payload).encode(),headers),timeout=600))
 raw=response['message']['content'] if a.backend=='ollama' else response['choices'][0]['message']['content']
 result={'backend':a.backend,'model':a.model,'elapsed_wall_seconds':time.monotonic()-start,'raw_output':raw,'response':response}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Saved:',a.output)
if __name__=='__main__':main()
