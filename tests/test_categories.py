import pytest
from nepisirsem.categories import categorize


@pytest.mark.parametrize("title, ingredients, expected", [
    # eskiden yanlış olanlar
    ("Mercimek Köftesi", ["kırmızı mercimek", "ince bulgur", "soğan"], "meze"),
    ("Çiğ Köfte", ["ince bulgur", "isot", "domates salçası"], "meze"),
    ("Tavuk Göğsü", ["süt", "tavuk göğsü", "şeker", "pirinç unu"], "tatli"),
    ("Etli Kuru Fasulye", ["kuru fasulye", "kuşbaşı dana eti", "soğan"], "et"),
    ("Patates Köftesi", ["patates", "yumurta", "un"], "sebze"),
    # doğru çalışanlar bozulmasın
    ("İzmir Köfte", ["kıyma", "patates", "domates"], "et"),
    ("Kekikli Tavuk", ["tavuk but", "kekik"], "tavuk"),
    ("Fırında Tavuk Göğsü", ["tavuk göğsü", "yoğurt", "salça"], "tavuk"),
    ("Mercimek Çorbası", ["kırmızı mercimek", "soğan"], "corba"),
    ("Fırında Sütlaç", ["süt", "pirinç", "şeker"], "tatli"),
])
def test_categorize(title, ingredients, expected):
    assert categorize(title, ingredients)[0] == expected


def test_malzeme_bilinmiyorsa_sadece_basliga_bakar():
    assert categorize("Patates Köftesi")[0] == "et"