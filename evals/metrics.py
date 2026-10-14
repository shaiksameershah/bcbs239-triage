ORDER = ["low", "medium", "high", "critical"]


def report(gp, gs, pp, ps, review=None, label=""):
    n = len(gs)
    print(f"\n--- {label} (n={n}) ---")
    print(f"principle accuracy {sum(a == b for a, b in zip(gp, pp)) / n:.0%}")
    print(f"severity accuracy  {sum(a == b for a, b in zip(gs, ps)) / n:.0%}")
    under = sum(ORDER.index(p) < ORDER.index(g) for g, p in zip(gs, ps))
    over = sum(ORDER.index(p) > ORDER.index(g) for g, p in zip(gs, ps))
    print(f"under-triage {under / n:.0%} | over-triage {over / n:.0%}")
    crit = [i for i, g in enumerate(gs) if g == "critical"]
    if crit:
        hit = sum(ps[i] == "critical" for i in crit)
        print(f"critical recall {hit}/{len(crit)} = {hit / len(crit):.0%}")
        if review is not None:
            esc = sum(not review[i] for i in crit)
            print(f"critical issues with no critical label and no review flag: {esc}/{len(crit)}")
    print("confusion (rows = gold, columns = predicted):", ORDER)
    for g in ORDER:
        print(f"  {g:9}", [sum(1 for a, b in zip(gs, ps) if a == g and b == p) for p in ORDER])
