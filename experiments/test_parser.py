from datasets import load_dataset
from recipe_parser import extract_ingredient_lines

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()

# İlk 3 tarifi elle kontrol et
for i in range(3):
    print(f"\n--- Tarif {i} ---")
    for item in extract_ingredient_lines(df.iloc[i]["text"]):
        print(" ", item)

# Toplu kontrol: kaç tarif için en az 1 malzeme çıkarabildik?
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)
counts = df["raw_ingredients"].apply(len)
print(f"\nMalzemesi çıkarılabilen tarif: {(counts > 0).sum()}")
print("Tarif başına malzeme sayısı:")
print(counts[counts > 0].describe().round(1))
