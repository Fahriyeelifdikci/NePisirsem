import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from nepisirsem.recipe_parser import clean_name
from nepisirsem.matching import DEFAULT_PANTRY, missing, uses_all

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

print("Yükleniyor...")
df = pd.read_parquet("data/recipes.parquet")
vectors = np.load("data/recipe_vectors.npy").astype(np.float32)
model = SentenceTransformer(MODEL_NAME)


def parse_query(query):
    """'Yumurta, un , süt' → {'yumurta', 'un', 'süt'}"""
    return {clean_name(part) for part in query.split(",") if part.strip()}


def search(have, top_k=24, candidates=300, max_missing=None,
           pantry=(), require_all=False):
    """Kullanıcının malzemelerine en uygun tarifleri bulur.

    have        : kullanıcının malzemeleri (temiz adlar)
    top_k       : en fazla kaç tarif döndürülsün
    candidates  : modelden kaç aday alınsın (filtrelerden önce)
    max_missing : en fazla kaç eksik malzemeye izin verilsin (None = sınırsız)
    pantry      : kullanıcının "evde hep var" dediği temel malzemeler
    require_all : tarif, seçilen malzemelerin hepsini kullanmak zorunda mı
    """
    have = set(have)

    query_vector = model.encode(", ".join(sorted(have)), normalize_embeddings=True)
    scores = vectors @ query_vector
    best = np.argsort(-scores)[:candidates]

    results = df.iloc[best].copy()
    results["score"] = scores[best]
    results["missing"] = results["ingredients"].apply(
        lambda ingredients: missing(ingredients, have, pantry)
    )
    results["n_missing"] = results["missing"].apply(len)
    results["n_total"] = results["ingredients"].apply(len)

    if max_missing is not None:
        results = results[results["n_missing"] <= max_missing]
    if require_all:
        results = results[results["ingredients"].apply(lambda ings: uses_all(ings, have))]

    results = results.sort_values("score", ascending=False)
    return results.head(top_k)


if __name__ == "__main__":
    while True:
        query = input("\nElindeki malzemeler (çıkmak için Enter): ")
        if not query:
            break
        for _, row in search(parse_query(query), top_k=5, pantry=DEFAULT_PANTRY).iterrows():
            n_have = row["n_total"] - row["n_missing"]
            print(f"\n{row['title']}  ({n_have}/{row['n_total']} malzeme sende)")
            if row["n_missing"] == 0:
                print("   ✅ Hepsi var!")
            else:
                print("   ❌ Eksik:", ", ".join(row["missing"]))