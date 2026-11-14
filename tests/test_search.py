"""Arama motorunun mantığını gerçek BERT modeli olmadan test eder."""
import numpy as np
import pandas as pd
import pytest
from nepisirsem.search import RecipeSearch


class FakeModel:
    """Gerçek model yerine: her sorguya aynı vektörü döndürür."""

    def encode(self, text, normalize_embeddings=True):
        return np.array([1.0, 0.0], dtype=np.float32)


@pytest.fixture
def engine():
    """3 tariflik minik bir arama motoru. Benzerlik puanları: kek 0.9, omlet 0.5, pilav 0.1"""
    df = pd.DataFrame({
        "title": ["Kek", "Omlet", "Pilav"],
        "ingredients": [["un", "yumurta", "şeker"], ["yumurta", "tuz"], ["pirinç", "su", "tereyağı"]],
    })
    vectors = np.array([[0.9, 0.1], [0.5, 0.5], [0.1, 0.9]], dtype=np.float32)
    return RecipeSearch(df, vectors, FakeModel())


def test_sonuclar_benzerlige_gore_sirali(engine):
    results = engine.search({"yumurta"})
    assert list(results["title"]) == ["Kek", "Omlet", "Pilav"]


def test_max_missing_filtreler(engine):
    results = engine.search({"yumurta"}, max_missing=1)
    assert list(results["title"]) == ["Omlet"]          # kek: un+şeker eksik, pilav: 3 eksik


def test_pantry_eksik_sayisini_dusurur(engine):
    results = engine.search({"yumurta"}, max_missing=0, pantry=("tuz",))
    assert list(results["title"]) == ["Omlet"]


def test_require_all(engine):
    results = engine.search({"yumurta", "un"}, require_all=True)
    assert list(results["title"]) == ["Kek"]