# 06 - Business Report

The analytical narrative of Meridian Business Intelligence.
Translates every data finding into a strategic recommendation
with a measurable KPI. This is the executive-facing layer
of the repo - written for a private banking MD, a PE analyst,
or a BD decision-maker who has not seen the underlying data.

---

## Files

| File | Purpose |
|---|---|
| hypothesis_statement.md | Business problem definition and four analytical hypotheses |
| findings_summary.md | What the data revealed across all five analytical layers |
| business_report.pdf | Executive-ready final deliverable - added after analysis complete |

---

## Audience

This report is not written for a technical reader.
Every SQL query, every Python model, every dashboard
chart gets translated into one of three things:

- A finding: what the data shows
- An implication: what it means for the business
- A recommendation: what to do about it, with a KPI
  that defines what success looks like

---

## Report Structure

1. Executive Summary - three findings, three recommendations
2. Business Problem and Hypotheses
3. Methodology Overview - data, tools, analytical approach
4. Findings by hypothesis - confirmed or rejected with evidence
5. Strategic Recommendations with KPIs
6. Appendix - key charts from Python dashboard outputs

---

## Connection to Other Repos

The findings in this report inform two downstream repos:

Meridian-Monte-Carlo uses the AUM distribution and
concentration risk findings as inputs to the macro
stress test scenarios.

Meridian-Ventures uses the CLV findings and corridor
AUM data to validate co-investment allocation logic
and deal sourcing priorities by jurisdiction.
