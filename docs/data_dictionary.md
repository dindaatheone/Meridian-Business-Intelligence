# CHANGELOG - Meridian Business Intelligence

All notable changes to this repository documented
in reverse chronological order. Each entry records
what was added, why it matters, and what comes next.

---

## [0.6.0] - Business Report Layer

### Added
- 06_business_report/README.md - report structure,
  audience definition, connection to downstream repos
- 06_business_report/hypothesis_statement.md - four
  analytical hypotheses with business problem framing
  and confirmation/rejection implications
- 06_business_report/findings_summary.md - findings
  structure with KPIs for each recommendation

### Next
- Execute data_generation.py to populate CSVs
- Run PostgreSQL seed loader
- Execute all four SQL analysis files
- Run Python analysis scripts
- Complete findings with actual metric values
- Build Looker Studio dashboard
- Generate business_report.pdf

---

## [0.5.0] - Visualization Layer

### Added
- 05_visualization/README.md - dashboard structure,
  pipeline documentation, build sequence
- 05_visualization/looker_studio_link.md - page
  structure, data source mapping, access note
- 05_visualization/chart_notes.md - per-chart
  documentation for all 10 charts across three pages

---

## [0.4.0] - Python Analytical Pipeline

### Added
- 04_advanced_analysis/README.md - pipeline overview,
  tool rationale, run sequence
- 04_advanced_analysis/requirements.txt - pinned
  Python dependencies
- 04_advanced_analysis/data_generation.py - synthetic
  universe generator for all three CSVs
- 04_advanced_analysis/statistical_analysis.py -
  descriptive stats, correlation matrix, AUM distribution
- 04_advanced_analysis/credit_risk_scoring.py -
  DTI and DTC ratios, four-tier risk classification
- 04_advanced_analysis/forecasting_model.py -
  24-month AUM trend projection with confidence bounds

---

## [0.3.0] - SQL Analysis Layer

### Added
- 03_sql_analysis/README.md - query objectives,
  SQL concepts by level, execution order
- 03_sql_analysis/01_exploratory.sql - data quality
  validation, distributions, NULL checks, flag distributions
- 03_sql_analysis/02_joins_and_aggregations.sql -
  multi-table joins, AUM totals, RM productivity,
  corridor flows, FX exposure
- 03_sql_analysis/03_cte_window_functions.sql -
  AUM rankings, MoM change, rolling averages,
  decile distribution, cumulative inflows
- 03_sql_analysis/04_business_metrics.sql - six
  core private banking KPIs with business interpretation

---

## [0.2.0] - Database Architecture

### Added
- 02_database/README.md - relational logic, design
  decisions, setup instructions
- 02_database/schema.sql - three-table PostgreSQL
  schema with CHECK constraints and foreign keys
- 02_database/seed.sql - COPY loader with row count
  and referential integrity verification

---

## [0.1.0] - Foundation Layer

### Added
- README.md - master overview, institutional context,
  repo architecture, data spine, six KPIs, setup guide
- 00_bank_profile/README.md - section navigation
- 00_bank_profile/bank_identity.md - founding insight,
  jurisdiction rationale, five corridors, competitive
  positioning, regulatory context, ethical framework
- 00_bank_profile/client_tiers.md - HNW/VHNW/UHNW
  definitions, product access matrix, special flags,
  corridor profiles, KPI definitions
- 01_raw_data/README.md - synthetic universe parameters,
  generation rules, transaction and asset class reference
- 01_raw_data/clients.csv - header row defined
- 01_raw_data/portfolios.csv - header row defined
- 01_raw_data/transactions.csv - header row defined
- docs/data_dictionary.md - complete field definitions
  for all three tables with business meaning
- docs/methodology.md - tool selection rationale,
  data spine architecture, generation logic,
  SQL design principles, forecasting approach
- docs/CHANGELOG.md - this file