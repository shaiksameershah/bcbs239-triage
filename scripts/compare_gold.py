import collections
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
key_path = root / "data" / "gold_key.json"
csv_path = root / "data" / "gold_review.csv"
out_path = root / "data" / "gold.json"

with key_path.open() as f:
    key = json.load(f)
with csv_path.open(newline="") as f:
    mine = list(csv.DictReader(f))

if not mine:
    raise SystemExit(f"No rows found in {csv_path}. Add review labels to the CSV before comparing.")

if len(key) != len(mine):
    print(
        f"Warning: gold_key has {len(key)} rows but gold_review.csv has {len(mine)} rows; "
        "comparing the overlapping records."
    )

rows = []
for idx, (k, m) in enumerate(zip(key, mine), start=1):
    principle = (m.get("my_principle") or "").strip()
    severity = (m.get("my_severity") or "").strip()
    if principle and severity:
        rows.append((k, m, principle, severity))

if not rows:
    print(f"No hand-verified rows found in {csv_path}. Fill in my_principle and my_severity before running this script.")
    raise SystemExit(0)

n = len(rows)
p = sum(k["principle"] == principle for k, _, principle, _ in rows)
s = sum(k["severity"] == severity for k, _, _, severity in rows)
print(f"reviewed {n}; principle agreement {p/n:.0%}; severity agreement {s/n:.0%}")

diffs = collections.Counter(
    (k["severity"], severity) for k, _, _, severity in rows if k["severity"] != severity
)
for (a, b), c in diffs.most_common():
    print(f"  synthetic label {a} vs mine {b}: {c}")

gold = [
    {**k, "principle": principle, "severity": severity, "gold": True}
    for k, _, principle, severity in rows
]
with out_path.open("w") as f:
    json.dump(gold, f, indent=2)
print("wrote data/gold.json with", len(gold), "hand-verified rows")
