import json
import sys

from evals.metrics import report
from src.agent import triage

path, tag = sys.argv[1], sys.argv[2]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
data = json.load(open(path))[:limit]

preds, fails = [], 0
for i, d in enumerate(data):
    try:
        out = triage(d["text"], save_to_log=False)
        r = out["result"]
        preds.append({
            "text": d["text"],
            "gold_principle": d["principle"],
            "gold_severity": d["severity"],
            "pred_principle": r["principle"],
            "pred_severity": r["severity"],
            "confidence": r["confidence"],
            "review": out["needs_human_review"],
        })
    except Exception as e:
        fails += 1
        print(f"\nFAIL row {i}: {e}")
    print(f"{i + 1}/{len(data)}", end="\r")

json.dump(preds, open(f"evals/preds_{tag}.json", "w"), indent=1)
print(f"\nfailures: {fails}")
report(
    [p["gold_principle"] for p in preds],
    [p["gold_severity"] for p in preds],
    [p["pred_principle"] for p in preds],
    [p["pred_severity"] for p in preds],
    [p["review"] for p in preds],
    label=tag,
)
