import pytest
from nepisirsem.matching import has, missing, uses_all


# ---------- has ----------

@pytest.mark.parametrize("ingredient, available, expected", [
    ("kıyma", {"kıyma"}, True),
    ("yağlı kıyma", {"kıyma"}, True),
    ("beyaz peynir", {"peynir"}, True),
    # eskiden xfail olanlar
    ("kaşar peyniri", {"peynir"}, True),
    ("pul biber", {"biber"}, False),
    # genel ↔ tür
    ("peynir", {"kaşar peyniri"}, True),
    ("biber", {"kapya biber"}, True),
    ("biber", {"pul biber"}, False),
    ("kırmızı toz biber", {"biber"}, False),
    # bilinçli olarak eşleşmeyenler
    ("limon suyu", {"su"}, False),
    ("mısır unu", {"un"}, False),
    ("peynir", {"labne"}, False),
])
def test_has(ingredient, available, expected):
    assert has(ingredient, available) == expected

# ---------- missing ----------

def test_missing_pantry_sadece_secilenleri_sayar():
    """Pantry dürüstlüğü: şeker işaretlenmediyse eksik görünmeli."""
    assert missing(["un", "şeker", "tuz"], {"un"}, pantry=("tuz",)) == ["şeker"]


def test_missing_pantry_bossa_her_sey_sayilir():
    assert missing(["un", "tuz"], {"un"}) == ["tuz"]


def test_missing_turetilmis_malzemeler():
    """Yumurtası olanın yumurta sarısı da vardır."""
    assert missing(["yumurta sarısı", "un"], {"yumurta", "un"}) == []


# ---------- uses_all ----------

def test_uses_all():
    assert uses_all(["un", "yumurta sarısı"], {"un", "yumurta"})
    assert not uses_all(["un"], {"un", "yumurta"})