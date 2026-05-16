# Meridian Business Intelligence

**Singapore MAS Jurisdiction | Asia-Pacific | Boutique Private Banking**

---

## What This Is

This repository is the analytical foundation of Meridian Private Bank,
a Singapore-domiciled boutique private banking institution serving
HNW and UHNW clients across five Asia-Pacific corridors: China,
Singapore, Indonesia, Macau, and Brunei.

Every analytical decision here, from schema design to metric selection
to SQL architecture to Python modeling, is grounded in how private
banking actually generates and captures relationship intelligence.

The central thesis: a private bank generates more relationship
intelligence than it captures. The gap between what the data knows
and what the institution acts on is where AUM attrition begins,
concentration risk accumulates invisibly, and CLV is systematically
underestimated. This repo builds the infrastructure that closes that gap.

---

## What This Repo Proves

| Capability | Demonstration |
|---|---|
| Relational database design | PostgreSQL schema with full referential integrity - clients, portfolios, transactions |
| Synthetic data engineering | Python-generated Asia-Pacific private banking data universe |
| SQL analytical depth | Four-level progression: exploratory, joins, CTEs and window functions, business metrics |
| Statistical modeling | Descriptive analysis, correlation matrix, AUM distribution by tier and corridor |
| Credit risk scoring | DTI and DTC ratio model with four-tier risk classification |
| Time series forecasting | 24-month AUM trend projection with confidence interval bounds |
| Business intelligence | Looker Studio three-page dashboard - executive, client, transaction layers |
| Strategic communication | Executive-ready business report translating data into private banking decisions |

---

## The Institution

**Name:** Meridian Private Bank
**Legal Entity:** Meridian Capital Management Pte. Ltd.
**Jurisdiction:** Singapore - Monetary Authority of Singapore (MAS)
**Posture:** Boutique Asia-Pacific specialist
**Client Corridors:** China (40%), Singapore (25%), Indonesia (20%), Macau (10%), Brunei (5%)

**Client Tiers:**
- HNW: USD 1M to 5M investable assets
- VHNW: USD 5M to 30M investable assets
- UHNW: USD 30M and above

This repo is one of three that collectively constitute Meridian's
institutional infrastructure:

| Repo | Role |
|---|---|
| Meridian-Business-Intelligence | Client intelligence layer - this repo |
| Meridian-Monte-Carlo | Risk quantification layer |
| Meridian-Ventures | Capital deployment layer |

The client entity schema defined in this repo is the single source
of truth across all three. No field is added downstream without a
version update to the Meridian Strategic Master Guidebook.

---

## Repo Architecture

```
Meridian-Business-Intelligence/
|
|-- README.md                              <- Master overview, stack, KPIs, setup
|
|-- 00_bank_profile/
|   |-- README.md                          <- Section overview and navigation
|   |-- bank_identity.md                   <- Founding insight, jurisdiction, competitive positioning
|   +-- client_tiers.md                    <- HNW/VHNW/UHNW definitions, product access, special flags
|
|-- 01_raw_data/
|   |-- README.md                          <- Synthetic universe parameters and generation notes
|   |-- clients.csv                        <- 500 to 1,000 synthetic client records
|   |-- portfolios.csv                     <- Portfolio allocations and performance per client
|   +-- transactions.csv                   <- 24 months of monthly transaction history
|
|-- 02_database/
|   |-- README.md                          <- ERD explanation and schema design decisions
|   |-- schema.sql                         <- CREATE TABLE with constraints, types, foreign keys
|   |-- seed.sql                           <- COPY statements loading synthetic CSVs
|   +-- ERD.png                            <- Entity relationship diagram
|
|-- 03_sql_analysis/
|   |-- README.md                          <- Query objectives and execution order
|   |-- 01_exploratory.sql                 <- Data quality, distributions, NULL checks
|   |-- 02_joins_and_aggregations.sql      <- Multi-table joins, AUM totals, RM productivity
|   |-- 03_cte_window_functions.sql        <- Rankings, MoM change, rolling averages
|   +-- 04_business_metrics.sql            <- AUM growth, concentration risk, churn, CLV, FX
|
|-- 04_advanced_analysis/
|   |-- README.md                          <- Pipeline overview, why Python, run sequence
|   |-- requirements.txt                   <- All Python dependencies with pinned versions
|   |-- data_generation.py                 <- Generates all three synthetic CSVs
|   |-- statistical_analysis.py            <- Descriptive stats, correlation matrix, AUM distribution
|   |-- credit_risk_scoring.py             <- DTI and DTC ratios, four-tier risk classification
|   +-- forecasting_model.py               <- 24-month AUM trend projection with confidence bounds
|
|-- 05_visualization/
|   |-- README.md                          <- Dashboard structure, pipeline, design rationale
|   |-- looker_studio_link.md              <- Public dashboard URL and chart data sources
|   |-- chart_notes.md                     <- Per-chart source query, fields, interpretation
|   +-- dashboard_screenshot.png           <- Full three-page dashboard capture
|
|-- 06_business_report/
|   |-- README.md                          <- Report structure, audience, connection to other repos
|   |-- hypothesis_statement.md            <- Business problem and four analytical hypotheses
|   |-- findings_summary.md                <- Findings, implications, recommendations with KPIs
|   +-- business_report.pdf                <- Executive-ready final deliverable
|
+-- docs/
    |-- data_dictionary.md                 <- Every table, every column, data types, valid values
    |-- methodology.md                     <- Analytical approach, tool choices, pipeline rationale
    +-- CHANGELOG.md                       <- Version history as project builds
```
---

## The Data Spine

The synthetic data universe is generated from an immutable client
entity schema. Key fields across all three tables:

**clients:** client_id, jurisdiction, client_tier, investable_aum_usd,
primary_currency, product_mandate_type, risk_appetite,
shariah_compliant_flag, co_investment_eligible_flag,
annual_income_usd, total_debt_usd, assigned_rm

**portfolios:** portfolio_id, client_id, aum_usd, equity_pct,
fixed_income_pct, alternatives_pct, cash_pct, structured_pct,
private_credit_pct, performance_ytd, performance_inception

**transactions:** transaction_id, client_id, portfolio_id,
transaction_type, amount_usd, original_currency, fx_rate_applied,
asset_class, fee_amount_usd, fee_type

Full definitions in `docs/data_dictionary.md`.

---

## Six Core KPIs

| KPI | Formula | Private Banking Significance |
|---|---|---|
| AUM Growth Rate | (AUM_end - AUM_start) / AUM_start x 100 | Primary revenue driver - fees scale with AUM |
| Concentration Risk | Top 10% client AUM / Total AUM | Revenue fragility - high concentration means high churn exposure |
| Client Lifetime Value | Avg annual fee x expected tenure years | Relationship capital - guides RM resource allocation |
| Churn Rate | Clients lost / clients at start x 100 | Silent revenue erosion - detectable before formal exit |
| DTI Ratio | Total debt / gross annual income | Credit risk - signals over-leveraged client relationships |
| DTC Ratio | Total debt / total investable assets | Leverage risk - debt approaching asset base is critical signal |

---

## Setup and Reproduction

**Requirements:**
- Python 3.9+
- PostgreSQL local instance
- pip install -r 04_advanced_analysis/requirements.txt

**Run sequence:**

```bash
# 1. Generate synthetic data
python 04_advanced_analysis/data_generation.py

# 2. Initialize database
psql -U postgres -c "CREATE DATABASE meridian_bi;"
psql -U postgres -d meridian_bi -f 02_database/schema.sql
psql -U postgres -d meridian_bi -f 02_database/seed.sql

# 3. Run SQL analysis
psql -U postgres -d meridian_bi -f 03_sql_analysis/01_exploratory.sql
psql -U postgres -d meridian_bi -f 03_sql_analysis/04_business_metrics.sql

# 4. Run Python models
python 04_advanced_analysis/statistical_analysis.py
python 04_advanced_analysis/credit_risk_scoring.py
python 04_advanced_analysis/forecasting_model.py
```

All outputs are reproducible. No manual steps. No external credentials.

---

## Part of Meridian Private Bank

**Singapore MAS Jurisdiction | Asia-Pacific Focus | Version 1.0**

All data synthetic. Portfolio artifact. Not a licensed institution.
