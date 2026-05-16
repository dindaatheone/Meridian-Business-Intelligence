# Meridian Business Intelligence
# Statistical Analysis
# Descriptive statistics, correlation matrix,
# AUM distribution by tier and jurisdiction
#
# Input:  PostgreSQL meridian_bi database
# Output: outputs/statistical_summary.csv
#         outputs/correlation_matrix.png
#         outputs/aum_distribution.png

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Database Connection ───────────────────────────────────────
conn = psycopg2.connect(
    dbname   = "meridian_bi",
    user     = "postgres",
    password = "",
    host     = "localhost",
    port     = "5432"
)

# ── Load Data ─────────────────────────────────────────────────
clients_df = pd.read_sql("""
    SELECT
        c.client_id,
        c.jurisdiction,
        c.client_tier,
        c.investable_aum_usd,
        c.annual_income_usd,
        c.total_debt_usd,
        c.relationship_tenure_months,
        p.equity_pct,
        p.fixed_income_pct,
        p.alternatives_pct,
        p.cash_pct,
        p.structured_pct,
        p.private_credit_pct,
        p.performance_ytd
    FROM clients c
    JOIN portfolios p ON c.client_id = p.client_id
    WHERE c.is_active = TRUE
""", conn)

# ── Descriptive Statistics ────────────────────────────────────
numeric_cols = [
    'investable_aum_usd', 'annual_income_usd', 'total_debt_usd',
    'relationship_tenure_months', 'equity_pct', 'fixed_income_pct',
    'performance_ytd'
]

summary = clients_df[numeric_cols].describe().T
summary['median'] = clients_df[numeric_cols].median()
summary.to_csv(f"{OUTPUT_DIR}/statistical_summary.csv")
print("Statistical summary saved.")

# ── Correlation Matrix ────────────────────────────────────────
corr = clients_df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    corr,
    annot     = True,
    fmt       = ".2f",
    cmap      = "Blues",
    linewidths = 0.5,
    ax        = ax
)
ax.set_title(
    "Meridian BI - Correlation Matrix\nKey Client and Portfolio Variables",
    fontsize  = 13,
    pad       = 15
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=150)
plt.close()
print("Correlation matrix saved.")

# ── AUM Distribution by Tier ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# By tier
tier_order = ['HNW', 'VHNW', 'UHNW']
tier_aum = clients_df.groupby('client_tier')['investable_aum_usd'].sum()
tier_aum = tier_aum.reindex(tier_order)

axes[0].bar(
    tier_aum.index,
    tier_aum.values / 1_000_000,
    color = ['#1E3A5F', '#B8962E', '#8A9BB0']
)
axes[0].set_title("Total AUM by Client Tier (USD M)", fontsize=12)
axes[0].set_xlabel("Client Tier")
axes[0].set_ylabel("AUM (USD Millions)")

# By jurisdiction
juris_aum = clients_df.groupby('jurisdiction')['investable_aum_usd'].sum()
juris_aum = juris_aum.sort_values(ascending=False)

axes[1].bar(
    juris_aum.index,
    juris_aum.values / 1_000_000,
    color = '#1E3A5F'
)
axes[1].set_title("Total AUM by Jurisdiction (USD M)", fontsize=12)
axes[1].set_xlabel("Jurisdiction")
axes[1].set_ylabel("AUM (USD Millions)")
axes[1].tick_params(axis='x', rotation=15)

plt.suptitle(
    "Meridian Business Intelligence - AUM Distribution Analysis",
    fontsize = 14,
    y        = 1.02
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/aum_distribution.png", dpi=150)
plt.close()
print("AUM distribution chart saved.")

conn.close()
print("\nStatistical analysis complete. Outputs in outputs/")