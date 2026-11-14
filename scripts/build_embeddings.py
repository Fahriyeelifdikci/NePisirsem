import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

df = pd.read_parquet("data/recipes.parquet")
texts = df["ingredients"].apply(lambda ings: ", ".join(sorted(ings))).tolist()
print("Örnek metin:", texts[0])
print("Tarif sayısı:", len(texts))

model = SentenceTransformer(MODEL_NAME)
vectors = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    normalize_embeddings=True,
)

np.save("data/recipe_vectors.npy", vectors)
print("Vektör tablosu:", vectors.shape, "→ data/recipe_vectors.npy")