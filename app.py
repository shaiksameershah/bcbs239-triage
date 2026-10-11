import streamlit as st

from src.agent import triage

st.set_page_config(page_title="DQ Issue Triage Agent", layout="wide")
st.title("BCBS 239 Data Quality Issue Triage Agent")
st.caption("Synthetic data only. Local model. Low-confidence and critical issues are flagged for human review.")

text = st.text_area("Describe the data quality issue", height=140)

if st.button("Triage") and text.strip():
    with st.spinner("Analyzing..."):
        out = triage(text)
    r = out["result"]

    if out["needs_human_review"]:
        st.warning("Needs human review: " + "; ".join(out["review_reasons"]))
    if out["possible_duplicate"]:
        st.error("Possible duplicate or recurrence of an earlier issue")

    c1, c2, c3 = st.columns(3)
    c1.metric("Principle", r["principle"])
    c2.metric("Severity", r["severity"])
    c3.metric("Confidence", f"{r['confidence']:.0%}")

    st.write(f"**Root cause:** {r['root_cause']}")
    st.write(f"**Reasoning:** {r['severity_reasoning']}")
    st.write(f"**Owner:** {r['owner_type']}  |  **SLA:** {r['sla_days']} days")

    st.subheader("Remediation plan")
    for step in r["remediation_steps"]:
        st.markdown(f"- {step}")

    st.subheader("Similar past issues")
    if out["similar"]:
        for s in out["similar"]:
            st.write(f"{s['similarity']:.2f} | {s['principle']} | {s['text']}")
    else:
        st.write("No past issues logged yet.")
