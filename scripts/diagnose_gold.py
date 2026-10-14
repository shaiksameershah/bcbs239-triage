import json

gold = json.load(open("data/gold.json"))
key = {k["text"]: k for k in json.load(open("data/gold_key.json"))}
preds = {p["text"]: p for p in json.load(open("evals/preds_agent_v2.json"))}
rows = [(g, key[g["text"]], preds.get(g["text"])) for g in gold if g["text"] in key]


def pct(pairs):
    pairs = list(pairs)
    return f"{sum(a == b for a, b in pairs) / len(pairs):.0%}" if pairs else "n/a"


print("rows:", len(rows))
print("YOUR labels vs SYNTHETIC   principle", pct((g["principle"], k["principle"]) for g, k, p in rows),
      "| severity", pct((g["severity"], k["severity"]) for g, k, p in rows))
scored = [(g, k, p) for g, k, p in rows if p]
print("AGENT vs YOUR labels       principle", pct((g["principle"], p["pred_principle"]) for g, k, p in scored),
      "| severity", pct((g["severity"], p["pred_severity"]) for g, k, p in scored))
print("AGENT vs SYNTHETIC labels  principle", pct((k["principle"], p["pred_principle"]) for g, k, p in scored),
      "| severity", pct((k["severity"], p["pred_severity"]) for g, k, p in scored))
print("always-'high' baseline vs yours, severity", pct((g["severity"], "high") for g, k, p in scored))

for flag in (False, True):
    sub = [(g, k) for g, k, p in rows if k.get("ambiguous", False) == flag]
    if sub:
        print(f"ambiguous={flag} (n={len(sub)}): your vs synthetic principle",
              pct((g["principle"], k["principle"]) for g, k in sub),
              "| severity", pct((g["severity"], k["severity"]) for g, k in sub))

for syn, mine in (("high", "medium"), ("critical", "high")):
    ex = [g["text"] for g, k, p in rows if k["severity"] == syn and g["severity"] == mine][:6]
    print(f"\nSynthetic={syn}, yours={mine}: {len(ex)} examples")
    for t in ex:
        print("  -", t[:170])
