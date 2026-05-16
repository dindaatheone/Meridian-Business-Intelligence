# Methodology - Meridian Business Intelligence

Complete documentation of the analytical approach,
tool selection rationale, data spine architecture,
and pipeline design decisions. This document explains
why each choice was made, not just what was chosen.

---

## Analytical Architecture

Five-layer architecture. Each layer depends on the one
before it. No layer can be skipped.

| Layer | Tool | Purpose |
|---|---|---|
| 1 - Data Generation | Python - Faker, NumPy | Synthetic universe creation from immutable schema |
| 2 - Relational Database | PostgreSQL | Structured storage with referential integrity enforcement |
| 3 - SQL Analysis | PostgreSQL query engine | Four-level progression from data quality to business KPIs |
| 4 - Statistical Modeling | Python - pandas, scipy, matplotlib | Descriptive analysis, credit risk scoring, forecasting |
| 5 - Visualization | Looker Studio via Google Sheets | Executive-facing dashboard with public access |

---

## Tool Selection Rationale

### PostgreSQL over SQLite

PostgreSQL enforces referential integrity, CHECK constraints,
and complex data types at the database level. SQLite does not
enforce foreign key constraints by default and lacks the
statistical functions used in the SQL analysis files.
PostgreSQL is also the industry standard for institutional
data environments. It signals the right technical posture
for a private banking analytics project.

### Python over Excel

Reproducibility is the primary reason. Every output from
the Python scripts - the correlation matrix, the risk
scores, the AUM forecast - can be regenerated identically
by anyone who clones the repo and runs the scripts.
Excel outputs are not reproducible in this way. A reviewer
cannot verify an Excel model without the original file and
the same software version.

Version control is the second reason. Git diffs on Python
files show exactly what changed between versions. Git diffs
on Excel files are meaningless binary blobs.

Institutional signal is the third reason. Python-based
analytical pipelines are what PE firms, banks, and BD
teams use internally. Excel is a reporting tool. Python
is an analytical infrastructure tool.

### Looker Studio via Google Sheets Pipeline

Direct PostgreSQL connector to Looker Studio requires
database credentials that do not travel with the repo.
A reviewer cloning the project cannot reproduce the
dashboard without those credentials. The Google Sheets
pipeline eliminates that friction. SQL query results
are exported to CSV, imported to Google Sheets, and
Looker Studio connects to the sheet as its data source.
The dashboard URL is public. Any reviewer opens it
instantly with no setup required.

---

## Data Spine Architecture

The client entity schema is immutable at Guidebook v1.0.
This means no field is added to the clients, portfolios,
or transactions table without a version update to the
Meridian Strategic Master Guidebook and a corresponding
update to this methodology document and the data dictionary.

This constraint exists because two downstream repos draw
from the same schema:

Meridian-Monte-Carlo uses AUM distribution data,
portfolio allocation percentages, and FX exposure fields
as inputs to the macro stress test model.

Meridian-Ventures uses the co_investment_eligible_flag
and jurisdiction fields to drive co-investment allocation
logic and deal sourcing prioritization.

If the schema changes in this repo without coordination,
downstream repos break. The immutability constraint
prevents that failure mode.

---

## Synthetic Data Generation Logic

The data generation script enforces four rules that
make the synthetic universe analytically meaningful
rather than just numerically valid.

**Rule 1 - Tier threshold enforcement**
AUM values are drawn from ranges that respect tier
boundaries exactly. An HNW client never has AUM above
USD 5M. A UHNW client never has AUM below USD 30M.
This is enforced in the generation script, not just
documented as a target.

**Rule 2 - Transaction proportionality**
Transaction amounts are calculated as percentages of
the client's AUM, not as absolute values drawn from
a fixed distribution. An HNW client with USD 2M AUM
makes transactions scaled to that AUM. A UHNW client
with USD 80M AUM makes proportionally larger transactions.
This creates realistic variation in transaction size
across the client population.

**Rule 3 - Ratio distribution realism**
DTI and DTC ratios across the generated client population
follow a roughly normal distribution centered on 0.30 to
0.40. This reflects real private banking books where most
clients are moderately leveraged with a tail of high-risk
outliers. The tail is intentional - it makes the credit
risk scoring exercise analytically meaningful.

**Rule 4 - Flag consistency**
The shariah_compliant_flag is only set to TRUE for clients
in the Indonesia and Brunei jurisdictions. The
co_investment_eligible_flag is only set to TRUE for VHNW
and UHNW tier clients. These rules are enforced in the
generation script so the flag distributions in the
generated data match the institutional logic documented
in 00_bank_profile/client_tiers.md.

---

## SQL Analysis Design Principles

Every query in 03_sql_analysis answers a question with
a business consequence. The progression across four files
is deliberate.

Level 1 exploratory queries validate data before it is
trusted. No analysis is meaningful if the underlying
data has integrity issues. Checking for NULL values in
critical fields, orphaned records, and allocation
percentages that do not sum to 100 is not optional.

Level 2 join queries answer the first real business
questions by combining the three tables. AUM per client,
RM productivity, and corridor flow analysis all require
data from at least two tables.

Level 3 CTE and window function queries implement the
analytical patterns that characterize institutional-grade
SQL work: period-over-period comparison using LAG,
portfolio share using SUM OVER, ranking using RANK
OVER PARTITION BY, and smoothing using rolling averages.

Level 4 business metrics queries answer the six KPIs
that a private bank board monitors. These queries are
the analytical deliverables that justify the entire
data infrastructure below them.

---

## Forecasting Model Approach

The forecasting model uses a moving average projection
rather than ARIMA for two reasons.

First, 24 months of monthly data is a short series for
ARIMA. ARIMA requires sufficient history to estimate
autoregressive and moving average parameters reliably.
24 data points produce unstable parameter estimates
and wide confidence intervals that reduce the forecast's
interpretive value.

Second, the business question is directional, not
point-precise. A private banking MD reviewing AUM
trajectory needs to know whether the book is growing,
flattening, or contracting, and what the confidence
range around the projection looks like. A moving average
projection with a 95% confidence interval answers that
question clearly without requiring assumptions about
ARIMA order selection that would need to be defended
in a business context.

For a production system with 5 or more years of monthly
data, ARIMA or exponential smoothing would be appropriate.
That transition is documented here as the path forward
when data history grows.