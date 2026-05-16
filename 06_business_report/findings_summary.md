# Findings Summary - Meridian Business Intelligence

## Overview

This document summarizes the analytical findings across
all five layers of the Meridian BI project: SQL exploratory
analysis, SQL business metrics, Python statistical analysis,
Python credit risk scoring, and Python AUM forecasting.

Each finding is stated as a business conclusion, not a
technical observation. Each recommendation includes a KPI
that defines what success looks like and a timeframe.

Full supporting charts and query outputs are in the
Looker Studio dashboard and the outputs folder.

---

## Finding 1 - AUM Concentration Risk

**Hypothesis H1: Confirmed or Rejected**
To be completed after data generation and SQL execution.

**What the data shows:**
The top_10pct_concentration metric from 04_business_metrics.sql
returns [value to be inserted after execution].

**Business implication:**
[To be completed after execution]

**Recommendation:**
[To be completed after execution]

**KPI:** Top decile concentration ratio reviewed monthly.
Target: below 35% within 12 months through deliberate
mid-market client acquisition in Singapore and Indonesia corridors.

---

## Finding 2 - Churn Signal Detection

**Hypothesis H2: Confirmed or Rejected**
To be completed after data generation and SQL execution.

**What the data shows:**
The churn detection query from 04_business_metrics.sql
identifies [n] active clients with no inflow in 180 days.

**Business implication:**
[To be completed after execution]

**Recommendation:**
Implement weekly churn signal monitoring. Route flagged
clients to assigned RM within five business days.
Document intervention and outcome in CRM.

**KPI:** Churn signal response rate. Target: 100% of flagged
clients contacted within five business days of threshold.
Measure: reduction in formal churn rate from baseline
over the following 12-month period.

---

## Finding 3 - Client Lifetime Value by Corridor

**Hypothesis H3: Confirmed or Rejected**
To be completed after data generation and SQL execution.

**What the data shows:**
The CLV approximation from 04_business_metrics.sql shows
estimated 10-year CLV stratified by jurisdiction and tier.

**Business implication:**
[To be completed after execution]

**Recommendation:**
Restructure RM assignment weighting based on CLV findings.
Highest CLV corridors receive senior RM capacity first.

**KPI:** Revenue per RM by corridor. Reviewed quarterly.
Target: top-CLV corridor generates 40% above mean
revenue per client within 18 months of reallocation.

---

## Finding 4 - Credit Risk Distribution

**Hypothesis H4: Confirmed or Rejected**
To be completed after data generation and SQL execution.

**What the data shows:**
The credit risk scoring model from credit_risk_scoring.py
assigns [n] clients to tier C or D out of [total] active clients.

**Business implication:**
[To be completed after execution]

**Recommendation:**
Restrict new credit extensions for tier D clients immediately.
Require quarterly facility review for tier C clients.
Flag correlated risk where high DTI clients hold Lombard loans.

**KPI:** Credit risk tier distribution reviewed monthly.
Target: tier D clients below 3% of active book within 6 months
through facility restructuring or client exit.

---

## Finding 5 - AUM Trajectory

**Additional finding beyond the four hypotheses.**

**What the data shows:**
The 24-month cumulative AUM trend and 6-month projection
from forecasting_model.py shows [trajectory description
to be completed after execution].

**Business implication:**
[To be completed after execution]

**Recommendation:**
[To be completed after execution]

**KPI:** Monthly AUM growth rate against 3-month moving
average baseline. Target: positive net flow in at least
10 of every 12 months. Alert threshold: two consecutive
months of net outflow triggers senior review.

---

## Note on Findings Completion

All findings marked as placeholder above are completed
after the following steps are executed in sequence:

1. python 04_advanced_analysis/data_generation.py
2. psql seed loader for all three tables
3. All four SQL analysis files executed
4. python statistical_analysis.py
5. python credit_risk_scoring.py
6. python forecasting_model.py

Actual metric values replace placeholders.
Hypothesis confirmation or rejection is stated explicitly.
Charts from outputs folder are embedded in business_report.pdf.