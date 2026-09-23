QuranLens v0.3 — Universal Search

Copy these files into:
C:\QuranLens

Replace index.html and START_QURANLENS.bat if asked.
DO NOT replace or delete C:\QuranLens\data\quran.json.

Then run:

cd C:\QuranLens
python .\install_translation.py
python .\test_v03.py
.\START_QURANLENS.bat

Search examples:
water
rain
ماء
يوم القيامة
2:25

Behavior:
- verse reference is auto-detected
- Arabic is auto-detected
- English searches the local Pickthall translation
- references are clickable
- Arabic corpus remains separate and unchanged
