import pytest
from nepisirsem.categories import categorize
import numpy as np


@pytest.mark.parametrize("title, ingredients, expected", [
    # eskiden yanlış olanlar
    ("Mercimek Köftesi", ["kırmızı mercimek", "ince bulgur", "soğan"], "meze"),
    ("Çiğ Köfte", ["ince bulgur", "isot", "domates salçası"], "meze"),
    ("Tavuk Göğsü", ["süt", "tavuk göğsü", "şeker", "pirinç unu"], "tatli"),
    ("Etli Kuru Fasulye", ["kuru fasulye", "kuşbaşı dana eti", "soğan"], "et"),
    ("Patates Köftesi", ["patates", "yumurta", "un"], "sebze"),
    # "Diğer" analizinden gelenler (experiments/inspect_other.py)
    ("Çikolatalı Enerji Topları", ["hurma", "kakao", "ceviz"], "tatli"),
    ("Yulaf Lapası", ["yulaf", "süt", "muz"], "meze"),
    ("Fırın Falafel", ["nohut", "maydanoz", "kimyon"], "meze"),
    ("Mantar Sote", ["mantar", "tereyağı", "soğan"], "sebze"),
    ("Izgara Hindi Göğüs", ["hindi göğüs", "zeytinyağı"], "tavuk"),
    ("Portakallı Cheescake", ["labne", "bisküvi", "portakal"], "pasta"),
    ("Susamlı Kahvaltı Simidi", ["un", "susam", "pekmez"], "borek"),
    # doğru çalışanlar bozulmasın
    ("Tavuk Sote", ["tavuk göğsü", "biber", "domates"], "tavuk"),
    ("Havuçlu Kek", ["havuç", "un", "yumurta"], "kek"),
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



def test_malzemeler_numpy_dizisi_olarak_gelince_calisir():
    """Parquet'ten okunan malzeme listeleri Python listesi değil, numpy dizisidir."""
    ingredients = np.array(["süt", "tavuk göğsü", "şeker"], dtype=object)
    assert categorize("Tavuk Göğsü", ingredients)[0] == "tatli"