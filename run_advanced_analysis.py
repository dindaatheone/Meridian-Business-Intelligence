# Meridian Business Intelligence
# Advanced Analysis Runner
# Statistical analysis, credit risk scoring, AUM forecasting
# Reads from CSV outputs - no database required
#
# Input:  01_raw_data/clients.csv
#         01_raw_data/portfolios.csv
#         01_raw_data/transactions.csv
#         03_sql_analysis/outputs/03_cte_window_functions/monthly_flows.csv
#
# Output: 04_advanced_analysis/outputs/
#         statistical_summary.csv
#         correlation_matrix.png
#         aum_distribution.png
#         risk_scores.csv
#         risk_distribution.png
#         aum_forecast.png
#         forecast_summary.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import timedelta

OUTPUT_DIR = "04_advanced_analysis/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NAVY     = '#1E3A5F'
GOLD     = '#B8962E'
GREEN    = '#2E7D32'
AMBER    = '#E65100'
RED      = '#B71C1C'
GREY     = '#8A9BB0'

clients      = pd.read_csv("01_raw_data/clients.csv", parse_dates=['onboarding_date', 'exit_date'])
portfolios   = pd.read_csv("01_raw_data/portfolios.csv")
transactions = pd.read_csv("01_raw_data/transactions.csv", parse_dates=['transaction_date'])
monthly      = pd.read_csv("03_sql_analysis/outputs/03_cte_window_functions/monthly_flows.csv")

print("Meridian Business Intelligence - Advanced Analysis Runner")

# ══════════════════════════════════════════════════════════════
# STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\nRunning statistical analysis...")

cp = clients[clients['is_active'] == True].merge(portfolios, on='client_id')

numeric_cols = [
    'investable_aum_usd', 'annual_income_usd', 'total_debt_usd',
    'relationship_tenure_months', 'equity_pct', 'fixed_income_pct',
    'performance_ytd'
]

summary = cp[numeric_cols].describe().T
summary['median'] = cp[numeric_cols].median()
summary.to_csv(f"{OUTPUT_DIR}/statistical_summary.csv")
print("  Statistical summary saved.")

corr = cp[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    corr, annot=True, fmt=".2f",
    cmap="Blues", linewidths=0.5, ax=ax
)
ax.set_title(
    "Meridian BI - Correlation Matrix\nKey Client and Portfolio Variables",
    fontsize=13, pad=15
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=150)
plt.close()
print("  Correlation matrix saved.")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

tier_order = ['HNW', 'VHNW', 'UHNW']
tier_aum = cp.groupby('client_tier')['investable_aum_usd'].sum().reindex(tier_order)
axes[0].bar(tier_aum.index, tier_aum.values / 1_000_000,
            color=[NAVY, GOLD, GREY])
axes[0].set_title("Total AUM by Client Tier (USD M)", fontsize=12)
axes[0].set_xlabel("Client Tier")
axes[0].set_ylabel("AUM (USD Millions)")

juris_aum = cp.groupby('jurisdiction')['investable_aum_usd'].sum().sort_values(ascending=False)
axes[1].bar(juris_aum.index, juris_aum.values / 1_000_000, color=NAVY)
axes[1].set_title("Total AUM by Jurisdiction (USD M)", fontsize=12)
axes[1].set_xlabel("Jurisdiction")
axes[1].set_ylabel("AUM (USD Millions)")
axes[1].tick_params(axis='x', rotation=15)

plt.suptitle("Meridian Business Intelligence - AUM Distribution Analysis",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/aum_distribution.png", dpi=150)
plt.close()
print("  AUM distribution chart saved.")

# ══════════════════════════════════════════════════════════════
# CREDIT RISK SCORING
# ══════════════════════════════════════════════════════════════
print("\nRunning credit risk scoring...")

df = clients[
    (clients['is_active'] == True) &
    (clients['annual_income_usd'] > 0)
].merge(portfolios[['client_id', 'aum_usd']], on='client_id')

df = df[df['aum_usd'] > 0].copy()

df['dti'] = df['total_debt_usd'] / df['annual_income_usd']
df['dtc'] = df['total_debt_usd'] / df['aum_usd']

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

output_cols = [
    'client_id', 'full_name', 'client_tier', 'jurisdiction',
    'annual_income_usd', 'total_debt_usd', 'aum_usd',
    'dti', 'dtc', 'risk_tier'
]
df[output_cols].round(4).to_csv(f"{OUTPUT_DIR}/risk_scores.csv", index=False)
print("  Risk scores saved.")

tier_order_risk  = ['A - Low', 'B - Moderate', 'C - High', 'D - Critical']
tier_colors_risk = [GREEN, GOLD, AMBER, RED]
tier_counts = df['risk_tier'].value_counts().reindex(tier_order_risk, fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].bar(tier_counts.index, tier_counts.values, color=tier_colors_risk)
axes[0].set_title("Client Count by Credit Risk Tier", fontsize=12)
axes[0].set_xlabel("Risk Tier")
axes[0].set_ylabel("Number of Clients")
axes[0].tick_params(axis='x', rotation=15)

scatter_colors = {
    'A - Low':      GREEN,
    'B - Moderate': GOLD,
    'C - High':     AMBER,
    'D - Critical': RED,
}
for tier in tier_order_risk:
    subset = df[df['risk_tier'] == tier]
    axes[1].scatter(subset['dti'], subset['dtc'],
                    label=tier, color=scatter_colors[tier], alpha=0.6, s=30)

axes[1].axvline(x=0.50, color='gray', linestyle='--', alpha=0.5)
axes[1].axhline(y=0.50, color='gray', linestyle='--', alpha=0.5)
axes[1].set_title("DTI vs DTC by Risk Tier", fontsize=12)
axes[1].set_xlabel("Debt-to-Income (DTI)")
axes[1].set_ylabel("Debt-to-Capital (DTC)")
axes[1].legend(fontsize=9)

plt.suptitle("Meridian Business Intelligence - Credit Risk Scoring",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/risk_distribution.png", dpi=150)
plt.close()
print("  Risk distribution chart saved.")

risk_summary = df.groupby('risk_tier').agg(
    client_count  = ('client_id', 'count'),
    avg_dti       = ('dti',       'mean'),
    avg_dtc       = ('dtc',       'mean'),
    total_aum_usd = ('aum_usd',   'sum'),
).round(4)
print("\n  Credit Risk Summary:")
print(risk_summary.to_string())

# ══════════════════════════════════════════════════════════════
# AUM FORECASTING
# ══════════════════════════════════════════════════════════════
print("\nRunning AUM forecasting...")

monthly['month_dt'] = pd.to_datetime(monthly['month'].astype(str))
monthly_sorted = monthly.sort_values('month_dt').reset_index(drop=True)
monthly_sorted['cumulative_aum'] = monthly_sorted['net_flow'].cumsum()
monthly_sorted['ma_3m'] = monthly_sorted['cumulative_aum'].rolling(window=3).mean()

monthly_changes    = monthly_sorted['cumulative_aum'].diff().dropna()
avg_monthly_change = monthly_changes.mean()
std_monthly_change = monthly_changes.std()

last_date = monthly_sorted['month_dt'].iloc[-1]
last_aum  = monthly_sorted['cumulative_aum'].iloc[-1]

forecast_months = 6
forecast_dates  = [last_date + timedelta(days=30 * i) for i in range(1, forecast_months + 1)]
forecast_base   = [last_aum + avg_monthly_change * i for i in range(1, forecast_months + 1)]
forecast_upper  = [v + 1.96 * std_monthly_change * np.sqrt(i) for i, v in enumerate(forecast_base, 1)]
forecast_lower  = [v - 1.96 * std_monthly_change * np.sqrt(i) for i, v in enumerate(forecast_base, 1)]

fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(monthly_sorted['month_dt'],
        monthly_sorted['cumulative_aum'] / 1_000_000,
        color=NAVY, linewidth=2, label='Historical AUM')
ax.plot(monthly_sorted['month_dt'],
        monthly_sorted['ma_3m'] / 1_000_000,
        color=GOLD, linewidth=1.5, linestyle='--', label='3-Month Moving Average')
ax.plot(forecast_dates,
        [v / 1_000_000 for v in forecast_base],
        color=NAVY, linewidth=2, linestyle=':', label='6-Month Projection (Base)')
ax.fill_between(forecast_dates,
                [v / 1_000_000 for v in forecast_lower],
                [v / 1_000_000 for v in forecast_upper],
                alpha=0.15, color=NAVY, label='95% Confidence Interval')
ax.axvline(x=last_date, color='gray', linestyle='--', alpha=0.6, label='Projection Start')

ax.set_title("Meridian Business Intelligence\nAUM Trend and 6-Month Projection (USD Millions)",
             fontsize=14, pad=15)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Cumulative Net AUM (USD Millions)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/aum_forecast.png", dpi=150)
plt.close()
print("  AUM forecast chart saved.")

forecast_df = pd.DataFrame({
    'month':          forecast_dates,
    'base_aum_usd':   forecast_base,
    'upper_95_usd':   forecast_upper,
    'lower_95_usd':   forecast_lower,
})
forecast_df.to_csv(f"{OUTPUT_DIR}/forecast_summary.csv", index=False)
print("  Forecast summary saved.")

print(f"\nAll outputs saved to {OUTPUT_DIR}/")
print("Done.")
