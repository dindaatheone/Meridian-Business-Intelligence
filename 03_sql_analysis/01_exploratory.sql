-- Meridian Business Intelligence
-- Level 1: Exploratory Analysis
-- Objective: Validate data quality and understand distributions
-- before any business analysis is run.
-- Every private banking dataset must be interrogated before trusted.

-- ============================================================
-- SECTION 1: Basic Counts
-- Question: What is the size and composition of the client base?
-- ============================================================

-- Client count by tier
-- Interpretation: tier distribution should reflect synthetic
-- universe parameters - HNW 50%, VHNW 35%, UHNW 15%
SELECT
    client_tier,
    COUNT(*)                                AS client_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM clients
GROUP BY client_tier
ORDER BY client_count DESC;


-- Client count by jurisdiction
-- Interpretation: should reflect corridor weights -
-- China 40%, Singapore 25%, Indonesia 20%, Macau 10%, Brunei 5%
SELECT
    jurisdiction,
    COUNT(*)                                AS client_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM clients
GROUP BY jurisdiction
ORDER BY client_count DESC;


-- Active vs inactive clients
-- Interpretation: churn rate approximation at population level
SELECT
    is_active,
    COUNT(*)    AS client_count
FROM clients
GROUP BY is_active;


-- ============================================================
-- SECTION 2: AUM Distributions
-- Question: What does the AUM landscape look like across tiers?
-- ============================================================

-- AUM statistics across all clients
-- Interpretation: mean vs median gap indicates skew from UHNW outliers
SELECT
    MIN(investable_aum_usd)                                     AS min_aum,
    MAX(investable_aum_usd)                                     AS max_aum,
    ROUND(AVG(investable_aum_usd), 2)                          AS avg_aum,
    PERCENTILE_CONT(0.5) WITHIN GROUP
        (ORDER BY investable_aum_usd)                          AS median_aum,
    ROUND(STDDEV(investable_aum_usd), 2)                       AS stddev_aum
FROM clients;


-- AUM statistics by tier
-- Interpretation: validates synthetic data tier thresholds
SELECT
    client_tier,
    COUNT(*)                                                    AS client_count,
    ROUND(MIN(investable_aum_usd), 2)                          AS min_aum,
    ROUND(MAX(investable_aum_usd), 2)                          AS max_aum,
    ROUND(AVG(investable_aum_usd), 2)                          AS avg_aum,
    ROUND(SUM(investable_aum_usd), 2)                          AS total_aum
FROM clients
GROUP BY client_tier
ORDER BY total_aum DESC;


-- ============================================================
-- SECTION 3: Data Quality Checks
-- Question: Are there integrity issues before analysis begins?
-- ============================================================

-- Clients with no portfolio (orphaned client records)
-- Interpretation: should return zero rows - any result is a data issue
SELECT
    c.client_id,
    c.full_name,
    c.client_tier,
    c.jurisdiction
FROM clients c
LEFT JOIN portfolios p ON c.client_id = p.client_id
WHERE p.portfolio_id IS NULL;


-- Portfolios with allocation percentages not summing to 100
-- Interpretation: allocation drift indicates generation script error
SELECT
    portfolio_id,
    client_id,
    ROUND(
        equity_pct + fixed_income_pct + alternatives_pct +
        cash_pct + structured_pct + private_credit_pct, 2
    )   AS total_allocation_pct
FROM portfolios
WHERE ROUND(
    equity_pct + fixed_income_pct + alternatives_pct +
    cash_pct + structured_pct + private_credit_pct, 2
) != 100.00;


-- NULL checks on critical client fields
-- Interpretation: any NULLs in these fields breaks downstream analysis
SELECT
    COUNT(*)                                            AS total_clients,
    COUNT(investable_aum_usd)                          AS has_aum,
    COUNT(client_tier)                                 AS has_tier,
    COUNT(jurisdiction)                                AS has_jurisdiction,
    COUNT(primary_currency)                            AS has_currency,
    COUNT(assigned_rm)                                 AS has_rm,
    COUNT(annual_income_usd)                           AS has_income,
    COUNT(total_debt_usd)                              AS has_debt
FROM clients;


-- ============================================================
-- SECTION 4: Special Flag Distributions
-- Question: How are Shariah and co-investment flags distributed?
-- ============================================================

-- Shariah-compliant clients by jurisdiction
-- Interpretation: should concentrate in Indonesia and Brunei
SELECT
    jurisdiction,
    COUNT(*)                                AS total_clients,
    SUM(CASE WHEN shariah_compliant_flag = TRUE
        THEN 1 ELSE 0 END)                 AS shariah_clients,
    ROUND(SUM(CASE WHEN shariah_compliant_flag = TRUE
        THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS shariah_pct
FROM clients
GROUP BY jurisdiction
ORDER BY shariah_pct DESC;


-- Co-investment eligible clients by tier
-- Interpretation: should be 100% for VHNW and UHNW, 0% for HNW
SELECT
    client_tier,
    COUNT(*)                                AS total_clients,
    SUM(CASE WHEN co_investment_eligible_flag = TRUE
        THEN 1 ELSE 0 END)                 AS eligible_clients,
    ROUND(SUM(CASE WHEN co_investment_eligible_flag = TRUE
        THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS eligible_pct
FROM clients
GROUP BY client_tier
ORDER BY client_tier;