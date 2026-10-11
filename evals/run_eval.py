import json

from src.agent import triage

data = json.load(open("data/labeled.json"))
p_ok = s_ok = 0
clear_p = clear_n = 0

for d in data:
    r = triage(d["text"], save_to_log=False)["result"]
    p_hit = r["principle"] == d["principle"]
    s_hit = r["severity"] == d["severity"]
    p_ok += p_hit
    s_ok += s_hit
    if not d["ambiguous"]:
        clear_n += 1
        clear_p += p_hit
    flag = "" if (p_hit and s_hit) else "  <-- MISS"
    print(f"{d['text'][:55]:55} | {r['principle']:24} {r['severity']:8}{flag}")

n = len(data)
print(f"\nPrinciple accuracy (all):       {p_ok}/{n} = {p_ok/n:.0%}")
print(f"Principle accuracy (clear only): {clear_p}/{clear_n} = {clear_p/clear_n:.0%}")
print(f"Severity accuracy (all):        {s_ok}/{n} = {s_ok/n:.0%}")