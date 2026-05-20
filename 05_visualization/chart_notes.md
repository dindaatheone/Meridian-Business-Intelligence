# Chart Notes - Meridian BI Dashboard

Per-chart documentation for every visual in the dashboard.
For each chart: the source query, the fields or filters applied,
and the business interpretation of what the chart is telling
a private banking analyst.

---

## Page 1 - Executive Overview

### Scorecard: Total AUM (USD)

Source: 04_business_metrics.sql, AUM growth rate query
Field: aum_end value from the growth rate CTE
Filter: none, shows total book AUM

The single most important number in private banking.
If this is flat or declining, every other metric is
secondary to understanding why.

### Line Chart: AUM Growth Trend

Source: 03_cte_window_functions.sql, monthly flows CTE
Fields: month on X axis, cumulative net flow on Y axis
Filter: none, full history

Slope is the health signal. Accelerating positive slope
means net new client acquisition and deepening relationships.
Flattening signals relationship stagnation before formal
churn occurs.

### Gauge: Concentration Risk

Source: 04_business_metrics.sql, concentration risk query
Field: top_10pct_concentration
Threshold: green below 30%, amber 30% to 40%, red above 40%

Above 40% means the top 10% of clients hold more than 40%
of total AUM. One large exit creates a revenue shock the
rest of the book cannot absorb quickly.

### Scorecard: Active Client Count

Source: 01_exploratory.sql, client count by tier query
Field: client_count where is_active = TRUE
Filter: is_active = TRUE

Context for AUM per client calculation. Declining client
count with stable AUM means remaining clients are deepening.
The opposite means top clients are leaving.

### Bar Chart: AUM by Client Tier

Source: 02_joins_and_aggregations.sql, client AUM summary
Fields: client_tier on X axis, total_aum_usd on Y axis
Filter: is_active = TRUE

UHNW should dominate AUM even when HNW dominates client count.
If HNW represents more than 30% of total AUM the book is
underpenetrated at the top.

---

## Page 2 - Client Analytics

### Bar Chart: AUM by Jurisdiction

Source: 02_joins_and_aggregations.sql, corridor flow analysis
Fields: jurisdiction on X axis, total_aum_usd on Y axis
Filter: is_active = TRUE

Validates corridor weighting against strategic targets.
China at 40% of AUM and Singapore at 25% is the target
distribution. Significant deviation signals either
outperformance in one corridor or underperformance that
needs RM attention.

### Pie Chart: Risk Profile Distribution

Source: 01_exploratory.sql, client count by tier
Fields: risk_appetite as dimension, client_count as metric

Moderate should be the modal risk profile. A book skewed
heavily to aggressive signals clients are chasing returns,
which creates churn risk when performance disappoints.
Conservative skew in UHNW is normal and expected for
capital preservation mandates.

### Churn Signal Clients

Source: 04_business_metrics.sql, churn detection query
Fields: full_name, client_tier, jurisdiction, assigned_rm,
last_inflow_date, days_since_inflow, current_aum_usd
Filter: days_since_inflow > 180
Sort: days_since_inflow descending

This is the early warning system. Every client on this
list is a relationship at risk. The RM should have
contacted each within the last 30 days. If not, that
is a governance failure, not a data finding.

### Bar Chart: Shariah Clients by Corridor

Source: 02_joins_and_aggregations.sql, Shariah AUM query
Fields: jurisdiction, shariah_clients, total_clients
Filter: jurisdiction IN (Indonesia, Brunei, Macau)

Tracks the Islamic finance book composition. Growing
Shariah client share in Indonesia and Brunei validates
the product sleeve investment. Flat numbers in these
corridors signal either product-market fit issues or
RM capability gaps.

---

## Page 3 - Transaction Intelligence

### Bar Chart: Monthly Inflow vs Outflow

Source: 03_cte_window_functions.sql, monthly flows CTE
Fields: month on X axis, inflows and outflows as grouped bars
Filter: transaction_type IN (Inflow, Outflow)

The gap between inflows and outflows is net new money.
Persistent outflow dominance signals portfolio liquidation,
either planned withdrawals or relationship deterioration.
Seasonal patterns in inflows often reflect bonus cycles
in the client base.

### Bar Chart: Fee Revenue by Type

Source: 04_business_metrics.sql, fee revenue decomposition
Fields: fee_type, total_fee_revenue, pct_of_total_fees
Filter: transaction_type = Fee

Management fee growth tracks AUM growth with a lag.
Performance fee contribution signals alpha generation.
Flat or declining management fees while AUM grows signals
pricing pressure or mandate migration to lower-fee structures.

### Ranked Bar Chart: Top 10 Clients by AUM

Source: 03_cte_window_functions.sql, AUM ranking CTE
Fields: full_name on Y axis, total_aum_usd on X axis
Filter: rank_overall <= 10
Sort: total_aum_usd descending

The ten names on this chart represent a disproportionate
share of total revenue. Each has a named RM accountable
for the relationship. This chart is reviewed monthly
at senior level.

### FX Exposure by Currency

Source: 02_joins_and_aggregations.sql, FX exposure query
Fields: original_currency, total_volume_usd, pct_of_total

CNY and IDR concentration signals sovereign risk beyond
pure market risk. Heavy IDR volume from Indonesia corridor
clients during periods of rupiah depreciation is a credit
risk indicator as well as a currency risk indicator.

### Churn Early Warning Scorecard

Source: 04_business_metrics.sql, churn detection query
Fields: count of at-risk clients, sum of AUM at risk

Headline numbers for the churn signal table above.
The AUM at risk figure is the revenue exposure if
every flagged client exits in the same quarter.
That scenario is unlikely but the number frames
the urgency of RM outreach.
