import re
from datasets import load_dataset
from nepisirsem.paths import DATA_DIR
from nepisirsem.recipe_parser import extract_ingredient_lines, parse_ingredients

TITLE = re.compile(r"([^\n]+?) Tarifi Nasıl Yapılır\?")


def extract_title(text, url):
    """Tarifin adını metinden çıkarır, bulamazsa URL'den üretir."""
    match = TITLE.search(text)
    if match:
        return match.group(1).strip()
    return url.rstrip("/").split("/")[-1].replace("-", " ").capitalize()


def main():
    df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
    df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)
    df = df[df["raw_ingredients"].apply(len) > 0].copy()

    pairs = df["raw_ingredients"].apply(parse_ingredients)        # [(ad, miktar), ...]
    df["ingredients"] = pairs.apply(lambda p: [name for name, _ in p])
    df["amounts"] = pairs.apply(lambda p: [amount for _, amount in p])
    df["url"] = df["metadata"].apply(lambda m: m["url"])
    df["title"] = df.apply(lambda row: extract_title(row["text"], row["url"]), axis=1)

    out = df[["id", "url", "title", "ingredients", "amounts"]]
    DATA_DIR.mkdir(exist_ok=True)
    out.to_parquet(DATA_DIR / "recipes.parquet", index=False)

    fallback = (~df["text"].str.contains(" Tarifi Nasıl Yapılır?", regex=False)).sum()
    print(len(out), "tarif kaydedildi →", DATA_DIR / "recipes.parquet")
    print("Adı metinden bulunamayan (URL'den üretilen):", fallback)
    print(out[["title", "ingredients", "amounts"]].head(5).to_string())


if __name__ == "__main__":
    main()