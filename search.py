import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

print("Yükleniyor...")
df = pd.read_parquet("data/recipes.parquet")
vectors = np.load("data/recipe_vectors.npy")
model = SentenceTransformer(MODEL_NAME)


def search(query, top_k=5):
    """Sorguya en yakın top_k tarifi döndürür."""
    query_vector = model.encode(query, normalize_embeddings=True)
    scores = vectors @ query_vector
    best = np.argsort(-scores)[:top_k]
    return df.iloc[best].assign(score=scores[best])


while True:
    query = input("\nElindeki malzemeler (çıkmak için Enter): ")
    if not query:
        break
    for _, row in search(query).iterrows():
        print(f"\n{row['score']:.2f}  {row['url']}")
        print("      ", ", ".join(row["ingredients"]))