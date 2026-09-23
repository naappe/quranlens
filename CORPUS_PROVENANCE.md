# QuranLens Corpus Provenance

## Authoritative display corpus
- Source: Tanzil Project
- Text type: Uthmani
- Version: 1.1
- Release: February 2021
- Source page: https://tanzil.net/download/
- Updates: https://tanzil.net/updates/
- License: Creative Commons Attribution 3.0, subject to Tanzil's text terms.

Tanzil states that its Quran text is produced through automatic comparison,
rule-based verification, and manual verification against the Medina Mushaf.

## QuranLens trust policy
`VERIFIED` inside QuranLens has a narrow technical meaning:

1. The corpus was downloaded from the recorded source URL.
2. Exactly 114 surahs are present.
3. Exactly 6,236 ayahs are present.
4. Every expected surah:ayah key exists once.
5. Every surah has the expected number of ayahs.
6. The downloaded bytes and canonical verse stream receive SHA-256 hashes.
7. The authoritative Arabic display text is not normalized, rewritten, stemmed,
   stripped of marks, or otherwise modified.

It does NOT mean QuranLens independently certifies a religious text. Source
provenance remains visible at all times.

## Search data
Any future normalized Arabic, roots, lemmas, tokenization, embeddings, or
semantic indexes must live outside the `arabic` field. Derived search data
must never overwrite the source text.
