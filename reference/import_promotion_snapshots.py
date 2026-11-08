"""Append browser DOM snapshots to the existing reference index (never overwrite pages).

Usage: python import_promotion_snapshots.py SNAPSHOTS TARGETS OUTPUT
Snapshots: <brand>-NNN.json with url, title, html, text, description, og_image.
Requires beautifulsoup4. Source URL order in TARGETS defines stable page IDs.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag
from section_inference import partition, infer_role

DATE = '2026-11-08'
SELECTORS = {
    'kakao_gift': '#mArticle', 'shinsegaev': 'section.event-detail',
    'zigzag': '#__content_editor', 'hankkitongsal': '#contents',
    'dongwonmall': '#content', 'cjthemarket': '.event-page',
    'wconcept': '.content',
}
UNAVAILABLE = {
    'kolonmall-002': 'No promotion body rendered; the page shows a dialog saying it will return to the mall homepage.',
    'shinsegaev-004': 'Requested plan detail redirected to the general event listing; listing content is not the requested promotion.',
}

def clean_text(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip()

def destination_type(url, base=None):
    if not url: return 'unknown'
    if url.startswith('#'): return 'same_page_anchor'
    parsed = urlsplit(url); path=parsed.path.lower()
    if re.search(r'product|goods|/prd|/item', path): return 'product_detail'
    if re.search(r'cart|checkout|order',path): return 'cart_or_checkout'
    if re.search(r'login|signin',path): return 'login'
    if re.search(r'event|promotion|special|plan|magazine|/page/', path): return 'promotion'
    if parsed.scheme not in ('http','https'): return 'external_action'
    return 'external_page' if base and parsed.netloc != urlsplit(base).netloc else 'other_store_page'

def dom_path(node, root):
    path = []
    while node is not root:
        parent = node.parent
        path.append([c for c in parent.children if isinstance(c, Tag)].index(node) + 1)
        node = parent
    return [1] + list(reversed(path))

def build(raw, brand, pid, url):
    page = dict(id=pid, brand=brand, collected_date=DATE, url=url,
                listing_label=raw.get('title') or url, resolved_url=raw['url'],
                description=raw.get('description'), images=[], og_image=raw.get('og_image'),
                text='', title=raw.get('title'), status='captured', relationships=[],
                relationship_capture_status='extracted_from_html',
                source_revisit={'resolved_url': raw['url'], 'status':'revisited', 'title':raw.get('title')},
                sections=[], image_assets=[], section_status='inferred_from_html', html_file=None)
    if pid in UNAVAILABLE:
        page.update(status='body_unavailable', section_status='body_unavailable',
                    capture_note=UNAVAILABLE[pid], observed_text=raw.get('text',''))
        return page, ''
    soup = BeautifulSoup(raw['html'], 'html.parser')
    if brand == 'kolonmall':
        root = soup.select_one('.special-detail')
        root = next((p for p in root.parents if 'pt_var(--d-header-h)' in p.get('class', [])), root.parent.parent.parent.parent)
    else:
        root = soup.select_one(SELECTORS[brand])
    if root is None: raise ValueError(f'{pid}: missing promotion root')
    # Drop executable code, trackers, SVG icons and hidden form/session values.
    for node in root.select('script,iframe,noscript,svg,input[type="hidden"]'):
        node.decompose()
    page['text'] = clean_text(root)
    if brand == 'cjthemarket':
        page.update(status='app_handoff', capture_note='Desktop page exposes promotional images and QR/app handoff; full app event body was not available. No app interaction was performed.')
    parts = partition(root, brand)
    section_of = {}
    for order, node in enumerate(parts, 1):
        sid = f's{order:02d}'
        for e in [node, *node.find_all(True)]: section_of[id(e)] = sid
        headings = [clean_text(h) for h in node.select('h1,h2,h3,h4,h5,h6') if clean_text(h)]
        role, evidence = infer_role(node, order, brand)
        page['sections'].append(dict(id=sid, order=order, role=role,
            role_evidence=evidence, headings=headings,
            text=clean_text(node), dom_path=dom_path(node,root), dom_id=node.get('id'), image_ids=[], relationship_indexes=[]))
    sections = {s['id']:s for s in page['sections']}
    seen_links = {}
    for e in root.select('a,button,[role="button"],[role="tab"],area'):
        target = e.get('href') or e.get('data-href') or e.get('data-url') or e.get('data-link')
        dest = urljoin(raw['url'], target) if target and not target.lower().startswith(('javascript:','data:')) else None
        handler = e.get('onclick')
        if not dest and handler:
            match = re.search(r"(?:location(?:\.href)?\s*=|window\.open\s*\()\s*['\"]([^'\"]+)", handler)
            if match: dest = urljoin(raw['url'], match.group(1))
        label = clean_text(e) or e.get('alt') or e.get('aria-label') or e.get('title') or ' '.join(i.get('alt','') for i in e.select('img'))
        key = (e.name,label,dest,target or handler)
        if key not in seen_links:
            rel = dict(source_url=url,label=label,element=e.name,destination_url=dest,
                       destination_type='same_page_anchor' if target and target.startswith('#') else destination_type(dest, raw['url']),
                       status='declared_in_html' if dest else 'unverified')
            if target or handler: rel['raw_target'] = target or handler
            seen_links[key] = len(page['relationships']);page['relationships'].append(rel)
        sid = section_of.get(id(e))
        if sid and seen_links[key] not in sections[sid]['relationship_indexes']:
            sections[sid]['relationship_indexes'].append(seen_links[key])
    assets = {}
    for e in [root, *root.find_all(True)]:
        urls = []; alternates=[]
        if e.name == 'img':
            candidates = [e.get(attr) for attr in ['src','data-src','data-original','data-lazy-src'] if e.get(attr)]
            for attr in ['srcset','data-srcset']:
                candidates.extend(p.strip().split()[0] for p in e.get(attr,'').split(',') if p.strip())
            candidates=[urljoin(raw['url'],u) for u in candidates if not u.startswith(('data:','blob:'))]
            if candidates:urls=[candidates[0]];alternates=list(dict.fromkeys(candidates[1:]))
        urls.extend(re.findall(r'url\([\'\"]?([^\)\'\"]+)', e.get('style','')))
        for image_url in dict.fromkeys(urls):
            image_url=urljoin(raw['url'],image_url)
            if not image_url.startswith(('https://','http://')): continue
            alt=e.get('alt','');sid=section_of.get(id(e));parent_link=e.find_parent('a')
            role=sections[sid]['role'] if sid else None
            if parent_link and destination_type(urljoin(raw['url'],parent_link.get('href',''))) == 'product_detail':
                tag,evidence='product_photo','product_link'
            elif re.search(r'/Prod_Img/|/product/|/goods/', image_url,re.I):
                tag,evidence='product_photo','asset_filename'
            elif re.search(r'button|btn_|icon|arrow|shadow|close|logo|scroll',image_url,re.I):
                tag,evidence='ui_asset','asset_filename'
            elif re.search(r'쿠폰|coupon|혜택|유의사항|notice',alt,re.I):
                tag,evidence='event_information','alt_text'
            elif role in ('brand_story','lookbook'):
                tag,evidence='editorial_image','section_context'
            elif role in ('hero','related_promotions'):
                tag,evidence='promotion_banner','section_context'
            elif role in ('benefit_overview','coupon_offer','participation_event','terms'):
                tag,evidence='event_information','section_context'
            else:tag,evidence='unknown','insufficient_evidence'
            if image_url not in assets:
                aid=f'i{len(assets)+1:04d}'
                assets[image_url]=dict(id=aid,url=image_url,alt=alt,tags=[tag],tag_evidence=[evidence],section_ids=[],alternate_urls=[])
            asset=assets[image_url]
            if tag not in asset['tags']:asset['tags'].append(tag)
            if evidence not in asset['tag_evidence']:asset['tag_evidence'].append(evidence)
            for alternate in alternates:
                if alternate!=image_url and alternate not in asset['alternate_urls']:asset['alternate_urls'].append(alternate)
            if sid and sid not in asset['section_ids']:asset['section_ids'].append(sid)
            if sid and asset['id'] not in sections[sid]['image_ids']:sections[sid]['image_ids'].append(asset['id'])
            if e.name=='img':page['images'].append(dict(alt=alt,url=image_url,tags=asset['tags'],image_id=asset['id']))
    page['image_assets']=list(assets.values())
    page['capture_method']='Browser-rendered public DOM; promotion root selected, scripts/trackers and hidden form values removed. Initial rendered state only; image pixels, other tabs, product bodies and live click destinations not collected.'
    for node in [root, *root.find_all(True)]:
        for key in list(node.attrs):
            if key.lower().startswith('on'): del node.attrs[key]
    html=str(root)
    page['html_file']=f'pages/{pid}.html'
    return page, html

def main():
    snapshots, targets_file, dst = map(Path, sys.argv[1:])
    targets=json.loads(targets_file.read_text()); brands=json.loads((dst/'brands.json').read_text())
    rows=[json.loads(line) for line in (dst/'index.jsonl').read_text().splitlines()]
    existing={r['id'] for r in rows}; prepared=[]
    for brand,urls in targets.items():
        pages=[]
        for number,url in enumerate(urls,1):
            pid=f'{brand}-{number:03d}'
            if pid in existing or (dst/'pages'/f'{pid}.json').exists():raise ValueError(f'Refusing to overwrite {pid}')
            raw=json.loads((snapshots/f'{pid}.json').read_text())
            page,html=build(raw,brand,pid,url);prepared.append((page,html));pages.append(page)
            resolved=page['resolved_url']; parsed=urlsplit(resolved)
            rows.append(dict(id=pid,brand=brand,url=url,resolved_url=resolved,host=parsed.netloc,
                path_hint='/'.join(parsed.path.strip('/').split('/')[:2]),title=page['listing_label'],page_title=page['title'],
                status=page['status'],collected_date=DATE,meta_file=f'pages/{pid}.json',html_file=page['html_file'],
                html_bytes=len(html.encode()),n_sections=len(page['sections']),n_images=len(page['image_assets'])))
        brands[brand]=dict(collected_date=DATE,timezone='Asia/Seoul',source_url=urls[0],source_urls=urls,
            scope='Only the user-supplied promotion URLs; no listing expansion or product detail collection.',
            html_type='Rendered promotion body DOM (scripts, trackers and hidden form values removed)',
            counts={s:sum(p['status']==s for p in pages) for s in ['captured','app_handoff','body_unavailable']},
            relationship_collection={'date':DATE,'source':'Rendered DOM; no live click verification',
                'counts_by_status':dict(Counter(r['status'] for p in pages for r in p['relationships']))},
            section_collection={'method':'Automatic inference from archived rendered HTML, authored modules, headings and local context. Nested wrapper boundaries are traversed; DOM order may differ from visual layout.',
                'image_method':'HTML img/lazy attributes, srcset and inline CSS URLs; image pixels and embedded text not inspected. External CSS backgrounds may not be included.',
                'section_count':sum(len(p['sections']) for p in pages),
                'page_counts':dict(Counter(p['section_status'] for p in pages)),
                'image_asset_count':sum(len(p['image_assets']) for p in pages),
                'image_tag_counts':dict(Counter(t for p in pages for a in p['image_assets'] for t in a['tags'])),
                'relationship_indexes':'Zero-based indexes into the page relationships array.',
                'dom_path':'One-based element indexes from the archived HTML fragment root.'})
    for page,html in prepared:
        (dst/'pages'/f"{page['id']}.json").write_text(json.dumps(page,ensure_ascii=False,indent=1))
        if html:(dst/'pages'/f"{page['id']}.html").write_text(html)
    (dst/'brands.json').write_text(json.dumps(brands,ensure_ascii=False,indent=1))
    (dst/'index.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    print(json.dumps({'total':len(rows),'added':len(prepared),'statuses':dict(Counter(p['status'] for p,h in prepared))}))

if __name__=='__main__': main()
