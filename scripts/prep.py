import collections
import json
import re

import numpy as np
import ollama

from src.data import ALLOWED_P, ALLOWED_S, load_file

EMBED_MODEL = "nomic-embed-text"
NEAR = 0.95
FILES = {
    "train": "data/synthetic/train.json",
    "dev": "data/synthetic/val.json",
    "test": "data/synthetic/test.json",
}


def clean(rows):
    out, seen, bad = [], set(), 0
    for r in rows:
        t = re.sub(r"\s+", " ", str(r.get("text", "")).strip())
        if not t or r.get("principle") not in ALLOWED_P or r.get("severity") not in ALLOWED_S:
            bad += 1
            continue
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        out.append({
            "text": t,
            "principle": r["principle"],
            "severity": r["severity"],
            "ambiguous": bool(r.get("ambiguous", False)),
        })
    return out, bad


def embed_all(texts, batch=64):
    out = []
    for i in range(0, len(texts), batch):
        out += ollama.embed(model=EMBED_MODEL, input=texts[i:i + batch])["embeddings"]
        print(f"  embedded {min(i + batch, len(texts))}/{len(texts)}", end="\r")
    print()
    return np.array(out, dtype="float32")


def dedupe_within(rows, X):
    sim = X @ X.T
    np.fill_diagonal(sim, 0)
    drop = np.zeros(len(rows), bool)
    for i in range(len(rows)):
        if not drop[i]:
            drop[np.where(sim[i, i + 1:] > NEAR)[0] + i + 1] = True
    keep = ~drop
    return [r for r, k in zip(rows, keep) if k], X[keep], int(drop.sum())


def drop_similar(rows, X, ref):
    keep = (X @ ref.T).max(axis=1) <= NEAR
    return [r for r, k in zip(rows, keep) if k], X[keep], int((~keep).sum())


data = {}
for name, path in FILES.items():
    rows, bad = clean(load_file(path))
    print(f"{name}: {len(rows)} rows after validation and exact dedupe ({bad} invalid)")
    X = embed_all([r["text"] for r in rows])
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    rows, X, n = dedupe_within(rows, X)
    print(f"{name}: removed {n} near-duplicates within split, {len(rows)} remain")
    data[name] = (rows, X)

# Leakage: test is the anchor and is never reduced further
rows, X, n = drop_similar(*data["dev"], data["test"][1])
data["dev"] = (rows, X)
print(f"dev: removed {n} rows too similar to test")

ref = np.vstack([data["dev"][1], data["test"][1]])
rows, X, n = drop_similar(*data["train"], ref)
data["train"] = (rows, X)
print(f"train: removed {n} rows too similar to dev or test")

print("\nFinal splits")
for name, (rows, X) in data.items():
    json.dump(rows, open(f"data/splits/{name}.json", "w"), indent=1)
    np.save(f"data/cache/{name}_X.npy", X)
    print(f"  {name}: {len(rows)} rows | severity {dict(collections.Counter(r['severity'] for r in rows))}")
