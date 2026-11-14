"""'gr' birimi ne sıklıkla, hangi biçimlerde geçiyor? UNITS'e eklemeden önce ölçüyoruz."""
from collections import Counter

from datasets import load_dataset
from nepisirsem.recipe_parser import NUMBER, extract_ingredient_lines

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()

groups = Counter()       # her biçimden kaç tane var
examples = {}            # her biçim için birkaç örnek satır

for text in df["text"]:
    for line in extract_ingredient_lines(text):
        match = NUMBER.match(line)
        if not match:
            continue
        rest = line[match.end():].strip()
        if not rest.startswith("gr") or rest.startswith("gram"):
            continue                      # "gr" ile başlamıyor ya da zaten "gram"

        next_char = rest[2:3]             # "gr"den hemen sonraki karakter
        if next_char == ".":
            group = "gr.  (zaten tanınıyor)"
        elif next_char == " ":
            group = "gr + boşluk"
        else:
            group = "gr + harf (birim mi, kelime mi?)"

        groups[group] += 1
        examples.setdefault(group, []).append(line)

for group, count in groups.most_common():
    print(f"\n{count:6d}  {group}")
    for line in examples[group][:15]:
        print("        ", line)