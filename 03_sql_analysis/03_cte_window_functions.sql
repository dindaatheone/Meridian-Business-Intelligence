-- Meridian Business Intelligence
-- Level 3: CTEs and Window Functions
-- Objective: Advanced analytical patterns for ranking,
-- trending, and period-over-period comparison.
-- These patterns are the foundation of private banking
-- performance attribution and client segmentation.

-- ============================================================
-- SECTION 1: AUM Ranking
-- Question: How does each client rank within their tier
-- and across the total book?
-- ============================================================

-- Client AUM rank within tier and as percentage of total book
WITH client_aum AS (
    SELECT
        c.client_id,
        c.full_name,
        c.client_tier,
        c.jurisdiction,
        c.assigned_rm,
        SUM(p.aum_usd)  AS total_aum
    FROM clients c
    JOIN portfolios p ON c.client_id = p.client_id
    GROUP BY
        c.client_id,
        c.full_name,
        c.client_tier,
        c.jurisdiction,
        c.assigned_rm
)
SELECT
    client_id,
    full_name,
    client_tier,
    jurisdiction,
    assigned_rm,
    ROUND(total_aum, 2)                                         AS total_aum_usd,
    RANK() OVER (
        PARTITION BY client_tier
        ORDER BY total_aum DESC
    )                                                           AS rank_within_tier,
    RANK() OVER (
        ORDER BY total_aum DESC
    )                                                           AS rank_overall,
    ROUND(total_aum / SUM(total_aum) OVER () * 100, 4)        AS pct_of_total_book
FROM client_aum
ORDER BY rank_overall;


-- ============================================================
-- SECTION 2: Month-over-Month AUM Change
-- Question: Is the book growing, stable, or contracting
-- on a monthly basis?
-- ============================================================

WITH monthly_flows AS (
    SELECT
        DATE_TRUNC('month', transaction_date)           AS month,
        SUM(CASE WHEN transaction_type = 'Inflow'
            THEN amount_usd ELSE 0 END)                AS inflows,
        SUM(CASE WHEN transaction_type = 'Outflow'
            THEN ABS(amount_usd) ELSE 0 END)           AS outflows,
        SUM(CASE WHEN transaction_type = 'Inflow'
            THEN amount_usd ELSE 0 END) -
        SUM(CASE WHEN transaction_type = 'Outflow'
            THEN ABS(amount_usd) ELSE 0 END)           AS net_flow
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date)
)
SELECT
    month,
    ROUND(inflows, 2)                                   AS inflows_usd,
    ROUND(outflows, 2)                                  AS outflows_usd,
    ROUND(net_flow, 2)                                  AS net_flow_usd,
    LAG(net_flow) OVER (ORDER BY month)                AS prev_month_net_flow,
    ROUND(
        (net_flow - LAG(net_flow) OVER (ORDER BY month)) /
        NULLIF(ABS(LAG(net_flow) OVER (ORDER BY month)), 0) * 100,
    2)                                                  AS mom_change_pct
FROM monthly_flows
ORDER BY month;


-- ============================================================
-- SECTION 3: Rolling 3-Month Average Net Flow
-- Question: What is the smoothed AUM momentum trend?
-- ============================================================

WITH monthly_flows AS (
    SELECT
        DATE_TRUNC('month', transaction_date)           AS month,
        SUM(CASE WHEN transaction_type = 'Inflow'
            THEN amount_usd ELSE 0 END) -
        SUM(CASE WHEN transaction_type = 'Outflow'
            THEN ABS(amount_usd) ELSE 0 END)           AS net_flow
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date)
)
SELECT
    month,
    ROUND(net_flow, 2)                                  AS net_flow_usd,
    ROUND(AVG(net_flow) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                                               AS rolling_3m_avg
FROM monthly_flows
ORDER BY month;


-- ============================================================
-- SECTION 4: Client AUM Decile Distribution
-- Question: How concentrated is AUM across the client base?
-- ============================================================

WITH client_aum AS (
    SELECT
        c.client_id,
        c.client_tier,
        SUM(p.aum_usd)  AS total_aum
    FROM clients c
    JOIN portfolios p ON c.client_id = p.client_id
    GROUP BY c.client_id, c.client_tier
),
deciled AS (
    SELECT
        client_id,
        client_tier,
        total_aum,
        NTILE(10) OVER (ORDER BY total_aum DESC)    AS decile
    FROM client_aum
)
SELECT
    decile,
    COUNT(*)                                            AS client_count,
    ROUND(SUM(total_aum), 2)                           AS decile_aum,
    ROUND(SUM(total_aum) / SUM(SUM(total_aum))
        OVER () * 100, 2)                              AS pct_of_total_aum
FROM deciled
GROUP BY decile
ORDER BY decile;


-- ============================================================
-- SECTION 5: Cumulative Inflows per Client Since Onboarding
-- Question: Which clients are deepening their relationship
-- over time versus those who are static?
-- ============================================================

SELECT
    c.client_id,
    c.full_name,
    c.client_tier,
    t.transaction_date,
    t.amount_usd                                        AS inflow_usd,
    SUM(t.amount_usd) OVER (
        PARTITION BY c.client_id
        ORDER BY t.transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                   AS cumulative_inflows
FROM clients c
JOIN portfolios p     ON c.client_id    = p.client_id
JOIN transactions t   ON p.portfolio_id = t.portfolio_id
WHERE t.transaction_type = 'Inflow'
ORDER BY c.client_id, t.transaction_date;