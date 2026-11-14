from pathlib import Path
from datasets import load_dataset
from recipe_parser import extract_ingredient_lines, parse_ingredient, clean_name


def ingredient_names(lines):
    """Ham satırlardan temiz, tekrarsız malzeme adı listesi üretir."""
    names = []
    for line in lines:
        amount, unit, name = parse_ingredient(line)
        name = clean_name(name)
        if name:
            names.append(name)
    return list(dict.fromkeys(names))


df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)

df = df[df["raw_ingredients"].apply(len) > 0].copy()
df["ingredients"] = df["raw_ingredients"].apply(ingredient_names)
df["url"] = df["metadata"].apply(lambda m: m["url"])

out = df[["id", "url", "text", "raw_ingredients", "ingredients"]]

Path("data").mkdir(exist_ok=True)
out.to_parquet("data/recipes.parquet", index=False)

print(len(out), "tarif kaydedildi → data/recipes.parquet")
print(out[["url", "ingredients"]].head())