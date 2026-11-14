import pandas as pd
from recipe_parser import extract_ingredient_lines

df = pd.read_parquet("data/recipes.parquet")
row = df[df["url"].str.contains("saglikli-mini-pankek")].iloc[0]

text = row["text"]
start = text.find("İçin Malzemeler")
print(repr(text[start:start + 600]))

print("\nRobotun çıkardığı satırlar:")
for line in extract_ingredient_lines(text):
    print("  ", line)

print("\nTemiz malzeme listesi:", list(row["ingredients"]))