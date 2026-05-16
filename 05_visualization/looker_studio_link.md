# Looker Studio Dashboard - Meridian Business Intelligence

## Dashboard URL

> To be added after dashboard is built and published.
> Format: https://lookerstudio.google.com/reporting/[id]

## Access

Public view. No login required for portfolio reviewers.
No database credentials needed. Open the link and the
dashboard loads immediately.

## Pages

| Page | Title | Primary Charts |
|---|---|---|
| 1 | Executive Overview | Total AUM scorecard, AUM growth trend line, concentration risk gauge, client count by tier |
| 2 | Client Analytics | AUM by jurisdiction bar chart, tier distribution pie, risk profile breakdown, churn signal table |
| 3 | Transaction Intelligence | Monthly inflow vs outflow bar chart, fee revenue by type trend, top 10 clients by AUM ranked bar |

## Data Sources

Each page connects to a named sheet in the Meridian BI
Google Sheets workbook. Sheet names match the SQL files
they were generated from:

| Sheet Name | Source SQL File |
|---|---|
| exploratory | 01_exploratory.sql |
| joins_aggregations | 02_joins_and_aggregations.sql |
| cte_window | 03_cte_window_functions.sql |
| business_metrics | 04_business_metrics.sql |

## Screenshot

See dashboard_screenshot.png in this folder.
Added after dashboard build is complete.