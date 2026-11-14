import pytest
from nepisirsem.synonyms import SYNONYMS, canonical


@pytest.mark.parametrize("name, expected", [
    ("tereyağ", "tereyağı"),
    ("kuru soğan", "soğan"),
    ("vanilin", "vanilya"),
    ("ayçiçek yağı", "sıvı yağ"),
    ("yumurt sarısı", "yumurta sarısı"),
])
def test_varyant_kanonik_ada_doner(name, expected):
    assert canonical(name) == expected


@pytest.mark.parametrize("name", ["un", "tereyağı", "salça", "kuru maya", "yaş maya"])
def test_sozlukte_olmayan_ad_degismez(name):
    assert canonical(name) == name


def test_zincir_yok():
    """Kanonik adlar kendileri varyant olmamalı: a→b, b→c gibi zincirler yasak."""
    zincirler = [v for v in SYNONYMS.values() if v in SYNONYMS]
    assert zincirler == []