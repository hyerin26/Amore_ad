# -*- coding: utf-8 -*-
"""One-shot localhost credential input for FREE Space tests; token kept in memory.
No token persistence, request logging, remote paid inference, or billing changes.
"""
import hashlib,json,os,secrets,subprocess,sys,threading,urllib.parse,urllib.request
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
HERE=Path(__file__).resolve().parent
PORT=8793;ORIGIN=f'http://127.0.0.1:{PORT}';NONCE=secrets.token_urlsafe(32)
state={'status':'waiting','message':'읽기 토큰을 입력하면 무료 데모 테스트를 이어서 실행합니다.'}
HTML='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>무료 모델 테스트 인증</title><style>body{font:17px system-ui;max-width:640px;margin:60px auto;padding:24px;background:#f2f5f1;color:#22372b}input,button{font:inherit;padding:12px;margin-top:12px;box-sizing:border-box;width:100%}button{background:#28583e;color:white;border:0;border-radius:8px}.box{background:white;padding:24px;border-radius:14px}small{color:#5b695e}</style><h1>무료 모델 테스트 인증</h1><div class="box"><p>Hugging Face의 <b>읽기(Read) 토큰</b>을 입력하세요.</p><p><a href="https://huggingface.co/settings/tokens" target="_blank" rel="noreferrer">Hugging Face 토큰 설정 열기</a> → Create new token → Read → 테스트용 이름 → 생성된 토큰을 복사하세요.</p><form method="post" action="/token"><input type="hidden" name="nonce" value="NONCE"><label>읽기 토큰<input name="token" type="password" autocomplete="off" placeholder="hf_..." required></label><button>무료 데모 테스트 실행</button></form><p><small>이 입력창은 이 노트북의 127.0.0.1에서만 열립니다. 토큰은 메모리에서만 사용하고 파일·로그·결과에 저장하지 않습니다. 인증은 Hugging Face 및 무료 HF Space에만 전달합니다. 유료 추론·크레딧 구매는 실행하지 않습니다.</small></p></div><p id="status">기다리는 중</p><script>setInterval(async()=>{let d=await(await fetch('/status')).json();document.getElementById('status').textContent=d.status+' — '+d.message;},2500)</script></html>'''.replace('NONCE',NONCE)
def worker(token):
 env=os.environ.copy();env['HF_TOKEN']=token
 try:
  # Only PUBLIC FREE SPACE RUNNER is allowed here. No paid router invocation.
  with open(HERE/'results/authenticated_run.log','w') as log:
   p=subprocess.Popen([sys.executable,str(HERE/'run_public_demos.py'),'--retry-errors'],env=env,stdout=log,stderr=log)
   env.pop('HF_TOKEN',None);token=None
   code=p.wait();state.update(status='done' if code==0 else 'error',message='무료 데모 실행을 마쳤습니다. 결과 검증을 진행합니다.' if code==0 else '실행 오류가 있습니다. 결과 로그를 확인합니다.')
 except Exception:state.update(status='error',message='실행 환경을 확인해야 합니다.')
 finally:env.pop('HF_TOKEN',None);token=None
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,code,body,kind='text/html; charset=utf-8'):
  data=body.encode();self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/status':self.send(200,json.dumps(state,ensure_ascii=False),'application/json');return
  if self.path=='/':self.send(200,HTML);return
  self.send(404,'없음')
 def do_POST(self):
  if self.path!='/token' or self.headers.get('Origin')!=ORIGIN or int(self.headers.get('Content-Length','0'))>4096:self.send(403,'요청을 확인해주세요.');return
  fields=urllib.parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode());token=fields.get('token',[''])[0].strip()
  if fields.get('nonce',[''])[0]!=NONCE or not token.startswith('hf_'):self.send(400,'Hugging Face 읽기 토큰 형식과 입력창을 확인해주세요.');return
  if state['status'] not in ('waiting','auth_error'):self.send(409,'이미 실행 중이거나 완료됐습니다.');return
  try:
   request=urllib.request.Request('https://huggingface.co/api/whoami-v2',headers={'Authorization':'Bearer '+token})
   with urllib.request.urlopen(request,timeout=20) as response:valid=response.status==200
   if not valid:raise ValueError()
  except Exception:
   token=None;state.update(status='auth_error',message='토큰 인증에 실패했습니다. 입력값을 확인해주세요.');self.send(401,'토큰 인증에 실패했습니다. 뒤로 가서 다시 입력해주세요.');return
  state.update(status='running',message='인증됐습니다. 무료 공개 데모를 실행 중입니다. 토큰 입력값은 보관하지 않습니다.')
  threading.Thread(target=worker,args=(token,),daemon=True).start();token=None;fields.clear()
  self.send(200,'<!doctype html><html lang="ko"><meta charset="utf-8"><title>테스트 실행 중</title><body><h1>인증됐습니다</h1><p>무료 공개 데모 테스트를 실행 중입니다. 이 탭을 닫아도 실행은 계속됩니다.</p><p id="status"></p><script>setInterval(async()=>{let d=await(await fetch("/status")).json();document.getElementById("status").textContent=d.status+" — "+d.message;},2500)</script></body></html>')
if __name__=='__main__':
 print('Local input ready: '+ORIGIN,flush=True)
 HTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
