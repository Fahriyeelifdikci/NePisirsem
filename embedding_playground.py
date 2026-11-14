from sentence_transformers import SentenceTransformer, util

MODELS = [
    "paraphrase-multilingual-MiniLM-L12-v2",
    "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr",
]

SIMILAR = [
    ("vanilya", "vanilin"),
    ("şeker", "toz şeker"),
    ("kıyma", "dana kıyma"),
    ("kaşar", "kaşar peyniri"),
    ("zeytinyağı", "sıvı yağ"),
    ("salça", "domates salçası"),
]

DIFFERENT = [
    ("vanilya", "kıyma"),
    ("şeker", "sarımsak"),
    ("çikolata", "maydanoz"),
    ("un", "balık"),
    ("süt", "soğan"),
    ("bal", "karabiber"),
]


def average_score(model, pairs):
    """Çiftlerin ortalama benzerlik skorunu hesaplar."""
    left = model.encode([a for a, b in pairs])
    right = model.encode([b for a, b in pairs])
    scores = util.cos_sim(left, right).diagonal()
    return scores.mean().item()


for name in MODELS:
    model = SentenceTransformer(name)
    similar = average_score(model, SIMILAR)
    different = average_score(model, DIFFERENT)
    print(name)
    print(f"  benzer çiftler:   {similar:.2f}")
    print(f"  alakasız çiftler: {different:.2f}")
    print(f"  FARK:             {similar - different:.2f}\n")