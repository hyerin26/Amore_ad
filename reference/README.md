# reference parser

Converts per-brand promotion dumps (`<brand>_promotions.json`, each with a `pages` array) into one flat, brand-tagged reference index.

```bash
python3 reference/build_reference_index.py <dir with *_promotions.json> <output dir>
```

Output:

- `index.jsonl` - one line per page (id, brand, url, title, status, file paths, sizes)
- `brands.json` - per-brand collection metadata
- `pages/<brand>-NNN.json` - page record without html
- `pages/<brand>-NNN.html` - rendered promotion body DOM

Source data is not committed here.
