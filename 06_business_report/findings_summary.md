# Findings Summary - Meridian Business Intelligence

## Overview

This document states the analytical findings across all five
layers of the Meridian BI project: SQL exploratory analysis,
SQL business metrics, Python statistical analysis, Python
credit risk scoring, and Python AUM forecasting.

Each finding is stated as a business conclusion, not a
technical observation. Each recommendation includes a KPI
that defines what success looks like and a timeframe.

Supporting charts and query outputs are in
04_advanced_analysis/outputs/ and 05_visualization/outputs/.

---

## Finding 1 - AUM Concentration Risk

**H1: Confirmed**

The top 10% of clients hold 58.35% of total book AUM.
This is significantly above the 40% elevated threshold
defined in the hypothesis.

At 58.35% concentration, the departure of two or three
top-decile clients in the same quarter would create a
revenue shock the remaining book cannot absorb without
a meaningful decline in total fee income. The book is
running implicit key-man risk on its largest relationships.

The China corridor drives the concentration. 40% of total
AUM originates from Chinese clients, and within that
corridor the UHNW tier is disproportionately concentrated
with a small number of relationships.

**Recommendation:**
Elevate RM accountability for every top-decile client to
senior level immediately. Increase review frequency to
monthly for the top 20 relationships by AUM. Begin
deliberate mid-market acquisition in Singapore and
Indonesia corridors to dilute concentration over 18 months.

**KPI:** Top decile concentration ratio reviewed monthly.
Target: below 45% within 12 months, below 35% within
24 months through corridor diversification.

---

## Finding 2 - Churn Signals

**H2: Confirmed**

The churn detection query identifies active clients with
no inflow recorded in the last 180 days. Every client on
that list represents a relationship that has gone silent
without formal exit. The 180-day window is a conservative
threshold. In practice the intervention window opens
earlier, typically around 90 days of inflow cessation,
before the relationship has fully disengaged.

The RM accountability structure matters here. Each flagged
client has an assigned RM. If that RM has not made contact
within the last 30 days, the flag is a governance failure
as much as a relationship risk.

**Recommendation:**
Run the churn detection query weekly as an operational
report. Route every newly flagged client to the assigned
RM within five business days. Document the intervention
and outcome in the relationship record. Track whether
contact restores inflow activity within 90 days.

**KPI:** Churn signal response rate. Target: 100% of
flagged clients contacted within five business days.
Secondary KPI: reduction in formal churn rate from
baseline over the following 12-month period.

---

## Finding 3 - Client Lifetime Value by Corridor

**H3: Confirmed with nuance**

CLV varies significantly by tier as expected. UHNW clients
generate disproportionately higher estimated 10-year fee
revenue than HNW clients at every corridor. This is
structurally predictable given AUM-based fee mechanics.

The corridor dimension produces a less intuitive result.
Singapore UHNW clients show higher average CLV than China
UHNW clients in several RM books, driven by longer average
tenure and higher management fee consistency. China UHNW
clients carry larger AUM but show more volatility in fee
revenue due to mandate migration patterns and periodic
large outflow events.

Brunei, despite representing 5% of client count, produces
CLV per client that is competitive with Singapore at the
VHNW tier. The corridor is underinvested relative to its
revenue contribution per relationship.

**Recommendation:**
Weight senior RM capacity toward Singapore and Brunei
for the VHNW and UHNW segments where tenure and fee
consistency are highest. Review China UHNW mandate
structures to reduce outflow volatility and improve
fee revenue predictability.

**KPI:** Revenue per RM by corridor reviewed quarterly.
Target: Singapore and Brunei corridors achieve 40% above
mean revenue per client within 18 months of reallocation.

---

## Finding 4 - Credit Risk Distribution

**H4: Confirmed with synthetic data qualification**

The credit risk scoring model assigns clients to four tiers
based on debt-to-income and debt-to-capital ratios.

Results from the 271-client active book:
- A Low:      25 clients  (9%)
- B Moderate: 21 clients  (8%)
- C High:     10 clients  (4%)
- D Critical: 215 clients (79%)

The D Critical concentration at 79% reflects a synthetic
data generation artifact. The generator applied debt
parameters uniformly without tier-based constraints,
producing DTI and DTC ratios that would not reflect a
real private banking book where UHNW clients typically
carry conservative leverage relative to their asset base.

In a production deployment, the credit risk model
architecture is correct. DTI and DTC thresholds are
standard private banking credit metrics. The four-tier
classification maps directly to facility review
protocols. The finding that validates is the model
structure, not the synthetic distribution.

**Recommendation:**
In production, apply tier-specific DTI caps to the
synthetic generator to produce a realistic credit
distribution. Restrict new credit extensions for any
client scoring D Critical. Require quarterly facility
review for C High clients. Flag correlated risk where
high DTI clients hold Lombard loans against equity
portfolios.

**KPI:** Credit risk tier distribution reviewed monthly.
Production target: D Critical clients below 5% of active
book. Alert threshold: any increase in D Critical share
above 7% triggers senior credit review.

---

## Finding 5 - AUM Trajectory and Forecast

**Additional finding beyond the four hypotheses.**

The 24-month cumulative net flow trend shows positive
AUM momentum throughout the observation period. The
6-month projection from the moving average model
estimates base case AUM reaching approximately USD 1.38B
by May 2026, with a 95% confidence interval ranging
from USD 1.21B to USD 1.55B.

The forecast is built on net flow momentum, not market
returns. It captures relationship-driven AUM change:
inflows from deepening relationships, outflows from
withdrawals, fee drag. It does not capture market
appreciation or depreciation on existing AUM.

The positive trajectory is consistent with a book in
healthy growth phase. The confidence interval widening
over the 6-month horizon reflects normal uncertainty
in client behavior, not structural instability.

**Recommendation:**
Monitor actual monthly net flow against the base case
projection. A single month below the lower confidence
bound warrants investigation. Two consecutive months
below the lower bound triggers a senior review of the
RM productivity and corridor acquisition pipeline.

**KPI:** Monthly AUM growth rate against 3-month moving
average baseline. Target: positive net flow in at least
10 of every 12 months. Alert threshold: two consecutive
months of net outflow triggers senior review.
