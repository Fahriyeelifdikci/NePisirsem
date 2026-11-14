import pandas as pd
from categories import categorize

df = pd.read_parquet("data/recipes.parquet")
df["category"] = df["title"].apply(lambda t: categorize(t)[1])

print(df["category"].value_counts())

print("\n'Diğer'den rastgele 25 tarif:")
print(df[df["category"] == "Diğer"]["title"].sample(25, random_state=0).to_string())

from collections import Counter
from recipe_parser import clean_name

other = df[df["category"] == "Diğer"]["title"]
words = Counter(w for t in other for w in clean_name(t).split())
print("\n'Diğer'de en sık 40 kelime:")
for w, c in words.most_common(40):
    print(f"{c:5d}  {w}")