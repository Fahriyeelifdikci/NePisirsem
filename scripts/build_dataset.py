import re
from pathlib import Path
from datasets import load_dataset
from nepisirsem.recipe_parser import extract_ingredient_lines, parse_ingredient, clean_name

TITLE = re.compile(r"([^\n]+?) Tarifi Nasıl Yapılır\?")


def ingredient_names(lines):
    """Ham satırlardan temiz, tekrarsız malzeme adı listesi üretir."""
    names = []
    for line in lines:
        amount, unit, name = parse_ingredient(line)
        name = clean_name(name)
        if name:
            names.append(name)
    return list(dict.fromkeys(names))


def extract_title(text, url):
    """Tarifin adını metinden çıkarır, bulamazsa URL'den üretir."""
    match = TITLE.search(text)
    if match:
        return match.group(1).strip()
    return url.rstrip("/").split("/")[-1].replace("-", " ").capitalize()


df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)

df = df[df["raw_ingredients"].apply(len) > 0].copy()
df["ingredients"] = df["raw_ingredients"].apply(ingredient_names)
df["url"] = df["metadata"].apply(lambda m: m["url"])
df["title"] = df.apply(lambda row: extract_title(row["text"], row["url"]), axis=1)

out = df[["id", "url", "title", "text", "raw_ingredients", "ingredients"]]

Path("data").mkdir(exist_ok=True)
out.to_parquet("data/recipes.parquet", index=False)

fallback = (~out["text"].str.contains(" Tarifi Nasıl Yapılır?", regex=False)).sum()

print(len(out), "tarif kaydedildi → data/recipes.parquet")
print("Adı metinden bulunamayan (URL'den üretilen):", fallback)
print(out[["title", "url"]].head(10))