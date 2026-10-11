import json
import sys

from src.agent import triage

path = sys.argv[1] if len(sys.argv) > 1 else "data/labeled.json"
data = json.load(open(path))
p_ok = s_ok = 0
clear_p = clear_n = 0

for d in data:
    r = triage(d["text"], save_to_log=False)["result"]
    p_hit = r["principle"] == d["principle"]
    s_hit = r["severity"] == d["severity"]
    p_ok += p_hit
    s_ok += s_hit
    if not d.get("ambiguous", False):
        clear_n += 1
        clear_p += p_hit
    flag = "" if (p_hit and s_hit) else "  <-- MISS"
    print(f"{d['text'][:55]:55} | {r['principle']:24} {r['severity']:8}{flag}")

n = len(data)
print(f"\nFile: {path}")
print(f"Principle accuracy (all):        {p_ok}/{n} = {p_ok/n:.0%}")
if clear_n:
    print(f"Principle accuracy (clear only): {clear_p}/{clear_n} = {clear_p/clear_n:.0%}")
print(f"Severity accuracy (all):         {s_ok}/{n} = {s_ok/n:.0%}")
