"""Arama yöntemlerini karşılaştırır.  Kullanım:  python -m scripts.evaluate --n 200"""
import argparse
import time

from nepisirsem.evaluation import evaluate, make_queries
from nepisirsem.search import RecipeSearch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=200, help="kaç sorgu üretilsin")
    parser.add_argument("--keep", type=float, default=0.6, help="kaynak tarifin malzemelerinin ne kadarı kullanıcıda")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    engine = RecipeSearch.from_files()
    queries = make_queries(engine.df, n=args.n, keep=args.keep, seed=args.seed)
    print(f"{len(queries)} sorgu, keep={args.keep}, seed={args.seed}\n")

    start = time.time()
    report = evaluate(engine, queries)
    metrics = list(next(iter(report.values())))

    print(f"{'yöntem':<22}" + "".join(f"{m:>24}" for m in metrics))
    for name, values in report.items():
        print(f"{name:<22}" + "".join(f"{values[m]:>24.3f}" for m in metrics))
    print(f"\nSüre: {time.time() - start:.0f} sn")


if __name__ == "__main__":
    main()