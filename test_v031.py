from pathlib import Path
import json
R=Path(__file__).resolve().parent
q=json.loads((R/"data"/"quran.json").read_text(encoding="utf-8"))
t=json.loads((R/"data"/"translation_en_pickthall.json").read_text(encoding="utf-8"))
assert q["metadata"]["status"]=="VERIFIED"
assert len(q["verses"])==6236 and len(t["verses"])==6236
assert sum(x["surah"]==2 for x in q["verses"])==286
assert any(x["surah"]==2 and x["ayah"]==22 for x in q["verses"])
print("PASS — QuranLens v0.3.1")
print("Arabic corpus: PASS — 6236")
print("English translation: PASS — 6236")
print("Surah 2 navigation data: PASS — 286 ayahs")
print("2:22 target: PASS")
