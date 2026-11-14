import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from recipe_parser import clean_name

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

PANTRY = {"tuz", "su", "karabiber", "sıvı yağ", "zeytinyağı", "pul biber", "şeker"}

# Her eksik malzemenin benzerlik puanından ne kadar düşüreceği.
# 0 → sadece benzerlik (B kuralı), 1 → önce eksik sayısı (A kuralı)
PENALTY = 0

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


def uses_all(ingredients, have):
    """Tarif, kullanıcının seçtiği HER malzemeyi kullanıyor mu?"""
    return all(
        any(has(ingredient, expand({item})) for ingredient in ingredients)
        for item in have
    )


def search(have, top_k=24, candidates=300, max_missing=None,
           use_pantry=True, require_all=False):
    """Kullanıcının malzemelerine en uygun tarifleri bulur.

    have        : kullanıcının malzemeleri (temiz adlar)
    top_k       : en fazla kaç tarif döndürülsün
    candidates  : modelden kaç aday alınsın (filtrelerden önce)
    max_missing : en fazla kaç eksik malzemeye izin verilsin (None = sınırsız)
    use_pantry  : tuz, su gibi temel malzemeler evde var sayılsın mı
    require_all : tarif, seçilen malzemelerin hepsini kullanmak zorunda mı
    """
    have = set(have)
    available = expand(have)
    if use_pantry:
        available |= PANTRY

    query_vector = model.encode(", ".join(sorted(have)), normalize_embeddings=True)
    scores = vectors @ query_vector
    best = np.argsort(-scores)[:candidates]

    results = df.iloc[best].copy()
    results["score"] = scores[best]
    results["missing"] = results["ingredients"].apply(
        lambda ingredients: [i for i in ingredients if not has(i, available)]
    )
    results["n_missing"] = results["missing"].apply(len)
    results["n_total"] = results["ingredients"].apply(len)
    results["final"] = results["score"] - PENALTY * results["n_missing"]

    if max_missing is not None:
        results = results[results["n_missing"] <= max_missing]
    if require_all:
        results = results[results["ingredients"].apply(lambda ings: uses_all(ings, have))]

    results = results.sort_values(["final", "n_missing"], ascending=[False, True])
    return results.head(top_k)


if __name__ == "__main__":
    while True:
        query = input("\nElindeki malzemeler (çıkmak için Enter): ")
        if not query:
            break
        for _, row in search(parse_query(query), top_k=5).iterrows():
            n_have = row["n_total"] - row["n_missing"]
            print(f"\n{row['title']}  ({n_have}/{row['n_total']} malzeme sende)")
            if row["n_missing"] == 0:
                print("   ✅ Hepsi var!")
            else:
                print("   ❌ Eksik:", ", ".join(row["missing"]))