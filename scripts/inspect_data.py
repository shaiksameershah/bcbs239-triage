import collections
import statistics

from src.data import load_file

for name in ("train", "val", "test"):
    rows = load_file(f"data/synthetic/{name}.json")
    print(f"\n===== {name}: {len(rows)} rows =====")
    print("key sets:", collections.Counter(tuple(sorted(r.keys())) for r in rows).most_common(2))
    for k in ("principle", "severity", "ambiguous"):
        print(k, collections.Counter(r.get(k) for r in rows).most_common())
    lens = [len(str(r.get("text", "")).split()) for r in rows]
    print("words min/median/max:", min(lens), statistics.median(lens), max(lens))
    texts = [str(r.get("text", "")).strip().lower() for r in rows]
    print("exact duplicates within file:", len(texts) - len(set(texts)))
    print("sample:", rows[0])

tr = {str(r.get("text", "")).strip().lower() for r in load_file("data/synthetic/train.json")}
for other in ("val", "test"):
    ot = {str(r.get("text", "")).strip().lower() for r in load_file(f"data/synthetic/{other}.json")}
    print(f"\nexact overlap train vs {other}:", len(tr & ot))
