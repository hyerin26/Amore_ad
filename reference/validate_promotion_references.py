"""Validate authored section coverage, DOM paths and reference integrity.

Usage: python reference/validate_promotion_references.py
Requires beautifulsoup4. Checks the URL manifest added on 2026-11-08.
"""
import json
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from section_inference import text

BASE=Path(__file__).parent

def validate(data=BASE/'data'):
    targets=json.loads((BASE/'promotion_urls_20261108.json').read_text())
    rows=[json.loads(line) for line in (data/'index.jsonl').read_text().splitlines()]
    index={r['id']:r for r in rows}
    assert len(index)==len(rows), 'Duplicate page IDs'
    brands=json.loads((data/'brands.json').read_text())
    total=0
    for brand,urls in targets.items():
        pages=[]
        for number,url in enumerate(urls,1):
            pid=f'{brand}-{number:03d}';row=index[pid]
            page=json.loads((data/row['meta_file']).read_text());pages.append(page)
            assert page['url']==row['url']==url, pid
            assert page['status']==row['status'],pid
            sections=page['sections'];assets={a['id']:a for a in page['image_assets']}
            assert len(assets)==len(page['image_assets'])==row['n_images'],pid
            assert len(sections)==row['n_sections'],pid
            if page['status']=='body_unavailable':
                assert not sections and not assets and not page['html_file'] and not row['html_bytes'],pid
                continue
            assert len(sections)>1, f'{pid}: whole-body fallback regression'
            html=(data/page['html_file']).read_text()
            assert len(html.encode())==row['html_bytes'],pid
            soup=BeautifulSoup(html,'html.parser');root=soup.find()
            assert not soup.select('script,iframe,input[type="hidden"]'),pid
            assert all(not k.lower().startswith('on') for e in soup.find_all(True) for k in e.attrs),pid
            assert text(root)==page['text'],pid
            assert ' '.join(s['text'] for s in sections if s['text'])==page['text'], f'{pid}: dropped or duplicated text'
            assigned=set(); paths=[]; image_sections={aid:set() for aid in assets}
            for number,section in enumerate(sections,1):
                assert section['id']==f's{number:02d}' and section['order']==number,pid
                path=section['dom_path'];assert path[0]==1,pid
                node=root
                for offset in path[1:]:node=[c for c in node.children if isinstance(c,Tag)][offset-1]
                assert node.get('id')==section['dom_id'] and text(node)==section['text'],f'{pid}: invalid DOM path'
                assert all(not (path[:len(p)]==p or p[:len(path)]==path) for p in paths),f'{pid}: overlapping sections'
                paths.append(path)
                assert len(section['image_ids'])==len(set(section['image_ids'])),pid
                for aid in section['image_ids']:
                    assert aid in assets,pid
                    image_sections[aid].add(section['id'])
                for i in section['relationship_indexes']:
                    assert 0<=i<len(page['relationships']),pid
                    assigned.add(i)
            assert assigned==set(range(len(page['relationships']))),f'{pid}: unassigned relationship'
            for aid,asset in assets.items():
                assert image_sections[aid]==set(asset['section_ids']) and image_sections[aid],f'{pid}: asymmetric image mapping'
                assert asset['tag_evidence'],pid
            for image in page['images']:
                assert image['image_id'] in assets and image['tags']==assets[image['image_id']]['tags'],pid
            for rel in page['relationships']:
                assert rel['status'] in ('declared_in_html','unverified'),pid
                assert rel['destination_type'] in ('product_detail','promotion','other_store_page','external_page','external_action','unknown','same_page_anchor','cart_or_checkout','login'),pid
            total+=len(sections)
        meta=brands[brand]
        assert meta['section_collection']['section_count']==sum(len(p['sections']) for p in pages),brand
        assert meta['section_collection']['image_asset_count']==sum(len(p['image_assets']) for p in pages),brand
        assert meta['relationship_collection']['counts_by_status']==dict(Counter(r['status'] for p in pages for r in p['relationships'])),brand
    print(f'PASS: {sum(map(len,targets.values()))} requested URLs, {total} sections; DOM paths, complete text coverage, reciprocal image links and relationship indexes valid.')

if __name__=='__main__':validate()
