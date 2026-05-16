-- Meridian Business Intelligence
-- Level 2: JOINs and Aggregations
-- Objective: Combine the three tables to answer multi-entity
-- business questions. AUM per client, RM productivity,
-- corridor flow analysis, mandate distribution.

-- ============================================================
-- SECTION 1: Client AUM and Transaction Summary
-- Question: What is each client's full financial footprint?
-- ============================================================

-- Total AUM, transaction count, and flow summary per client
SELECT
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction,
    c.assigned_rm,
    SUM(p.aum_usd)                                      AS total_aum_usd,
    COUNT(t.transaction_id)                             AS transaction_count,
    SUM(CASE WHEN t.transaction_type = 'Inflow'
        THEN t.amount_usd ELSE 0 END)                  AS total_inflows_usd,
    SUM(CASE WHEN t.transaction_type = 'Outflow'
        THEN ABS(t.amount_usd) ELSE 0 END)             AS total_outflows_usd,
    SUM(CASE WHEN t.transaction_type = 'Fee'
        THEN t.fee_amount_usd ELSE 0 END)              AS total_fees_usd
FROM clients c
JOIN portfolios p     ON c.client_id    = p.client_id
JOIN transactions t   ON p.portfolio_id = t.portfolio_id
GROUP BY
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction,
    c.assigned_rm
ORDER BY total_aum_usd DESC;


-- ============================================================
-- SECTION 2: RM Productivity
-- Question: How is AUM distributed across relationship managers?
-- ============================================================

-- AUM per RM and client count per RM
-- Interpretation: industry benchmark is USD 200M to 400M per RM
-- Below benchmark signals underperformance or onboarding phase
SELECT
    c.assigned_rm,
    COUNT(DISTINCT c.client_id)                         AS client_count,
    ROUND(SUM(p.aum_usd), 2)                           AS total_aum_usd,
    ROUND(AVG(p.aum_usd), 2)                           AS avg_aum_per_client,
    ROUND(SUM(p.aum_usd) / COUNT(DISTINCT c.client_id), 2) AS aum_per_client
FROM clients c
JOIN portfolios p ON c.client_id = p.client_id
WHERE c.is_active = TRUE
GROUP BY c.assigned_rm
ORDER BY total_aum_usd DESC;


-- ============================================================
-- SECTION 3: Corridor Flow Analysis
-- Question: How do inflows and outflows differ by jurisdiction?
-- ============================================================

-- Net flow by jurisdiction over full 24-month period
SELECT
    c.jurisdiction,
    COUNT(DISTINCT c.client_id)                         AS client_count,
    ROUND(SUM(p.aum_usd), 2)                           AS total_aum_usd,
    ROUND(SUM(CASE WHEN t.transaction_type = 'Inflow'
        THEN t.amount_usd ELSE 0 END), 2)              AS total_inflows,
    ROUND(SUM(CASE WHEN t.transaction_type = 'Outflow'
        THEN ABS(t.amount_usd) ELSE 0 END), 2)        AS total_outflows,
    ROUND(SUM(CASE WHEN t.transaction_type = 'Inflow'
        THEN t.amount_usd ELSE 0 END) -
    SUM(CASE WHEN t.transaction_type = 'Outflow'
        THEN ABS(t.amount_usd) ELSE 0 END), 2)        AS net_flow
FROM clients c
JOIN portfolios p     ON c.client_id    = p.client_id
JOIN transactions t   ON p.portfolio_id = t.portfolio_id
GROUP BY c.jurisdiction
ORDER BY total_aum_usd DESC;


-- ============================================================
-- SECTION 4: Mandate and Product Distribution
-- Question: How are mandates distributed across tiers?
-- ============================================================

-- Mandate type distribution by client tier
SELECT
    c.client_tier,
    p.mandate_type,
    COUNT(DISTINCT c.client_id)                         AS client_count,
    ROUND(SUM(p.aum_usd), 2)                           AS total_aum_usd
FROM clients c
JOIN portfolios p ON c.client_id = p.client_id
GROUP BY c.client_tier, p.mandate_type
ORDER BY c.client_tier, total_aum_usd DESC;


-- Shariah-compliant AUM as percentage of total
-- Interpretation: tracks Islamic finance book size for product planning
SELECT
    ROUND(SUM(CASE WHEN c.shariah_compliant_flag = TRUE
        THEN p.aum_usd ELSE 0 END), 2)                AS shariah_aum,
    ROUND(SUM(p.aum_usd), 2)                          AS total_aum,
    ROUND(SUM(CASE WHEN c.shariah_compliant_flag = TRUE
        THEN p.aum_usd ELSE 0 END) /
    SUM(p.aum_usd) * 100, 2)                          AS shariah_aum_pct
FROM clients c
JOIN portfolios p ON c.client_id = p.client_id;


-- ============================================================
-- SECTION 5: FX Exposure by Currency
-- Question: What is the currency concentration risk in the book?
-- ============================================================

-- Transaction volume by original currency
SELECT
    original_currency,
    COUNT(*)                                            AS transaction_count,
    ROUND(SUM(ABS(amount_usd)), 2)                    AS total_volume_usd,
    ROUND(AVG(ABS(amount_usd)), 2)                    AS avg_transaction_usd
FROM transactions
WHERE original_currency IS NOT NULL
GROUP BY original_currency
ORDER BY total_volume_usd DESC;