# QuranLens v0.1

## Install the complete Arabic corpus

On a computer with Python 3 and internet access:

    python install_corpus.py

Then verify at any time:

    python verify_corpus.py

Successful installation creates:

- data/tanzil-uthmani-v1.1.txt — original downloaded source
- data/quran.json — QuranLens structured corpus
- data/verification-report.json — integrity report

The application remains blocked from Qur'an-only reasoning unless
`data/quran.json` has `metadata.status = VERIFIED`.

## Why the corpus is not silently bundled
QuranLens records source provenance and verifies the exact copy installed.
The installer fetches the corpus directly from the recorded Tanzil endpoint
instead of scraping arbitrary search results.

See `CORPUS_PROVENANCE.md` and `EVIDENCE_RULES.txt`.
