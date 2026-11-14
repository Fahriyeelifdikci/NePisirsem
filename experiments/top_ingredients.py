"""En sık geçen malzeme adlarını sayar: hangileri aynı şeyin farklı adı?"""
from collections import Counter
import pandas as pd

df = pd.read_parquet("data/recipes.parquet")
counts = Counter(name for ingredients in df["ingredients"] for name in ingredients)

print(f"Toplam farklı malzeme adı: {len(counts)}")
print(f"Sadece 1 tarifte geçen:    {sum(1 for c in counts.values() if c == 1)}\n")

for name, count in counts.most_common(150):
    print(f"{count:6d}  {name}")