-- Meridian Business Intelligence
-- PostgreSQL Database Schema
-- Version 1.0
-- Single source of truth for all three Meridian repos

-- ============================================================
-- TABLE: clients
-- One record per client relationship
-- ============================================================

CREATE TABLE clients (
    client_id                   SERIAL          PRIMARY KEY,
    full_name                   VARCHAR(100)    NOT NULL,
    jurisdiction                VARCHAR(50)     NOT NULL
                                CHECK (jurisdiction IN (
                                    'China',
                                    'Singapore',
                                    'Indonesia',
                                    'Macau',
                                    'Brunei'
                                )),
    date_of_birth               DATE,
    onboarding_date             DATE            NOT NULL,
    client_tier                 VARCHAR(10)     NOT NULL
                                CHECK (client_tier IN (
                                    'HNW',
                                    'VHNW',
                                    'UHNW'
                                )),
    investable_aum_usd          NUMERIC(18,2)   NOT NULL,
    primary_currency            VARCHAR(5)
                                CHECK (primary_currency IN (
                                    'CNY',
                                    'SGD',
                                    'IDR',
                                    'USD',
                                    'BND'
                                )),
    product_mandate_type        VARCHAR(20)
                                CHECK (product_mandate_type IN (
                                    'Discretionary',
                                    'Advisory',
                                    'Execution-Only'
                                )),
    risk_appetite               VARCHAR(15)
                                CHECK (risk_appetite IN (
                                    'Conservative',
                                    'Moderate',
                                    'Aggressive'
                                )),
    shariah_compliant_flag      BOOLEAN         DEFAULT FALSE,
    relationship_tenure_months  INT             DEFAULT 0,
    assigned_rm                 VARCHAR(100),
    co_investment_eligible_flag BOOLEAN         DEFAULT FALSE,
    last_rebalancing_date       DATE,
    annual_income_usd           NUMERIC(18,2),
    total_debt_usd              NUMERIC(18,2),
    is_active                   BOOLEAN         DEFAULT TRUE,
    exit_date                   DATE
);

-- ============================================================
-- TABLE: portfolios
-- One record per client portfolio
-- ============================================================

CREATE TABLE portfolios (
    portfolio_id                SERIAL          PRIMARY KEY,
    client_id                   INT             NOT NULL
                                REFERENCES clients(client_id),
    portfolio_name              VARCHAR(100),
    inception_date              DATE            NOT NULL,
    base_currency               VARCHAR(5)      DEFAULT 'USD',
    mandate_type                VARCHAR(20)
                                CHECK (mandate_type IN (
                                    'Discretionary',
                                    'Advisory',
                                    'Execution-Only'
                                )),
    aum_usd                     NUMERIC(18,2),
    equity_pct                  NUMERIC(5,2),
    fixed_income_pct            NUMERIC(5,2),
    alternatives_pct            NUMERIC(5,2),
    cash_pct                    NUMERIC(5,2),
    structured_pct              NUMERIC(5,2),
    private_credit_pct          NUMERIC(5,2),
    benchmark                   VARCHAR(50),
    performance_ytd             NUMERIC(8,4),
    performance_inception       NUMERIC(8,4),
    last_valuation_date         DATE
);

-- ============================================================
-- TABLE: transactions
-- One record per transaction event
-- ============================================================

CREATE TABLE transactions (
    transaction_id              SERIAL          PRIMARY KEY,
    client_id                   INT             NOT NULL
                                REFERENCES clients(client_id),
    portfolio_id                INT             NOT NULL
                                REFERENCES portfolios(portfolio_id),
    transaction_date            DATE            NOT NULL,
    transaction_type            VARCHAR(30)
                                CHECK (transaction_type IN (
                                    'Inflow',
                                    'Outflow',
                                    'Fee',
                                    'Dividend',
                                    'Interest',
                                    'Rebalance',
                                    'FX-Conversion'
                                )),
    amount_usd                  NUMERIC(18,2),
    original_currency           VARCHAR(5),
    fx_rate_applied             NUMERIC(12,6),
    asset_class                 VARCHAR(30)
                                CHECK (asset_class IN (
                                    'Equities',
                                    'Fixed Income',
                                    'Alternatives',
                                    'Cash',
                                    'Structured Products',
                                    'Private Credit'
                                )),
    fee_amount_usd              NUMERIC(18,2),
    fee_type                    VARCHAR(30)
                                CHECK (fee_type IN (
                                    'Management Fee',
                                    'Performance Fee',
                                    'Advisory Fee',
                                    'Transaction Fee',
                                    NULL
                                )),
    rm_id                       VARCHAR(100),
    notes                       TEXT
);