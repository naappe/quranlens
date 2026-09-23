from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent
q=ROOT/"data"/"quran.json"
t=ROOT/"data"/"translation_en_pickthall.json"
if not q.exists():
    print("FAIL: Arabic corpus missing");sys.exit(2)
qd=json.loads(q.read_text(encoding="utf-8"))
assert qd.get("metadata",{}).get("status")=="VERIFIED"
assert len(qd.get("verses",[]))==6236
print("Arabic corpus: PASS — 6236 ayahs")
if not t.exists():
    print("Translation: NOT INSTALLED")
    print("Run: python .\\install_translation.py")
    sys.exit(0)
td=json.loads(t.read_text(encoding="utf-8"))
assert len(td.get("verses",[]))==6236
assert len({(v["surah"],v["ayah"]) for v in td["verses"]})==6236
print("Translation: PASS — 6236 ayahs")
print("Universal search prerequisites: PASS")
