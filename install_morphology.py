from pathlib import Path
import json, re, hashlib, sys

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"
SRC=DATA/"quranic-corpus-morphology-0.4.txt"
OUT=DATA/"morphology_qac_v04.json"

if not SRC.exists():
    print("MISSING — official Quranic Arabic Corpus morphology file")
    print("Download Version 0.4 from: https://corpus.quran.com/download/")
    print("Save the unmodified file as:")
    print(SRC)
    sys.exit(2)

raw=SRC.read_bytes()
text=raw.decode("utf-8-sig")
rows=[]
pat=re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)\s+(\S+)\s+(\S+)\s+(.+)$")
for line in text.splitlines():
    m=pat.match(line.strip())
    if not m: continue
    s,a,w,seg=map(int,m.group(1,2,3,4))
    form,tag,features=m.group(5),m.group(6),m.group(7)
    lemma=root=None
    for f in features.split("|"):
        if f.startswith("LEM:"): lemma=f[4:]
        elif f.startswith("ROOT:"): root=f[5:]
    rows.append({"s":s,"a":a,"w":w,"seg":seg,"form":form,"tag":tag,"lemma":lemma,"root":root,"features":features})

if len(rows) < 120000:
    raise SystemExit(f"FAIL — expected full QAC morphology; parsed only {len(rows)} segment rows")
if not any(r["s"]==1 and r["a"]==1 and r["w"]==1 for r in rows):
    raise SystemExit("FAIL — QAC location structure not recognized")

payload={
 "metadata":{
   "source":"Quranic Arabic Corpus",
   "version":"0.4",
   "source_url":"https://corpus.quran.com/download/",
   "license":"GNU General Public License",
   "copyright":"Copyright (C) 2011 Kais Dukes",
   "attribution":"Quranic Arabic Corpus (Version 0.4) — corpus.quran.com",
   "source_sha256":hashlib.sha256(raw).hexdigest(),
   "segment_rows":len(rows),
   "status":"DERIVED_FROM_OFFICIAL_QAC_SOURCE",
   "note":"Morphology is a separate annotation layer. It does not modify QuranLens verified Arabic."
 },
 "segments":rows
}
OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print("PASS — Quranic Arabic Corpus morphology indexed")
print("Segments:",len(rows))
print("Source SHA-256:",payload["metadata"]["source_sha256"])
print("Saved:",OUT)
