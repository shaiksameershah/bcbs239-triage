# Data Quality Control Standards (fictional, for demo only)

## DQ-01 Severity and SLA
- Critical: affects regulatory reporting or risk aggregation and no workaround exists. SLA 5 days.
- High: affects a critical data element (CDE) but a workaround exists. SLA 15 days.
- Medium: affects internal management reporting only. SLA 45 days.
- Low: cosmetic, documentation, or naming issues. SLA 90 days.

## DQ-02 Lineage
Every CDE must have documented end-to-end lineage. A lineage break is raised to the data owner of the source system and the architecture team. Remediation includes re-documenting lineage and adding automated lineage checks.

## DQ-03 Accuracy and reconciliation
CDEs must be reconciled between source and consuming report at each reporting cycle. Breaks above tolerance require root cause analysis and a corrective adjustment with second-reviewer sign-off.

## DQ-04 Completeness
Missing records or null values in CDEs above 1 percent require an incident ticket. Remediation includes backfilling, adding completeness checks at ingestion, and confirming downstream impact.

## DQ-05 Timeliness
Feeds supporting risk reports must arrive before the agreed cutoff. Repeated late delivery (3 times in 30 days) is escalated to the feed owner's management. Remediation includes SLA monitoring and alerting.

## DQ-06 Manual processes
Manual adjustments require a ticket, a second reviewer, and a retirement plan with a target automation date.

## DQ-07 Transformation logic
Changes to transformation rules require testing against a baseline, documented approval, and a regression check on downstream reports.

## DQ-08 Adaptability
Data architecture must support ad hoc and stress-test requests within agreed turnaround. Gaps are raised to the data platform owner with a capacity plan.

## DQ-09 Ownership
Every issue is assigned to a named owner type: data owner, data steward, technology owner, or process owner. Issues with unclear ownership default to the data steward.

## DQ-10 Recurrence
An issue that recurs within 90 days of closure is reopened and reviewed for root cause, not simply fixed again.