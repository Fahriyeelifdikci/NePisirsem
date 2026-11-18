from nepisirsem.recipe_parser import parse_ingredient
examples = [
    "100gramtereyağı",
    "1,5su bardağıun",
    "1.5su bardağısüt",
    "2 tepeleme yemek kaşığıun",
    "200ml.süt",
    "1başsarımsak",
    "1küçük boy kabak",
    "Yarımadetkabak",
    '"su bardağımakarna',
]

for line in examples:
    print(line, "→", parse_ingredient(line))