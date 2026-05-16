# 05 - Visualization

Looker Studio dashboard connected to Meridian BI data
via Google Sheets pipeline. Three pages. Each page answers
a distinct business question a private bank leadership
team would ask in a monthly review.

---

## Files

| File | Purpose |
|---|---|
| looker_studio_link.md | Public dashboard URL and access note |
| chart_notes.md | Per-chart documentation - source query, fields, business interpretation |
| dashboard_screenshot.png | Full dashboard capture - added after build |

---

## Dashboard Structure

| Page | Title | Business Question |
|---|---|---|
| 1 | Executive Overview | What is the total AUM, growth trajectory, and concentration risk? |
| 2 | Client Analytics | How is the client base distributed and where are the churn signals? |
| 3 | Transaction Intelligence | What are the fee revenue trends and flow patterns by corridor? |

---

## Data Pipeline

Each SQL file in 03_sql_analysis maps to one or more
charts in the dashboard. The exact mapping is documented
in chart_notes.md.

---

## Build Sequence

1. Run all four SQL files in 03_sql_analysis
2. Export each result set to CSV
3. Import CSVs into Google Sheets
   - One sheet per SQL query result
   - Name each sheet to match the SQL file it came from
4. Connect Looker Studio to the Google Sheets file
   - Add data source: Google Sheets
   - Select the workbook
5. Build charts on each page using the sheet as source
6. Publish dashboard with public access
7. Copy URL into looker_studio_link.md
8. Screenshot full dashboard into dashboard_screenshot.png

---

## Design Rationale

Google Sheets pipeline over direct PostgreSQL connector:
portfolio reviewers can open the dashboard without
database credentials. The dashboard is fully public
and reproducible by anyone with the repo and a
Google account. No access friction. No setup required
beyond running the SQL and importing the results.

