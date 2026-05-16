# Meridian Business Intelligence
# AUM Forecasting Model
# 24-month historical AUM trend from transaction data
# Moving average projection with confidence interval bounds
#
# Input:  PostgreSQL meridian_bi database
# Output: outputs/aum_forecast.png
#         outputs/forecast_summary.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import os
from datetime import datetime, timedelta

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

# ── Load Monthly Net Flows ────────────────────────────────────
flows_df = pd.read_sql("""
    SELECT
        DATE_TRUNC('month', transaction_date)   AS month,
        SUM(CASE
            WHEN transaction_type = 'Inflow'
            THEN amount_usd ELSE 0
        END) -
        SUM(CASE
            WHEN transaction_type = 'Outflow'
            THEN ABS(amount_usd) ELSE 0
        END)                                    AS net_flow
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date)
    ORDER BY month
""", conn)

flows_df['month'] = pd.to_datetime(flows_df['month'])
flows_df['cumulative_aum'] = flows_df['net_flow'].cumsum()

# ── Moving Average and Trend ──────────────────────────────────
flows_df['ma_3m'] = flows_df['cumulative_aum'].rolling(window=3).mean()

monthly_changes = flows_df['cumulative_aum'].diff().dropna()
avg_monthly_change = monthly_changes.mean()
std_monthly_change = monthly_changes.std()

# ── 6-Month Projection ────────────────────────────────────────
last_date   = flows_df['month'].iloc[-1]
last_aum    = flows_df['cumulative_aum'].iloc[-1]

forecast_months = 6
forecast_dates  = [
    last_date + timedelta(days=30 * i)
    for i in range(1, forecast_months + 1)
]
forecast_base   = [
    last_aum + avg_monthly_change * i
    for i in range(1, forecast_months + 1)
]
forecast_upper  = [
    v + 1.96 * std_monthly_change * np.sqrt(i)
    for i, v in enumerate(forecast_base, 1)
]
forecast_lower  = [
    v - 1.96 * std_monthly_change * np.sqrt(i)
    for i, v in enumerate(forecast_base, 1)
]

# ── Chart ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(
    flows_df['month'],
    flows_df['cumulative_aum'] / 1_000_000,
    color     = '#1E3A5F',
    linewidth = 2,
    label     = 'Historical AUM'
)
ax.plot(
    flows_df['month'],
    flows_df['ma_3m'] / 1_000_000,
    color     = '#B8962E',
    linewidth = 1.5,
    linestyle = '--',
    label     = '3-Month Moving Average'
)
ax.plot(
    forecast_dates,
    [v / 1_000_000 for v in forecast_base],
    color     = '#1E3A5F',
    linewidth = 2,
    linestyle = ':',
    label     = '6-Month Projection (Base)'
)
ax.fill_between(
    forecast_dates,
    [v / 1_000_000 for v in forecast_lower],
    [v / 1_000_000 for v in forecast_upper],
    alpha     = 0.15,
    color     = '#1E3A5F',
    label     = '95% Confidence Interval'
)

ax.axvline(
    x         = last_date,
    color     = 'gray',
    linestyle = '--',
    alpha     = 0.6,
    label     = 'Projection Start'
)

ax.set_title(
    "Meridian Business Intelligence\nAUM Trend and 6-Month Projection (USD Millions)",
    fontsize  = 14,
    pad       = 15
)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Cumulative Net AUM (USD Millions)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/aum_forecast.png", dpi=150)
plt.close()
print("AUM forecast chart saved.")

# ── Forecast Summary CSV ──────────────────────────────────────
forecast_df = pd.DataFrame({
    'month':            forecast_dates,
    'base_aum_usd':     forecast_base,
    'upper_95_usd':     forecast_upper,
    'lower_95_usd':     forecast_lower,
})
forecast_df.to_csv(
    f"{OUTPUT_DIR}/forecast_summary.csv", index=False
)
print("Forecast summary saved.")

conn.close()
print("\nForecasting model complete. Outputs in outputs/")