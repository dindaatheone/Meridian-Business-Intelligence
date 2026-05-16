-- Meridian Business Intelligence
-- Level 4: Business Metrics
-- Objective: The six core private banking KPIs.
-- These are what a board monitors. Each query answers
-- one KPI with precision and includes the business
-- interpretation in the comment block.

-- ============================================================
-- METRIC 1: AUM Growth Rate
-- Formula: (AUM_end - AUM_start) / AUM_start x 100
-- Significance: primary revenue driver - fees scale with AUM
-- ============================================================

WITH period_aum AS (
    SELECT
        DATE_TRUNC('month', transaction_date)           AS month,
        SUM(CASE WHEN transaction_type = 'Inflow'
            THEN amount_usd ELSE 0 END) -
        SUM(CASE WHEN transaction_type = 'Outflow'
            THEN ABS(amount_usd) ELSE 0 END)           AS net_flow
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date)
),
cumulative AS (
    SELECT
        month,
        SUM(net_flow) OVER (ORDER BY month)            AS cumulative_aum
    FROM period_aum
)
SELECT
    MIN(cumulative_aum)                                 AS aum_start,
    MAX(cumulative_aum)                                 AS aum_end,
    ROUND(
        (MAX(cumulative_aum) - MIN(cumulative_aum)) /
        NULLIF(MIN(cumulative_aum), 0) * 100,
    2)                                                  AS aum_growth_rate_pct
FROM cumulative;


-- ============================================================
-- METRIC 2: Concentration Risk
-- Formula: Top 10% client AUM / Total AUM
-- Significance: above 40% is elevated risk - revenue is fragile
-- ============================================================

WITH client_aum AS (
    SELECT
        c.client_id,
        SUM(p.aum_usd)                                 AS total_aum
    FROM clients c
    JOIN portfolios p ON c.client_id = p.client_id
    GROUP BY c.client_id
),
deciled AS (
    SELECT
        client_id,
        total_aum,
        NTILE(10) OVER (ORDER BY total_aum DESC)       AS decile
    FROM client_aum
)
SELECT
    ROUND(
        SUM(CASE WHEN decile = 1 THEN total_aum ELSE 0 END) /
        NULLIF(SUM(total_aum), 0) * 100,
    2)                                                  AS top_10pct_concentration,
    CASE
        WHEN SUM(CASE WHEN decile = 1 THEN total_aum ELSE 0 END) /
             NULLIF(SUM(total_aum), 0) * 100 > 40
        THEN 'ELEVATED - revenue fragility risk'
        ELSE 'ACCEPTABLE - within threshold'
    END                                                 AS risk_assessment
FROM deciled;


-- ============================================================
-- METRIC 3: Churn Detection
-- Signal: no inflow in last 180 days on an active account
-- Significance: detectable before formal exit occurs
-- ============================================================

SELECT
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction,
    c.assigned_rm,
    MAX(t.transaction_date)                             AS last_inflow_date,
    CURRENT_DATE - MAX(t.transaction_date)             AS days_since_inflow,
    SUM(p.aum_usd)                                     AS current_aum_usd
FROM clients c
JOIN portfolios p     ON c.client_id    = p.client_id
JOIN transactions t   ON p.portfolio_id = t.portfolio_id
WHERE
    t.transaction_type  = 'Inflow'
    AND c.is_active     = TRUE
GROUP BY
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction,
    c.assigned_rm
HAVING CURRENT_DATE - MAX(t.transaction_date) > 180
ORDER BY days_since_inflow DESC;


-- ============================================================
-- METRIC 4: Client Lifetime Value
-- Formula: total fees collected / relationship years x 10
-- Significance: guides RM resource allocation decisions
-- ============================================================

WITH fee_revenue AS (
    SELECT
        c.client_id,
        SUM(ABS(t.fee_amount_usd))                     AS total_fees_collected
    FROM clients c
    JOIN portfolios p     ON c.client_id    = p.client_id
    JOIN transactions t   ON p.portfolio_id = t.portfolio_id
    WHERE t.transaction_type = 'Fee'
    GROUP BY c.client_id
),
tenure AS (
    SELECT
        client_id,
        EXTRACT(YEAR FROM AGE(
            COALESCE(exit_date, CURRENT_DATE),
            onboarding_date
        ))                                             AS relationship_years
    FROM clients
)
SELECT
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction,
    ROUND(f.total_fees_collected, 2)                   AS total_fees_usd,
    t.relationship_years,
    ROUND(f.total_fees_collected /
        NULLIF(t.relationship_years, 0), 2)            AS avg_annual_fee_usd,
    ROUND(f.total_fees_collected /
        NULLIF(t.relationship_years, 0) * 10, 2)      AS estimated_10yr_clv
FROM clients c
JOIN fee_revenue f   ON c.client_id = f.client_id
JOIN tenure t        ON c.client_id = t.client_id
ORDER BY estimated_10yr_clv DESC;


-- ============================================================
-- METRIC 5: Fee Revenue Decomposition
-- Question: What is the fee revenue breakdown by type?
-- Significance: performance fees signal alpha generation
-- management fees signal AUM scale
-- ============================================================

SELECT
    t.fee_type,
    COUNT(*)                                            AS transaction_count,
    ROUND(SUM(ABS(t.fee_amount_usd)), 2)              AS total_fee_revenue,
    ROUND(AVG(ABS(t.fee_amount_usd)), 2)              AS avg_fee_per_transaction,
    ROUND(SUM(ABS(t.fee_amount_usd)) /
        SUM(SUM(ABS(t.fee_amount_usd))) OVER () * 100, 2) AS pct_of_total_fees
FROM transactions t
WHERE t.transaction_type = 'Fee'
    AND t.fee_type IS NOT NULL
GROUP BY t.fee_type
ORDER BY total_fee_revenue DESC;


-- ============================================================
-- METRIC 6: FX Exposure by Currency and Corridor
-- Question: Where is the currency concentration risk?
-- Significance: CNY and IDR exposure carries sovereign
-- and political risk beyond pure market risk
-- ============================================================

SELECT
    c.jurisdiction,
    t.original_currency,
    COUNT(*)                                            AS transaction_count,
    ROUND(SUM(ABS(t.amount_usd)), 2)                  AS total_exposure_usd,
    ROUND(SUM(ABS(t.amount_usd)) /
        SUM(SUM(ABS(t.amount_usd))) OVER () * 100, 2) AS pct_of_total_exposure
FROM clients c
JOIN portfolios p     ON c.client_id    = p.client_id
JOIN transactions t   ON p.portfolio_id = t.portfolio_id
WHERE t.original_currency IS NOT NULL
    AND t.original_currency != 'USD'
GROUP BY c.jurisdiction, t.original_currency
ORDER BY total_exposure_usd DESC;