import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from recipe_parser import clean_name

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

PANTRY = {"tuz", "su", "karabiber", "sıvı yağ", "zeytinyağı", "pul biber", "şeker"}

# "X varsa bunlar da vardır": bir malzemenin parçaları ya da ondan hemen elde edilenler
DERIVED = {
    "yumurta": ["yumurta akı", "yumurta sarısı"],
    "limon": ["limon suyu", "limon kabuğu rendesi"],
    "portakal": ["portakal suyu", "portakal kabuğu rendesi"],
}

print("Yükleniyor...")
df = pd.read_parquet("data/recipes.parquet")
vectors = np.load("data/recipe_vectors.npy")
model = SentenceTransformer(MODEL_NAME)


def parse_query(query):
    """'Yumurta, un , süt' → {'yumurta', 'un', 'süt'}"""
    return {clean_name(part) for part in query.split(",") if part.strip()}


def expand(have):
    """Elimizdekilere onlardan elde edilenleri de ekler.
    {"yumurta"} → {"yumurta", "yumurta akı", "yumurta sarısı"}
    """
    result = set(have)
    for item in have:
        result.update(DERIVED.get(item, []))
    return result


def has(ingredient, available):
    """Elimizdekiler bu malzemeyi karşılıyor mu?
    "yağlı kıyma", {"kıyma"} → True
    "limon suyu",  {"su"}    → False
    """
    for item in available:
        if ingredient == item or ingredient.endswith(" " + item):
            return True
    return False


def search(query, top_k=5, candidates=50):
    """Önce en benzer `candidates` tarifi bulur,
    sonra eksik malzemesi az olanı üste alarak sıralar."""
    have = parse_query(query)
    available = expand(have) | PANTRY

    query_vector = model.encode(query, normalize_embeddings=True)
    scores = vectors @ query_vector
    best = np.argsort(-scores)[:candidates]

    results = df.iloc[best].copy()
    results["score"] = scores[best]
    results["missing"] = results["ingredients"].apply(
        lambda ingredients: [i for i in ingredients if not has(i, available)]
    )
    results["n_missing"] = results["missing"].apply(len)

    results = results.sort_values(["n_missing", "score"], ascending=[True, False])
    return results.head(top_k)


while True:
    query = input("\nElindeki malzemeler (çıkmak için Enter): ")
    if not query:
        break
    for _, row in search(query).iterrows():
        print(f"\n{row['score']:.2f}  {row['url']}")
        if row["n_missing"] == 0:
            print("       ✅ Hepsi var!")
        else:
            print("       ❌ Eksik:", ", ".join(row["missing"]))