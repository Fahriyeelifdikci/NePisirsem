from collections import Counter
from datasets import load_dataset
from recipe_parser import extract_ingredient_lines, parse_ingredient, clean_name

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)
all_lines = [line for lst in df["raw_ingredients"] for line in lst]

raw_names = []
clean_names = []

for line in all_lines:
    amount, unit, name = parse_ingredient(line)
    raw_names.append(name)
    clean_names.append(clean_name(name))

empty = clean_names.count("")

print("Farklı ad (temizlik ÖNCESİ):", len(set(raw_names)))
print("Farklı ad (temizlik SONRASI):", len(set(clean_names)))
print("Temizlikten sonra boş kalan:", empty)

print("\nTemizlik sonrası en sık 40 ad:")
for name, count in Counter(clean_names).most_common(40):
    print(f"{count:5d}  {name}")

# Çok kelimeli adların ilk kelimesi: sıfat adayları
first_words = Counter(
    name.split()[0] for name in clean_names if len(name.split()) > 1
)

print("\nÇok kelimeli adlarda en sık 40 İLK kelime:")
for word, count in first_words.most_common(40):
    print(f"{count:5d}  {word}")