#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parent
path = ROOT / "data" / "quran.json"

COUNTS = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

if not path.exists():
    print("FAIL: data/quran.json not found. Run install_corpus.py first.")
    sys.exit(2)

d = json.loads(path.read_text(encoding="utf-8"))
v = d.get("verses", [])
meta = d.get("metadata", {})

errors = []
if meta.get("status") != "VERIFIED":
    errors.append("metadata.status is not VERIFIED")
if len(v) != 6236:
    errors.append(f"expected 6236 ayahs, found {len(v)}")

seen = set()
actual = [0]*114
for x in v:
    key = (x.get("surah"), x.get("ayah"))
    if key in seen:
        errors.append(f"duplicate {key}")
    seen.add(key)
    s = x.get("surah")
    if isinstance(s, int) and 1 <= s <= 114:
        actual[s-1] += 1

if actual != COUNTS:
    errors.append("per-surah ayah counts do not match")

stream = "\n".join(f'{x["surah"]}|{x["ayah"]}|{x["arabic"]}' for x in v).encode("utf-8")
digest = hashlib.sha256(stream).hexdigest()
if digest != meta.get("canonical_verse_stream_sha256"):
    errors.append("canonical verse stream SHA-256 mismatch")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS — QuranLens corpus integrity verified")
print("114 surahs / 6236 ayahs")
print("SHA-256:", digest)
