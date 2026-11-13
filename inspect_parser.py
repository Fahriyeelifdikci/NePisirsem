from collections import Counter
from datasets import load_dataset
from recipe_parser import extract_ingredient_lines, parse_ingredient

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)
all_lines = [line for lst in df["raw_ingredients"] for line in lst]

names = []
no_unit = 0

for line in all_lines:
    amount, unit, name = parse_ingredient(line)
    if unit is None:
        no_unit += 1
    names.append(name)

print("Toplam satır:", len(all_lines))
print("Birimsiz satır:", no_unit)
print("Farklı malzeme adı:", len(set(names)))

print("\nEn sık 40 malzeme adı:")
for name, count in Counter(names).most_common(40):
    print(f"{count:5d}  {name}")