# 03 - SQL Analysis

Four-level SQL progression from data quality validation
to private banking business metrics. Each file builds on
the previous. Each query answers a specific business question
a private bank analytics team would ask in practice.

---

## Files

| File | Level | Business Focus |
|---|---|---|
| 01_exploratory.sql | Foundation | Data quality, distributions, NULL checks, basic counts |
| 02_joins_and_aggregations.sql | Intermediate | Multi-table joins, AUM totals, RM productivity, corridor breakdown |
| 03_cte_window_functions.sql | Advanced | Rankings, period-over-period change, rolling averages, percentiles |
| 04_business_metrics.sql | Business | AUM growth, concentration risk, churn detection, CLV, fee revenue, FX exposure |

---

## Query Design Principles

Every query in this folder answers a question with a
business consequence, not a technical exercise.

Before writing any query the question is stated explicitly.
After the result the business interpretation is documented
in the comment block. This is what separates analytical
infrastructure from academic SQL practice.

---

## Execution Order

Run in sequence. Later files depend on data quality
confirmed by earlier files.

```bash
psql -U postgres -d meridian_bi -f 03_sql_analysis/01_exploratory.sql
psql -U postgres -d meridian_bi -f 03_sql_analysis/02_joins_and_aggregations.sql
psql -U postgres -d meridian_bi -f 03_sql_analysis/03_cte_window_functions.sql
psql -U postgres -d meridian_bi -f 03_sql_analysis/04_business_metrics.sql
```

---

## SQL Concepts by Level

**Level 1 - Exploratory**
SELECT, WHERE, GROUP BY, ORDER BY, COUNT, MIN, MAX, AVG,
LEFT JOIN for NULL detection, LIMIT

**Level 2 - Joins and Aggregations**
INNER JOIN across three tables, SUM, CASE WHEN, HAVING,
multi-dimension GROUP BY, subqueries

**Level 3 - CTEs and Window Functions**
WITH clause, RANK() OVER, ROW_NUMBER() OVER, LAG() OVER,
SUM() OVER, PARTITION BY, NTILE(), PERCENTILE_CONT()

**Level 4 - Business Metrics**
Full CTE chains, compound window functions, date arithmetic,
NULLIF for division safety, EXTRACT, DATE_TRUNC, COALESCE