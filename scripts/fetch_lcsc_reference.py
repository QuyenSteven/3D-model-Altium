#!/usr/bin/env python3
import json
import sys
import urllib.request
from pathlib import Path

LCSC_ID = sys.argv[1] if len(sys.argv) > 1 else "C5379868"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("reference_models/VH3.96") / f"{LCSC_ID}.step"

API = f"https://easyeda.com/api/products/{LCSC_ID}/components?version=6.4.19.5"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

raw = get(API)
payload = json.loads(raw.decode("utf-8"))
result = payload.get("result", payload)

# LCSC/EasyEDA can return either one component object or a list.
if isinstance(result, list):
    candidates = result
else:
    candidates = [result]

model = None
component = None
for item in candidates:
    if not isinstance(item, dict):
        continue
    shapes = (((item.get("packageDetail") or {}).get("dataStr") or {}).get("shape") or [])
    for line in shapes:
        if not isinstance(line, str) or not line.startswith("SVGNODE~"):
            continue
        try:
            attrs = json.loads(line.split("~", 2)[1]).get("attrs", {})
        except Exception:
            continue
        if attrs.get("uuid"):
            model = attrs
            component = item
            break
    if model:
        break

if not model:
    raise SystemExit(f"No EasyEDA 3D SVGNODE found for {LCSC_ID}")

uuid = model["uuid"]
title = model.get("title", "")
step_url = f"https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/{uuid}"
step = get(step_url)

if not step.startswith(b"ISO-10303-21"):
    raise SystemExit(f"Downloaded payload is not STEP for UUID {uuid}; first bytes={step[:64]!r}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(step)

meta = {
    "lcsc_id": LCSC_ID,
    "uuid": uuid,
    "title": title,
    "source_api": API,
    "source_step": step_url,
    "easyeda_transform": {
        "origin": model.get("c_origin"),
        "rotation": model.get("c_rotation"),
        "z": model.get("z"),
    },
    "package_title": ((component or {}).get("packageDetail") or {}).get("title"),
}
OUT.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(meta, indent=2, ensure_ascii=False))
print(f"Wrote {OUT} ({len(step)} bytes)")
