import pytest
from nepisirsem.recipe_parser import to_number, parse_ingredient, clean_name


# ---------- to_number ----------

@pytest.mark.parametrize("text, expected", [
    ("1", 1.0),
    ("1,5", 1.5),
    ("1.5", 1.5),
    ("1/2", 0.5),
    ("2-3", 2.5),
    ("Yarım", 0.5),
    ("¾", 0.75),
])
def test_to_number_gecerli_girdiler(text, expected):
    assert to_number(text) == expected


@pytest.mark.parametrize("text", ["1/2/3", "-", ".", "1/0", "1-2-3", "1-."])

def test_to_number_bozuk_girdide_none_doner(text):
    assert to_number(text) is None


# ---------- parse_ingredient ----------

@pytest.mark.parametrize("line, expected", [
    ("100gramtereyağı", (100.0, "gram", "tereyağı")),
    ("1,5su bardağıun", (1.5, "su bardağı", "un")),
    ("2-3 adet yumurta", (2.5, "adet", "yumurta")),
    ("Yarımadetkabak", (0.5, "adet", "kabak")),
    ("tuz", (None, None, "tuz")),
    ("300gr.kıyma", (300.0, "gr.", "kıyma")),
    ("1 greyfurt", (1.0, None, "greyfurt")),
    ("yarım adet limon", (0.5, "adet", "limon")),
    ("çeyrek demet maydanoz", (0.25, "demet", "maydanoz")),
    ("Çeyrekdemetdereotu", (0.25, "demet", "dereotu")),
    ("2 tepeleme yemek kaşığıun", (2.0, "yemek kaşığı", "un")),
    ("1 büyük su bardağı süt", (1.0, "su bardağı", "süt")),
])
def test_parse_ingredient(line, expected):
    assert parse_ingredient(line) == expected

    

# ---------- clean_name ----------

@pytest.mark.parametrize("raw, expected", [
    ("İzmir tulum peyniri(rendelenmiş)", "izmir tulum peyniri"),
    ("(10 gram) kabartma tozu", "kabartma tozu"),
    ("küçük boy haşlanmış patates", "patates"),
    ("orta boysoğan", "soğan"),
    ("büyük boykuru soğan", "kuru soğan"),
    ("oda sıcaklığında tereyağı", "tereyağı"),
    ("boyoz", "boyoz"),
    ("kaynar su", "su"),
    ("tereyağı veya margarin", "tereyağı"),
    ("Margarin(veya tereyağı)", "margarin"),
    ("ortanca", "ortanca"),])
def test_clean_name(raw, expected):
    assert clean_name(raw) == expected


def test_buyuk_boy_tam_temizlenir():
    """Ayrıştırma + temizleme birlikte: '2 büyük boy patates' → 'patates'"""
    _, _, name = parse_ingredient("2 büyük boy patates")
    assert clean_name(name) == "patates"