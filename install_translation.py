#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
import json, hashlib, sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"; DATA.mkdir(exist_ok=True)
URL="https://api.alquran.cloud/v1/quran/en.pickthall"

print("Downloading English translation: Mohammed Marmaduke William Pickthall...")
req=Request(URL,headers={"User-Agent":"QuranLens/0.3 translation installer"})
with urlopen(req,timeout=60) as r:
    raw=r.read()

payload=json.loads(raw.decode("utf-8"))
data=payload.get("data") or {}
surahs=data.get("surahs") or []
verses=[]
for s in surahs:
    sn=s.get("number")
    for a in s.get("ayahs",[]):
        verses.append({
            "surah":sn,
            "ayah":a.get("numberInSurah"),
            "text":a.get("text","")
        })

if len(surahs)!=114:
    print("FAIL: expected 114 surahs, found",len(surahs)); sys.exit(2)
if len(verses)!=6236:
    print("FAIL: expected 6236 ayahs, found",len(verses)); sys.exit(2)

keys={(v["surah"],v["ayah"]) for v in verses}
if len(keys)!=6236:
    print("FAIL: duplicate or missing translation keys"); sys.exit(2)

out={
 "metadata":{
   "status":"INSTALLED",
   "language":"English",
   "translator":"Mohammed Marmaduke William Pickthall",
   "edition":"en.pickthall",
   "source":"Al Quran Cloud API",
   "source_url":URL,
   "ayah_count":6236,
   "surah_count":114,
   "download_sha256":hashlib.sha256(raw).hexdigest(),
   "installed_utc":datetime.now(timezone.utc).isoformat(),
   "role":"Reading/search layer only; not authoritative Arabic evidence."
 },
 "verses":verses
}
path=DATA/"translation_en_pickthall.json"
path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

print("PASS — English translation installed")
print("Translator: Mohammed Marmaduke William Pickthall")
print("114 surahs / 6236 ayahs")
print("Saved:",path)
print("SHA-256:",out["metadata"]["download_sha256"])
