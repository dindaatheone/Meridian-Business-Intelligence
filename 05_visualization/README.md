# 05 - Visualization

Python-generated dashboard from the Meridian BI data pipeline.
Three pages. Each page answers a distinct business question a
private bank leadership team would ask in a monthly review.

---

## Files

| File | Purpose |
|---|---|
| generate_charts.py | Generates all three dashboard pages from SQL output CSVs |
| chart_notes.md | Per-chart documentation: source query, fields, business interpretation |
| outputs/ | Generated PNG dashboard pages |

---

## Dashboard Structure

| Page | Title | Business Question |
|---|---|---|
| 1 | Executive Overview | What is the total AUM, growth trajectory, and concentration risk? |
| 2 | Client Analytics | How is the client base distributed and where are the churn signals? |
| 3 | Transaction Intelligence | What are the fee revenue trends and flow patterns by corridor? |

---

## Data Pipeline

Each SQL file in 03_sql_analysis maps to one or more charts.
The exact mapping is documented in chart_notes.md.

Run order:

1. Generate synthetic data: `python 01_raw_data/generate_synthetic_data.py`
2. Run SQL analysis: `python run_sql_analysis.py`
3. Generate charts: `python generate_charts.py`

All outputs land in 05_visualization/outputs/.

---

## Design Rationale

Direct Python pipeline over a BI tool connector: anyone cloning
the repo can reproduce every chart with one command. No credentials,
no external accounts, no setup beyond the requirements.txt.
The charts are committed outputs, not live dashboard links.
Reproducibility is the point.
