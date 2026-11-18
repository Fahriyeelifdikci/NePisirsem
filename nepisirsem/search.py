import numpy as np
import pandas as pd
from nepisirsem.paths import DATA_DIR
from nepisirsem.recipe_parser import clean_name
from nepisirsem.matching import DEFAULT_PANTRY, missing, uses_all

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"


# Sıralama puanı = 0.7 × anlamsal benzerlik + 0.3 × kapsama (malzemelerin ne kadarı sende).
# Ağırlık değerlendirmeyle seçildi (scripts/evaluate.py, seed 42) ve yeni sorgularla doğrulandı (seed 7).
EMBEDDING_WEIGHT = 0.7

class RecipeSearch:
    """Tarif arama motoru: veri, vektörler ve model bir arada.

    Model dışarıdan verilir (dependency injection): uygulama gerçek modeli,
    testler ise sahte, hızlı bir modeli verebilir.
    """

    def __init__(self, df, vectors, model):
        self.df = df
        self.vectors = vectors
        self.model = model

    @classmethod
    def from_files(cls, data_dir=DATA_DIR, model_name=MODEL_NAME):
        """Diskteki veriyi ve gerçek modeli yükleyerek motoru kurar (yavaş: ~440 MB model)."""
        from sentence_transformers import SentenceTransformer   # ağır import: sadece gerektiğinde
        df = pd.read_parquet(data_dir / "recipes.parquet")
        vectors = np.load(data_dir / "recipe_vectors.npy").astype(np.float32)
        return cls(df, vectors, SentenceTransformer(model_name))

    def embedding_scores(self, have):
        """Her tarif için, malzeme listesinin kullanıcınınkine anlamca ne kadar benzediği."""
        query = self.model.encode(", ".join(sorted(have)), normalize_embeddings=True)
        return self.vectors @ query

    def search(self, have, top_k=24, max_missing=None, pantry=(), require_all=False):
        """Kullanıcının malzemelerine en uygun tarifleri bulur.

        have        : kullanıcının malzemeleri (temiz adlar)
        top_k       : en fazla kaç tarif döndürülsün
        max_missing : en fazla kaç eksik malzemeye izin verilsin (None = sınırsız)
        pantry      : kullanıcının "evde hep var" dediği temel malzemeler
        require_all : tarif, seçilen malzemelerin hepsini kullanmak zorunda mı
        """
        have = set(have)

        results = self.df.copy()                          # bütün tarifler: aday sınırı yok
        results["missing"] = [missing(ings, have, pantry) for ings in results["ingredients"]]
        results["n_missing"] = results["missing"].apply(len)
        results["n_total"] = results["ingredients"].apply(len)

        coverage = 1 - results["n_missing"] / results["n_total"]
        results["score"] = (EMBEDDING_WEIGHT * self.embedding_scores(have)
                            + (1 - EMBEDDING_WEIGHT) * coverage)

        if max_missing is not None:
            results = results[results["n_missing"] <= max_missing]
        if require_all:
            results = results[results["ingredients"].apply(lambda ings: uses_all(ings, have))]

        results = results.sort_values("score", ascending=False)
        return results.head(top_k)

def parse_query(query):
    """'Yumurta, un , süt' → {'yumurta', 'un', 'süt'}"""
    return {clean_name(part) for part in query.split(",") if part.strip()}


if __name__ == "__main__":
    print("Yükleniyor...")
    engine = RecipeSearch.from_files()
    while True:
        query = input("\nElindeki malzemeler (çıkmak için Enter): ")
        if not query:
            break
        for _, row in engine.search(parse_query(query), top_k=5, pantry=DEFAULT_PANTRY).iterrows():
            n_have = row["n_total"] - row["n_missing"]
            print(f"\n{row['title']}  ({n_have}/{row['n_total']} malzeme sende)")
            if row["n_missing"] == 0:
                print("   ✅ Hepsi var!")
            else:
                print("   ❌ Eksik:", ", ".join(row["missing"]))