# Chart Notes - Meridian BI Dashboard

Per-chart documentation for every visual in the
Looker Studio dashboard. For each chart: the source
SQL query, the calculated fields or filters applied,
and the business interpretation of what the chart
is telling a private banking analyst.

---

## Page 1 - Executive Overview

### Scorecard: Total AUM (USD)

- Source: 04_business_metrics.sql - AUM growth rate query
- Field: aum_end value from the growth rate CTE
- Filter: none - shows total book AUM
- Interpretation: the single most important number in
  private banking. If this is flat or declining, every
  other metric is secondary to understanding why.

### Line Chart: AUM Growth Trend (24 Months)

- Source: 03_cte_window_functions.sql - monthly flows CTE
- Fields: month on X axis, cumulative_aum on Y axis
- Filter: none - full 24-month history
- Interpretation: slope is the health signal. Accelerating
  positive slope means net new client acquisition and
  deepening relationships. Flattening signals relationship
  stagnation before formal churn occurs.

### Gauge: Concentration Risk

- Source: 04_business_metrics.sql - concentration risk query
- Field: top_10pct_concentration
- Threshold: green below 30%, amber 30% to 40%, red above 40%
- Interpretation: above 40% means the top 10% of clients
  hold more than 40% of total AUM. One large exit creates
  a revenue shock the rest of the book cannot absorb quickly.

### Scorecard: Active Client Count

- Source: 01_exploratory.sql - client count by tier query
- Field: SUM of client_count where is_active = TRUE
- Filter: is_active = TRUE
- Interpretation: context for AUM per client calculation.
  Declining client count with stable AUM means remaining
  clients are deepening. Opposite means top clients are leaving.

### Bar Chart: AUM by Client Tier

- Source: 02_joins_and_aggregations.sql - client AUM summary
- Fields: client_tier on X axis, total_aum_usd on Y axis
- Filter: is_active = TRUE
- Interpretation: UHNW should dominate AUM even if HNW
  dominates client count. If HNW represents more than 30%
  of total AUM the book is underpenetrated at the top.

---

## Page 2 - Client Analytics

### Bar Chart: AUM by Jurisdiction

- Source: 02_joins_and_aggregations.sql - corridor flow analysis
- Fields: jurisdiction on X axis, total_aum_usd on Y axis
- Filter: is_active = TRUE
- Interpretation: validates corridor weighting against
  strategic targets. China at 40% of AUM and Singapore
  at 25% is the target distribution. Significant deviation
  signals either outperformance in one corridor or
  underperformance that needs RM attention.

### Pie Chart: Risk Profile Distribution

- Source: 01_exploratory.sql - client count by tier
- Fields: risk_appetite as dimension, client_count as metric
- Interpretation: moderate should be the modal risk profile.
  A book skewed heavily to aggressive signals clients are
  chasing returns which creates churn risk when performance
  disappoints. Conservative skew in UHNW is normal and
  expected for capital preservation mandates.

### Table: Churn Signal Clients

- Source: 04_business_metrics.sql - churn detection query
- Fields: full_name, client_tier, jurisdiction, assigned_rm,
  last_inflow_date, days_since_inflow, current_aum_usd
- Filter: days_since_inflow > 180
- Sort: days_since_inflow descending
- Interpretation: this table is the early warning system.
  Every client on this list is a relationship at risk.
  RM should have contacted each within the last 30 days.
  If not, that is a governance failure, not a data finding.

### Bar Chart: Shariah AUM vs Total AUM by Jurisdiction

- Source: 02_joins_and_aggregations.sql - Shariah AUM query
- Fields: jurisdiction, shariah_aum, total_aum
- Filter: jurisdiction IN (Indonesia, Brunei)
- Interpretation: tracks the Islamic finance book size.
  Growing Shariah AUM in Indonesia and Brunei validates
  the product sleeve investment. Flat Shariah AUM in
  these corridors signals either product-market fit
  issues or RM capability gaps.

---

## Page 3 - Transaction Intelligence

### Bar Chart: Monthly Inflow vs Outflow

- Source: 03_cte_window_functions.sql - monthly flows CTE
- Fields: month on X axis, inflows and outflows as grouped bars
- Filter: transaction_type IN (Inflow, Outflow)
- Interpretation: the gap between inflows and outflows
  is net new money. Persistent outflow dominance signals
  portfolio liquidation events - either planned withdrawals
  or relationship deterioration. Seasonal patterns in
  inflows often reflect bonus cycles in the client base.

### Line Chart: Fee Revenue by Type (Monthly)

- Source: 04_business_metrics.sql - fee revenue decomposition
- Fields: month on X axis, total_fee_revenue by fee_type
- Filter: transaction_type = Fee
- Interpretation: management fee growth tracks AUM growth
  with a lag. Performance fee spikes signal alpha generation
  quarters. Flat or declining management fees while AUM
  grows signals pricing pressure or mandate migration to
  lower-fee structures.

### Ranked Bar Chart: Top 10 Clients by AUM

- Source: 03_cte_window_functions.sql - AUM ranking CTE
- Fields: full_name on Y axis, total_aum_usd on X axis
- Filter: rank_overall <= 10
- Sort: total_aum_usd descending
- Interpretation: the ten names on this chart represent
  a disproportionate share of total revenue. Each one
  has a named RM accountable for the relationship.
  This chart is reviewed monthly at senior level.

### Stacked Bar: Transaction Volume by Currency

- Source: 02_joins_and_aggregations.sql - FX exposure query
- Fields: original_currency as stack dimension,
  total_volume_usd as metric, month on X axis
- Interpretation: CNY and IDR concentration signals
  sovereign risk beyond pure market risk. Heavy IDR
  volume from Indonesia corridor clients during periods
  of rupiah depreciation is a credit risk indicator
  as well as a currency risk indicator.