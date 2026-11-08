"""Check homepage sections and refreshed public evidence without touching old pages."""
import json
from pathlib import Path
from bs4 import BeautifulSoup,Tag
from section_inference import text
BASE=Path(__file__).parent/'data'
def validate():
 p=json.loads((BASE/'pages/osulloc-004.json').read_text());html=(BASE/p['html_file']).read_text();root=BeautifulSoup(html,'html.parser').find()
 rows=[json.loads(l) for l in (BASE/'index.jsonl').read_text().splitlines()];r=next(r for r in rows if r['id']==p['id'])
 assert len({r['id'] for r in rows})==len(rows)
 assert len(html.encode())==r['html_bytes']
 assert len(p['sections'])==r['n_sections']>1
 assert text(root)==p['text']==' '.join(s['text'] for s in p['sections'] if s['text'])
 assert not root.select('script,iframe,input[type="hidden"]')
 assets={a['id']:a for a in p['image_assets']};assigned=set();paths=[]
 for i,s in enumerate(p['sections'],1):
  assert s['id']==f's{i:02d}' and s['order']==i
  n=root
  for off in s['dom_path'][1:]:n=[x for x in n.children if isinstance(x,Tag)][off-1]
  assert n.get('id')==s['dom_id'] and text(n)==s['text']
  assert all(not (s['dom_path'][:len(t)]==t or t[:len(s['dom_path'])]==s['dom_path']) for t in paths);paths.append(s['dom_path'])
  for aid in s['image_ids']:assert s['id'] in assets[aid]['section_ids']
  for rel in s['relationship_indexes']:assert 0<=rel<len(p['relationships']);assigned.add(rel)
 assert assigned==set(range(len(p['relationships'])))
 for a in assets.values():
  assert set(a['section_ids'])=={s['id'] for s in p['sections'] if a['id'] in s['image_ids']}
 assert len(assets)==r['n_images']
 for f in (BASE/'revisits/20261108').glob('*.html'):
  soup=BeautifulSoup(f.read_text(),'html.parser');assert not soup.select('script,iframe,input,textarea')
  assert all(not k.lower().startswith('on') for n in soup.find_all(True) for k in n.attrs)
 print(f'PASS: osulloc-004 {len(p["sections"])} sections, {len(assets)} assets; DOM paths, coverage and references valid; revisit snapshots sanitized.')
if __name__=='__main__':validate()
