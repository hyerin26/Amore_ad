# -*- coding: utf-8 -*-
"""Import homepage with section/image/link conventions; preserve original event records."""
import json,sys,re
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup,Tag
import argparse
parser=argparse.ArgumentParser(description='Import main.json and sanitized event revisit snapshots from a browser collection.')
parser.add_argument('snapshots',type=Path)
parser.add_argument('--data',type=Path,default=Path(__file__).resolve().parent/'data')
args=parser.parse_args()
sys.path.insert(0,str(Path(__file__).resolve().parent))
from import_promotion_snapshots import build,SELECTORS
from section_inference import BOUNDARIES
SELECTORS['osulloc']='main'
# Reuse existing authored boundaries for the three event pages; add main modules.
BOUNDARIES['osulloc']='#main_banner .swiper-slide, #main_promotion, #main_product, #main_event, #main_recommended, #main_todays_event .todays_event, #main_explore, #main_brand, .event_view_detail .evt_cont, .event_view_detail [id^="section"], .event_view_detail .evt_visual, .event_sns_share, .more_events, .event_user_comment'
data=args.data;rows=[json.loads(l) for l in (data/'index.jsonl').read_text().splitlines()]
for name,pid in [('main','osulloc-004')]:
 if any(r['id']==pid for r in rows):raise ValueError('Refusing to overwrite '+pid)
 raw=json.loads((args.snapshots/(name+'.json')).read_text());page,html=build(raw,'osulloc',pid,raw['url'])
 # Classes inspected on the rendered main identify editorial/product modules.
 soup=BeautifulSoup(html,'html.parser');root=soup.find()
 for sec in page['sections']:
  node=root
  for offset in sec['dom_path'][1:]:node=[c for c in node.children if isinstance(c,Tag)][offset-1]
  mid=node.get('id','')
  if node.find_parent(id='main_banner'):sec['role']='hero' if 'swiper-slide' in node.get('class',[]) else 'section_navigation'
  elif mid=='main_product':sec['role']='section_navigation'
  elif mid in ('main_promotion','main_recommended'):sec['role']='product_list'
  elif mid=='main_event':sec['role']='related_promotions'
  elif mid in ('main_brand','main_explore'):sec['role']='brand_story'
  elif node.find_parent(id='main_todays_event'):sec['role']='brand_story'
  if sec['text'].startswith('베스트 세트 티 제품'):sec['role']='section_navigation'
  sec['role_evidence']='authored_main_module_markup'
 page['capture_note']='2026-11-08 main refresh. Event details 12413/12426/12412 already exist as osulloc-001..003; their current DOM snapshots are separately archived without duplicating reference IDs. Prices are observed historical data, not experimental offers.'
 (data/'pages'/f'{pid}.json').write_text(json.dumps(page,ensure_ascii=False,indent=1));(data/'pages'/f'{pid}.html').write_text(html)
 rows=[r for r in rows if r['id']!=pid]
 rows.append(dict(id=pid,brand='osulloc',url=raw['url'],resolved_url=raw['url'],host='www.osulloc.com',path_hint='kr/ko',title=raw['title'],page_title=raw['title'],status=page['status'],collected_date='2026-11-08',meta_file=f'pages/{pid}.json',html_file=page['html_file'],html_bytes=len(html.encode()),n_sections=len(page['sections']),n_images=len(page['image_assets'])))
 print(pid,len(page['sections']))
(data/'index.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
# Retain sanitized current snapshots of already indexed details for revisit evidence.
archive=data/'revisits/20261108';archive.mkdir(parents=True,exist_ok=True)
for name in ['12413','12426','12412','listing']:
 raw=json.loads((args.snapshots/(name+'.json')).read_text());soup=BeautifulSoup(raw['html'],'html.parser')
 for n in soup.select('script,iframe,noscript,svg,input,textarea'):n.decompose()
 for n in soup.find_all(True):
  for k in list(n.attrs):
   if k.lower().startswith('on'):del n.attrs[k]
 (archive/(name+'.html')).write_text(str(soup))
meta={'date':'2026-11-08','entry_url':'https://www.osulloc.com/kr/ko','main_reference_id':'osulloc-004','event_listing_url':'https://www.osulloc.com/kr/ko/life/event/list/ing','event_ids':['osulloc-001','osulloc-002','osulloc-003'],'event_numbers':['12413','12426','12412'],'new_event_detail_count':0,'method':'Browser-rendered DOM, event list currently exposes exactly these three existing events. Initial state, no OCR or participation/coupon actions.','snapshots':[f'{n}.html' for n in ['12413','12426','12412','listing']]}
(archive/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
brands=json.loads((data/'brands.json').read_text());brands['osulloc']['main_refresh']=meta;brands['osulloc']['additional_page_count']=1
pages=[json.loads(f.read_text()) for f in (data/'pages').glob('osulloc-*.json')]
brands['osulloc']['counts']=dict(Counter(p['status'] for p in pages))
brands['osulloc']['relationship_collection']['counts_by_status']=dict(Counter(r['status'] for p in pages for r in p['relationships']))
section_meta=brands['osulloc']['section_collection']
section_meta['section_count']=sum(len(p['sections']) for p in pages)
section_meta['page_counts']=dict(Counter(p['section_status'] for p in pages))
section_meta['image_asset_count']=sum(len(p['image_assets']) for p in pages)
section_meta['image_tag_counts']=dict(Counter(t for p in pages for a in p['image_assets'] for t in a['tags']))
(data/'brands.json').write_text(json.dumps(brands,ensure_ascii=False,indent=1))
