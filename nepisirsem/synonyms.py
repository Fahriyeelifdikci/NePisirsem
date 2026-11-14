"""Aynı malzemenin farklı adlarını tek bir 'kanonik' ada indirger.

Kaynak: experiments/top_ingredients.py çıktısı (en sık 150 malzeme).
Tartışmalı çiftler bilerek ayrı tutuldu (ör. salça ≠ domates salçası, kuru maya ≠ instant maya).
"""

# varyant → kanonik ad (kanonik ad: kullanıcının arayacağı, genelde en sık ya da en sade olan)
SYNONYMS = {
    # yazım farkları
    "tereyağ": "tereyağı",
    "zeytinyağ": "zeytinyağı",
    "sıvıyağ": "sıvı yağ",
    "limonun suyu": "limon suyu",
    "toz kırmızı biber": "kırmızı toz biber",
    # aynı şeyin iki adı
    "yumurta beyazı": "yumurta akı",
    "labne peyniri": "labne",
    "ceviz içi": "ceviz",
    "kuru soğan": "soğan",
    "toz şeker": "şeker",
    "sıvı krema": "krema",
    # kullanıcı kararıyla eşlenenler
    "vanilin": "vanilya",
    "ayçiçek yağı": "sıvı yağ",
    "yumurt sarısı": "yumurta sarısı",           # veride yazım hatası
}


def canonical(name):
    """Malzeme adını kanonik hâline çevirir; sözlükte yoksa olduğu gibi bırakır.
    "tereyağ" → "tereyağı",  "un" → "un"
    """
    return SYNONYMS.get(name, name)