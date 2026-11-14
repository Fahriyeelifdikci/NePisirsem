import numpy as np
import pandas as pd
from nepisirsem.evaluation import evaluate, make_queries, rank_of
from nepisirsem.search import RecipeSearch


class FakeModel:
    def encode(self, text, normalize_embeddings=True):
        return np.array([1.0, 0.0], dtype=np.float32)


def test_rank_of_esit_puanlarda_ortalama_sira():
    scores = np.array([0.9, 0.5, 0.5, 0.1])
    assert rank_of(scores, 0) == 1
    assert rank_of(scores, 1) == 2.5          # 2. ve 3. sıra paylaşılıyor


def test_make_queries_kaynak_tarifin_malzemelerinden_secer():
    df = pd.DataFrame({"ingredients": [["un", "yumurta", "şeker", "süt", "kakao"]] * 3})
    for pos, have in make_queries(df, n=3, keep=0.6, seed=0):
        assert have <= set(df["ingredients"].iloc[pos])
        assert len(have) == 3                  # 5 malzemenin %60'ı


def test_evaluate_calisir_ve_metrikler_mantikli():
    df = pd.DataFrame({"ingredients": [
        ["un", "yumurta", "şeker", "süt", "kakao"],
        ["pirinç", "tereyağı", "şehriye", "tavuk suyu", "karabiber"],
    ]})
    vectors = np.array([[0.9, 0.1], [0.1, 0.9]], dtype=np.float32)
    engine = RecipeSearch(df, vectors, FakeModel())
    report = evaluate(engine, make_queries(df, n=2, seed=0), top=1)
    for metrics in report.values():
        assert 0 <= metrics["MRR"] <= 1
    assert report["kapsama (baseline)"]["isabet@1"] == 1.0   # kendi malzemeleriyle kendini bulmalı