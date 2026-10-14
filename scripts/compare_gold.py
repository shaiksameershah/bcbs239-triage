import collections
import csv
import json
import re

from src.data import ALLOWED_P, ALLOWED_S

PMAP = {
    "2": "P2_architecture_lineage",
    "3": "P3_accuracy_integrity",
    "4": "P4_completeness",
    "5": "P5_timeliness",
    "6": "P6_adaptability",
}
WORDS = {
    "lineage": "2", "architecture": "2",
    "accuracy": "3", "integrity": "3",
    "completeness": "4", "complete": "4",
    "timeliness": "5", "timely": "5",
    "adaptability": "6", "adapt": "6",
}


def norm_p(x):
    x = x.strip()
    if x in ALLOWED_P:
        return x
    m = re.search(r"p\s*([2-6])", x.lower())
    if m:
        return PMAP[m.group(1)]
    for w, n in WORDS.items():
        if w in x.lower():
            return PMAP[n]
    return x


def norm_s(x):
    return x.strip().lower()


key = json.load(open("data/gold_key.json"))
rows = list(csv.DictReader(open("data/gold_review.csv", encoding="utf-8-sig")))

done, bad = [], []
for m in rows:
    if not m["my_principle"].strip() or not m["my_severity"].strip():
        continue
    k = key[int(float(m["id"]))]
    p, s = norm_p(m["my_principle"]), norm_s(m["my_severity"])
    if p not in ALLOWED_P or s not in ALLOWED_S:
        bad.append((m["id"], m["my_principle"], m["my_severity"]))
        continue
    done.append((k, p, s))

if bad:
    print("Unrecognized labels (fix these rows in the CSV, then rerun):")
    for b in bad[:20]:
        print("  id", b[0], "| principle:", repr(b[1]), "| severity:", repr(b[2]))
    raise SystemExit(1)

n = len(done)
pa = sum(k["principle"] == p for k, p, s in done)
sa = sum(k["severity"] == s for k, p, s in done)
print(f"reviewed {n}; principle agreement {pa/n:.0%}; severity agreement {sa/n:.0%}")
diffs = collections.Counter((k["severity"], s) for k, p, s in done if k["severity"] != s)
for (a, b), c in diffs.most_common():
    print(f"  synthetic label {a} vs mine {b}: {c}")

gold = [{**k, "principle": p, "severity": s, "gold": True} for k, p, s in done]
json.dump(gold, open("data/gold.json", "w"), indent=2)
print("wrote data/gold.json with", len(gold), "hand-verified rows")
print("gold severity counts:", dict(collections.Counter(g["severity"] for g in gold)))
