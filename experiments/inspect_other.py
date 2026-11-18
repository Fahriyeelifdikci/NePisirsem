"""'Diğer' kategorisine hangi tarifler düşüyor? Yeni anahtar kelime adaylarını bulmak için."""
from collections import Counter

import pandas as pd
from nepisirsem.categories import categorize
from nepisirsem.paths import DATA_DIR
from nepisirsem.recipe_parser import clean_name

df = pd.read_parquet(DATA_DIR / "recipes.parquet")
df["category"] = df.apply(lambda row: categorize(row["title"], row["ingredients"])[1], axis=1)

counts = df["category"].value_counts()
print("Kategori dağılımı:")
print(counts.to_string())
print(f"\n'Diğer' oranı: %{counts.get('Diğer', 0) / len(df) * 100:.1f}")

other = df[df["category"] == "Diğer"]["title"]

print("\n'Diğer'den rastgele 30 tarif:")
print(other.sample(30, random_state=0).to_string(index=False))

words = Counter(w for title in other for w in clean_name(title).split())
print("\n'Diğer'de en sık 50 kelime:")
for word, count in words.most_common(50):
    print(f"{count:5d}  {word}")