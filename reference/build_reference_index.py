"""reference_json/*_promotions.json -> one flat reference index.
reference_index/
  index.jsonl   one line per page (DB-ready: id, brand, url, title, status, files, sizes)
  brands.json   per-brand collection metadata (scope, counts, methods)
  pages/<id>.json   page record without html (brand tag included)
  pages/<id>.html   rendered promotion body DOM
"""
import json, re, sys, pathlib
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
(dst / "pages").mkdir(parents=True, exist_ok=True)
brands, rows = {}, []
for f in sorted(src.glob("*_promotions.json")):
    brand = f.name.replace("_promotions.json", "")
    d = json.load(open(f, encoding="utf-8"))
    brands[brand] = {k: v for k, v in d.items() if k != "pages"}
    for i, p in enumerate(d["pages"], 1):
        pid = f"{brand}-{i:03d}"
        html = p.get("html") or ""
        url = p.get("resolved_url") or p["url"]
        path = re.sub(r"^https?://[^/]+/?", "", url.split("#")[0].split("?")[0]).strip("/").split("/")
        rec = {"id": pid, "brand": brand, "collected_date": d.get("collected_date"),
               **{k: v for k, v in p.items() if k != "html"},
               "html_file": f"pages/{pid}.html" if html else None}
        (dst / "pages" / f"{pid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        if html: (dst / "pages" / f"{pid}.html").write_text(html, encoding="utf-8")
        rows.append({"id": pid, "brand": brand, "url": p["url"], "resolved_url": p.get("resolved_url"),
                     "host": re.sub(r"^https?://([^/]+).*", r"\1", url), "path_hint": "/".join(path[:2]),
                     "title": p.get("listing_label"), "page_title": p.get("title"),
                     "status": p.get("status"), "collected_date": d.get("collected_date"),
                     "meta_file": f"pages/{pid}.json", "html_file": rec["html_file"],
                     "html_bytes": len(html.encode()), "n_sections": len(p.get("sections") or []),
                     "n_images": len(p.get("image_assets") or [])})
(dst / "brands.json").write_text(json.dumps(brands, ensure_ascii=False, indent=1), encoding="utf-8")
with open(dst / "index.jsonl", "w", encoding="utf-8") as fh:
    for r in rows: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "pages", {b: sum(r["brand"] == b for r in rows) for b in brands})
