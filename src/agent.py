import pathlib

from . import store
from .llm import classify, cosine, embed

POLICIES = pathlib.Path("data/policies.md").read_text()

SYSTEM = f"""You are a data governance analyst triaging data quality issues
against BCBS 239 principles.

Principle meanings:
- P2 = data architecture and lineage
- P3 = accuracy and integrity
- P4 = completeness
- P5 = timeliness
- P6 = adaptability

Rules:
- Use ONLY the control standards below to set severity, SLA, and remediation.
- Pick the single best-fitting principle.
- Be honest about confidence. Use a value below 0.6 when the issue is ambiguous
  or could fit more than one principle.
- Severity depends on impact on reporting, not on duration or record counts. Internal-only reports cap at medium. Follow the DQ-01 order exactly.

CONTROL STANDARDS:
{POLICIES}"""

DUP_THRESHOLD = 0.78
REVIEW_THRESHOLD = 0.7


def triage(issue_text: str, save_to_log: bool = True) -> dict:
    log = store.load()
    vec = embed(issue_text)

    # 1. Retrieve similar past issues
    scored = sorted(
        ((cosine(vec, e["embedding"]), e) for e in log),
        key=lambda x: x[0],
        reverse=True,
    )[:3]
    similar = [
        {
            "similarity": round(s, 3),
            "text": e["text"],
            "principle": e["result"]["principle"],
        }
        for s, e in scored
    ]

    # 2. Classify, score, and draft remediation grounded in the policy text
    context = ""
    if similar:
        context = "\n\nSimilar past issues:\n" + "\n".join(
            f"- ({x['principle']}) {x['text']}" for x in similar
        )
    result = classify(SYSTEM, f"Issue:\n{issue_text}{context}")

    # 3. Governance flags
    is_dup = bool(similar) and similar[0]["similarity"] >= DUP_THRESHOLD
    needs_review = result.confidence < REVIEW_THRESHOLD or result.severity == "critical"

    out = {
        "result": result.model_dump(),
        "similar": similar,
        "possible_duplicate": is_dup,
        "needs_human_review": needs_review,
    }

    if save_to_log:
        log.append({"text": issue_text, "embedding": vec, "result": out["result"]})
        store.save(log)
    return out