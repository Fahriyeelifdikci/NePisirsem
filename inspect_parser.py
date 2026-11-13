from collections import Counter
from datasets import load_dataset
from recipe_parser import extract_ingredient_lines

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()
df["raw_ingredients"] = df["text"].apply(extract_ingredient_lines)

# Bütün tariflerin malzemelerini tek bir uzun listede topla
all_lines = [line for lst in df["raw_ingredients"] for line in lst]

# Sayıyla başlamayan satırları ayır
no_digit = [line for line in all_lines if not line[0].isdigit()]
print(f"Toplam satır: {len(all_lines)}")
print(f"Sayıyla başlamayan: {len(no_digit)}")

# En sık tekrar eden 30 tanesini göster
for line, count in Counter(no_digit).most_common(30):
    print(f"{count:5d}  {line}")

import random
random.seed(0)
print("\n--- Rastgele 30 örnek ---")
for line in random.sample(no_digit, 30):
    print("  ", line)