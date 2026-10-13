# Pass bar (written before running the gold evaluation)

Evaluation set: data/gold.json (hand-verified rows sampled from the locked test split).

- Critical recall >= 85%
- Severity accuracy >= 75%
- Principle accuracy >= 85%
- Under-triage rate <= 10%
- No more than 10% of critical issues may reach neither a critical label nor a human-review flag

Rules: the prompt, policies, and thresholds are not changed after seeing gold results
without evaluating on a new, unseen set.
