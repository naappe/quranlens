#!/usr/bin/env python3
"""
QuranLens corpus installer.

Downloads Tanzil Uthmani v1.1 directly from Tanzil, validates the structure,
preserves the Arabic text verbatim, records SHA-256 integrity metadata, and
builds QuranLens data/quran.json.

The script intentionally DOES NOT normalize or rewrite the authoritative Arabic
display text. Any future search normalization must be stored separately.
"""

from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

SOURCE_URL = (
    "https://tanzil.net/pub/download/index.php?"
    "quranType=uthmani&outType=txt-2&agree=true"
    "&marks=true&sajdah=true&rub=true&stanween=true"
)
SOURCE_NAME = "Tanzil Quran Text — Uthmani"
SOURCE_VERSION = "1.1"

SURAH_COUNTS = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def fetch() -> bytes:
    print("Downloading directly from Tanzil...")
    req = Request(
        SOURCE_URL,
        headers={"User-Agent": "QuranLens/0.1 corpus installer"}
    )
    with urlopen(req, timeout=45) as r:
        raw = r.read()
    if len(raw) < 500_000:
        raise RuntimeError(f"Downloaded file is unexpectedly small: {len(raw)} bytes")
    return raw

def parse_tanzil(raw: bytes):
    text = raw.decode("utf-8-sig")
    verses = []
    license_lines = []
    seen = set()

    for original_line in text.splitlines():
        line = original_line.rstrip("\r\n")
        if not line:
            continue

        # txt-2 format: surah|ayah|Arabic text
        m = re.match(r"^(\d{1,3})\|(\d{1,3})\|(.*)$", line)
        if m:
            s, a, arabic = int(m.group(1)), int(m.group(2)), m.group(3)

            if not (1 <= s <= 114):
                raise ValueError(f"Invalid surah number: {s}")
            if not (1 <= a <= SURAH_COUNTS[s-1]):
                raise ValueError(f"Invalid ayah number: {s}:{a}")
            if not arabic.strip():
                raise ValueError(f"Empty Arabic text at {s}:{a}")
            if (s, a) in seen:
                raise ValueError(f"Duplicate verse: {s}:{a}")

            # Important: arabic is kept exactly as supplied.
            seen.add((s, a))
            verses.append({
                "surah": s,
                "ayah": a,
                "key": f"{s}:{a}",
                "arabic": arabic
            })
        elif line.startswith("#"):
            license_lines.append(line)

    return verses, "\n".join(license_lines).strip()

def verify_structure(verses):
    errors = []

    if len(verses) != 6236:
        errors.append(f"Expected 6236 ayahs; found {len(verses)}")

    actual = [0] * 114
    for v in verses:
        actual[v["surah"] - 1] += 1

    for i, (got, exp) in enumerate(zip(actual, SURAH_COUNTS), start=1):
        if got != exp:
            errors.append(f"Surah {i}: expected {exp}, found {got}")

    expected_keys = {
        f"{s}:{a}"
        for s, count in enumerate(SURAH_COUNTS, start=1)
        for a in range(1, count + 1)
    }
    actual_keys = {v["key"] for v in verses}

    missing = sorted(expected_keys - actual_keys)
    extra = sorted(actual_keys - expected_keys)

    if missing:
        errors.append(f"Missing verse keys: {missing[:10]}")
    if extra:
        errors.append(f"Unexpected verse keys: {extra[:10]}")

    # We do not alter Unicode composition. We merely report its form.
    non_nfc = [v["key"] for v in verses if unicodedata.normalize("NFC", v["arabic"]) != v["arabic"]]

    return errors, actual, non_nfc

def build():
    raw = fetch()
    source_hash = sha256_bytes(raw)

    source_path = DATA / "tanzil-uthmani-v1.1.txt"
    source_path.write_bytes(raw)

    verses, notice = parse_tanzil(raw)
    errors, counts, non_nfc = verify_structure(verses)

    if errors:
        print("\nCORPUS VERIFICATION FAILED")
        for e in errors:
            print(" -", e)
        sys.exit(2)

    canonical_stream = "\n".join(
        f'{v["surah"]}|{v["ayah"]}|{v["arabic"]}' for v in verses
    ).encode("utf-8")
    canonical_hash = sha256_bytes(canonical_stream)

    payload = {
        "metadata": {
            "status": "VERIFIED",
            "project_status_meaning": (
                "Downloaded from the recorded Tanzil source and passed QuranLens "
                "structural/integrity checks. This label does not claim independent "
                "scholarly certification by QuranLens."
            ),
            "source": SOURCE_NAME,
            "source_url": SOURCE_URL,
            "source_version": SOURCE_VERSION,
            "script": "Uthmani",
            "surah_count": 114,
            "ayah_count": 6236,
            "source_file_sha256": source_hash,
            "canonical_verse_stream_sha256": canonical_hash,
            "installed_utc": datetime.now(timezone.utc).isoformat(),
            "text_policy": "Arabic display text preserved verbatim from source.",
            "normalization_policy": "No normalization applied to authoritative display text.",
            "unicode_non_nfc_verse_count": len(non_nfc),
            "license_notice": notice,
            "attribution": "Tanzil Project — https://tanzil.net",
        },
        "surah_ayah_counts": counts,
        "verses": verses
    }

    out = DATA / "quran.json"
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    report = {
        "status": "PASS",
        "source": SOURCE_NAME,
        "version": SOURCE_VERSION,
        "surahs": 114,
        "ayahs": 6236,
        "source_file_sha256": source_hash,
        "canonical_verse_stream_sha256": canonical_hash,
        "duplicate_keys": 0,
        "missing_keys": 0,
        "per_surah_counts_match": True,
        "authoritative_text_modified": False,
        "unicode_non_nfc_verse_count": len(non_nfc)
    }
    (DATA / "verification-report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("\nQURANLENS CORPUS VERIFIED")
    print("Source:", SOURCE_NAME, SOURCE_VERSION)
    print("Surahs: 114")
    print("Ayahs:  6236")
    print("Source SHA-256:", source_hash)
    print("Canonical verse stream SHA-256:", canonical_hash)
    print("Saved:", out)

if __name__ == "__main__":
    build()
