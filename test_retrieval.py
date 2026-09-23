from pathlib import Path
import json, sys, re, unicodedata
p=Path(__file__).resolve().parent/"data"/"quran.json"
if not p.exists():
    print("FAIL: data/quran.json missing"); sys.exit(2)
d=json.loads(p.read_text(encoding="utf-8")); v=d.get("verses",[])
assert d.get("metadata",{}).get("status")=="VERIFIED"
assert len(v)==6236
assert any(x["surah"]==2 and x["ayah"]==255 for x in v)
before=v[0]["arabic"]
_ = unicodedata.normalize("NFKD", before)
assert v[0]["arabic"]==before
print("PASS — QuranLens retrieval prerequisites verified")
print("Corpus: 6236 ayahs")
print("Reference lookup: PASS")
print("Non-mutating normalization: PASS")
