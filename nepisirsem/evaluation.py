"""Arama yöntemlerini karşılaştırmak için 'kaynak tarifi geri bulma' testi.

Fikir: Rastgele bir tarif seç, malzemelerinin bir kısmını "kullanıcının elindekiler" yap.
İyi bir arama yöntemi o tarifi (kaynak tarifi) üst sıralarda göstermeli.
Etiketlemeye gerek yok: doğru cevabı sorguyu üretirken zaten biliyoruz.
"""
import numpy as np
from nepisirsem.matching import DEFAULT_PANTRY, missing


# ---------- Sorgu üretimi ----------

def make_queries(df, n=200, keep=0.6, seed=42):
    """[(kaynak_tarif_pozisyonu, kullanıcının_malzemeleri), ...] üretir.
    keep: kaynak tarifin (pantry dışı) malzemelerinin ne kadarı kullanıcıda olsun
    """
    rng = np.random.default_rng(seed)               # seed: her çalıştırmada aynı sorgular
    sizes = df["ingredients"].apply(len).to_numpy()
    positions = rng.permutation(np.flatnonzero(sizes >= 5))

    queries = []
    for pos in positions:
        own = [i for i in df["ingredients"].iloc[pos] if i not in DEFAULT_PANTRY]
        if len(own) < 3:
            continue
        k = max(2, round(len(own) * keep))
        have = set(rng.choice(own, size=k, replace=False))
        queries.append((int(pos), have))
        if len(queries) == n:
            break
    return queries


# ---------- Sıralama yöntemleri: her biri bütün tariflere bir puan verir ----------

def embedding_scores(engine, have):
    """Şu anki yöntem: malzeme listelerinin anlamsal benzerliği."""
    query = engine.model.encode(", ".join(sorted(have)), normalize_embeddings=True)
    return engine.vectors @ query


def coverage_scores(engine, have):
    """Basit taban çizgisi (baseline): tarifin malzemelerinin yüzde kaçı sende var?"""
    return np.array([
        1 - len(missing(ings, have, DEFAULT_PANTRY)) / len(ings)
        for ings in engine.df["ingredients"]
    ])


def hybrid_scores(engine, have, weight=0.5):
    """İkisinin ağırlıklı ortalaması."""
    return weight * embedding_scores(engine, have) + (1 - weight) * coverage_scores(engine, have)


METHODS = {
    "embedding (şu anki)": embedding_scores,
    "kapsama (baseline)": coverage_scores,
    "hibrit (0.5 / 0.5)": hybrid_scores,
}


# ---------- Ölçüm ----------

def rank_of(scores, target):
    """Hedef tarifin sırası (1 = en üst). Eşit puanlılarda ortalama sıra: kimseyi kayırmaz."""
    greater = (scores > scores[target]).sum()
    equal = (scores == scores[target]).sum()          # hedefin kendisi dahil
    return greater + (equal + 1) / 2


def evaluate(engine, queries, methods=METHODS, top=10):
    """Her yöntem için ortalama metrikleri döndürür."""
    report = {}
    for name, method in methods.items():
        ranks, top_missing = [], []
        for target, have in queries:
            scores = method(engine, have)
            ranks.append(rank_of(scores, target))
            best = np.argsort(-scores)[:top]
            top_missing.append(np.mean([
                len(missing(engine.df["ingredients"].iloc[i], have, DEFAULT_PANTRY)) for i in best
            ]))
        ranks = np.array(ranks)
        report[name] = {
            "isabet@1": np.mean(ranks <= 1),
            f"isabet@{top}": np.mean(ranks <= top),
            "MRR": np.mean(1 / ranks),
            f"ilk {top}'da ort. eksik": np.mean(top_missing),
            "3000 dışında kalan": np.mean(ranks > 3000),
        }
    return report