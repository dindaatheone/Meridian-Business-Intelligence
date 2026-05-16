# Meridian Business Intelligence
# Credit Risk Scoring
# DTI and DTC ratio calculation
# Four-tier risk classification: A (Low), B (Moderate),
# C (High), D (Critical)
#
# Input:  PostgreSQL meridian_bi database
# Output: outputs/risk_scores.csv
#         outputs/risk_distribution.png

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# ── Load Client Data ──────────────────────────────────────────
df = pd.read_sql("""
    SELECT
        c.client_id,
        c.full_name,
        c.client_tier,
        c.jurisdiction,
        c.annual_income_usd,
        c.total_debt_usd,
        p.aum_usd
    FROM clients c
    JOIN portfolios p ON c.client_id = p.client_id
    WHERE c.is_active = TRUE
        AND c.annual_income_usd > 0
        AND p.aum_usd > 0
""", conn)

# ── Calculate Ratios ──────────────────────────────────────────
df['dti'] = df['total_debt_usd'] / df['annual_income_usd']
df['dtc'] = df['total_debt_usd'] / df['aum_usd']

# ── Risk Tier Assignment ──────────────────────────────────────
def assign_risk_tier(row):
    dti = row['dti']
    dtc = row['dtc']

    if dti > 0.70 or dtc > 0.70:
        return 'D - Critical'
    elif dti > 0.50 or dtc > 0.50:
        return 'C - High'
    elif dti > 0.30 or dtc > 0.20:
        return 'B - Moderate'
    else:
        return 'A - Low'

df['risk_tier'] = df.apply(assign_risk_tier, axis=1)

# ── Save Scores ───────────────────────────────────────────────
output_cols = [
    'client_id', 'full_name', 'client_tier', 'jurisdiction',
    'annual_income_usd', 'total_debt_usd', 'aum_usd',
    'dti', 'dtc', 'risk_tier'
]
df[output_cols].round(4).to_csv(
    f"{OUTPUT_DIR}/risk_scores.csv", index=False
)
print("Risk scores saved.")

# ── Risk Distribution Chart ───────────────────────────────────
tier_order  = ['A - Low', 'B - Moderate', 'C - High', 'D - Critical']
tier_colors = ['#2E7D32', '#B8962E', '#E65100', '#B71C1C']
tier_counts = df['risk_tier'].value_counts().reindex(tier_order, fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Client count by risk tier
axes[0].bar(
    tier_counts.index,
    tier_counts.values,
    color = tier_colors
)
axes[0].set_title("Client Count by Credit Risk Tier", fontsize=12)
axes[0].set_xlabel("Risk Tier")
axes[0].set_ylabel("Number of Clients")
axes[0].tick_params(axis='x', rotation=15)

# DTI vs DTC scatter
scatter_colors = {
    'A - Low':      '#2E7D32',
    'B - Moderate': '#B8962E',
    'C - High':     '#E65100',
    'D - Critical': '#B71C1C',
}
for tier in tier_order:
    subset = df[df['risk_tier'] == tier]
    axes[1].scatter(
        subset['dti'],
        subset['dtc'],
        label  = tier,
        color  = scatter_colors[tier],
        alpha  = 0.6,
        s      = 30
    )

axes[1].axvline(x=0.50, color='gray', linestyle='--', alpha=0.5)
axes[1].axhline(y=0.50, color='gray', linestyle='--', alpha=0.5)
axes[1].set_title("DTI vs DTC by Risk Tier", fontsize=12)
axes[1].set_xlabel("Debt-to-Income (DTI)")
axes[1].set_ylabel("Debt-to-Capital (DTC)")
axes[1].legend(fontsize=9)

plt.suptitle(
    "Meridian Business Intelligence - Credit Risk Scoring",
    fontsize = 14,
    y        = 1.02
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/risk_distribution.png", dpi=150)
plt.close()
print("Risk distribution chart saved.")

# ── Summary by Tier ───────────────────────────────────────────
summary = df.groupby('risk_tier').agg(
    client_count    = ('client_id',     'count'),
    avg_dti         = ('dti',           'mean'),
    avg_dtc         = ('dtc',           'mean'),
    total_aum_usd   = ('aum_usd',       'sum'),
).round(4)

print("\nCredit Risk Summary:")
print(summary.to_string())

conn.close()
print("\nCredit risk scoring complete. Outputs in outputs/")