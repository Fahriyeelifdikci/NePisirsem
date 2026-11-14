"""Parser değişikliğinin veriye etkisini ölçer: eski ve yeni parquet'i karşılaştırır."""
import os
import pandas as pd

old = pd.read_parquet(os.path.join(os.environ["TEMP"], "recipes_old.parquet"))
new = pd.read_parquet("data/recipes.parquet")


def unique_names(df):
    """Veri setindeki bütün farklı malzeme adlarının kümesi."""
    return {name for ingredients in df["ingredients"] for name in ingredients}


old_names, new_names = unique_names(old), unique_names(new)
changed = sum(list(a) != list(b) for a, b in zip(old["ingredients"], new["ingredients"]))

print(f"Tarif sayısı:              {len(old)} → {len(new)}")
print(f"Farklı malzeme adı:        {len(old_names)} → {len(new_names)}")
print(f"Malzeme listesi değişen:   {changed} tarif")
print("\nArtık olmayan adlardan örnekler:", sorted(old_names - new_names)[:20])