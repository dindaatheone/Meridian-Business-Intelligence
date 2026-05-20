# Meridian Business Intelligence
# SQL Analysis Runner
# Replicates all four SQL analysis levels using pandas
# No database required - runs directly against CSV data
#
# Input:  01_raw_data/clients.csv
#         01_raw_data/portfolios.csv
#         01_raw_data/transactions.csv
#
# Output: 03_sql_analysis/outputs/
#         01_exploratory/
#         02_joins_and_aggregations/
#         03_cte_window_functions/
#         04_business_metrics/

import pandas as pd
import numpy as np
import os
from datetime import date

# ── Load Data ─────────────────────────────────────────────────
print("Meridian Business Intelligence - SQL Analysis Runner")
print()

clients      = pd.read_csv("01_raw_data/clients.csv", parse_dates=[
                   'date_of_birth', 'onboarding_date',
                   'last_rebalancing_date', 'exit_date'
               ])
portfolios   = pd.read_csv("01_raw_data/portfolios.csv", parse_dates=[
                   'inception_date', 'last_valuation_date'
               ])
transactions = pd.read_csv("01_raw_data/transactions.csv", parse_dates=[
                   'transaction_date'
               ])

today = pd.Timestamp(date.today())

# Output dirs
DIRS = [
    "03_sql_analysis/outputs/01_exploratory",
    "03_sql_analysis/outputs/02_joins_and_aggregations",
    "03_sql_analysis/outputs/03_cte_window_functions",
    "03_sql_analysis/outputs/04_business_metrics",
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

def save(df, folder, filename):
    path = f"03_sql_analysis/outputs/{folder}/{filename}"
    df.to_csv(path, index=False)
    print(f"  Saved: {path} ({len(df)} rows)")

# ══════════════════════════════════════════════════════════════
# LEVEL 1: EXPLORATORY
# ══════════════════════════════════════════════════════════════
print("Level 1: Exploratory Analysis")

# Client count by tier
tier_dist = (clients.groupby('client_tier')
             .size().reset_index(name='client_count'))
tier_dist['pct_of_total'] = (tier_dist['client_count'] /
                              tier_dist['client_count'].sum() * 100).round(2)
tier_dist = tier_dist.sort_values('client_count', ascending=False)
save(tier_dist, "01_exploratory", "client_count_by_tier.csv")

# Client count by jurisdiction
juris_dist = (clients.groupby('jurisdiction')
              .size().reset_index(name='client_count'))
juris_dist['pct_of_total'] = (juris_dist['client_count'] /
                               juris_dist['client_count'].sum() * 100).round(2)
juris_dist = juris_dist.sort_values('client_count', ascending=False)
save(juris_dist, "01_exploratory", "client_count_by_jurisdiction.csv")

# Active vs inactive
active_dist = (clients.groupby('is_active')
               .size().reset_index(name='client_count'))
save(active_dist, "01_exploratory", "active_vs_inactive.csv")

# AUM statistics
aum_stats = pd.DataFrame([{
    'min_aum':    clients['investable_aum_usd'].min(),
    'max_aum':    clients['investable_aum_usd'].max(),
    'avg_aum':    round(clients['investable_aum_usd'].mean(), 2),
    'median_aum': clients['investable_aum_usd'].median(),
    'stddev_aum': round(clients['investable_aum_usd'].std(), 2),
}])
save(aum_stats, "01_exploratory", "aum_statistics.csv")

# AUM by tier
aum_by_tier = (clients.groupby('client_tier')
               .agg(
                   client_count=('client_id', 'count'),
                   min_aum=('investable_aum_usd', 'min'),
                   max_aum=('investable_aum_usd', 'max'),
                   avg_aum=('investable_aum_usd', 'mean'),
                   total_aum=('investable_aum_usd', 'sum'),
               ).round(2).reset_index()
               .sort_values('total_aum', ascending=False))
save(aum_by_tier, "01_exploratory", "aum_by_tier.csv")

# Orphaned clients (no portfolio)
orphaned = clients[~clients['client_id'].isin(portfolios['client_id'])][
    ['client_id', 'full_name', 'client_tier', 'jurisdiction']
]
save(orphaned, "01_exploratory", "orphaned_clients.csv")

# Portfolio allocation sum check
alloc_cols = ['equity_pct', 'fixed_income_pct', 'alternatives_pct',
              'cash_pct', 'structured_pct', 'private_credit_pct']
portfolios['total_alloc'] = portfolios[alloc_cols].sum(axis=1).round(2)
bad_alloc = portfolios[portfolios['total_alloc'] != 100.00][
    ['portfolio_id', 'client_id', 'total_alloc']
]
save(bad_alloc, "01_exploratory", "portfolio_allocation_drift.csv")

# NULL checks
null_check = pd.DataFrame([{
    'total_clients':   len(clients),
    'has_aum':         clients['investable_aum_usd'].notna().sum(),
    'has_tier':        clients['client_tier'].notna().sum(),
    'has_jurisdiction':clients['jurisdiction'].notna().sum(),
    'has_currency':    clients['primary_currency'].notna().sum(),
    'has_rm':          clients['assigned_rm'].notna().sum(),
    'has_income':      clients['annual_income_usd'].notna().sum(),
    'has_debt':        clients['total_debt_usd'].notna().sum(),
}])
save(null_check, "01_exploratory", "null_checks.csv")

# Shariah by jurisdiction
shariah = (clients.groupby('jurisdiction')
           .agg(
               total_clients=('client_id', 'count'),
               shariah_clients=('shariah_compliant_flag', 'sum'),
           ).reset_index())
shariah['shariah_pct'] = (shariah['shariah_clients'] /
                          shariah['total_clients'] * 100).round(2)
shariah = shariah.sort_values('shariah_pct', ascending=False)
save(shariah, "01_exploratory", "shariah_by_jurisdiction.csv")

# Co-investment eligible by tier
co_inv = (clients.groupby('client_tier')
          .agg(
              total_clients=('client_id', 'count'),
              eligible_clients=('co_investment_eligible_flag', 'sum'),
          ).reset_index())
co_inv['eligible_pct'] = (co_inv['eligible_clients'] /
                           co_inv['total_clients'] * 100).round(2)
save(co_inv, "01_exploratory", "co_investment_eligible_by_tier.csv")

# ══════════════════════════════════════════════════════════════
# LEVEL 2: JOINS AND AGGREGATIONS
# ══════════════════════════════════════════════════════════════
print("\nLevel 2: JOINs and Aggregations")

cp  = clients.merge(portfolios, on='client_id')
cpt = cp.merge(transactions, on=['client_id', 'portfolio_id'])

# Client financial footprint
footprint = (cpt.groupby(
    ['client_id', 'full_name', 'client_tier', 'jurisdiction', 'assigned_rm']
).agg(
    total_aum_usd=('aum_usd', 'sum'),
    transaction_count=('transaction_id', 'count'),
    total_inflows_usd=('amount_usd', lambda x:
        x[cpt.loc[x.index, 'transaction_type'] == 'Inflow'].sum()),
    total_outflows_usd=('amount_usd', lambda x:
        abs(x[cpt.loc[x.index, 'transaction_type'] == 'Outflow'].sum())),
    total_fees_usd=('fee_amount_usd', lambda x:
        x[cpt.loc[x.index, 'transaction_type'] == 'Fee'].sum()),
).round(2).reset_index()
.sort_values('total_aum_usd', ascending=False))
save(footprint, "02_joins_and_aggregations", "client_footprint.csv")

# RM productivity
active_cp = cp[cp['is_active'] == True]
rm_prod = (active_cp.groupby('assigned_rm')
           .agg(
               client_count=('client_id', 'nunique'),
               total_aum_usd=('aum_usd', 'sum'),
               avg_aum_per_client=('aum_usd', 'mean'),
           ).round(2).reset_index()
           .sort_values('total_aum_usd', ascending=False))
rm_prod['aum_per_client'] = (rm_prod['total_aum_usd'] /
                              rm_prod['client_count']).round(2)
save(rm_prod, "02_joins_and_aggregations", "rm_productivity.csv")

# Corridor flow analysis
corridor = (cpt.groupby('jurisdiction')
            .agg(
                client_count=('client_id', 'nunique'),
                total_aum_usd=('aum_usd', 'sum'),
                total_inflows=('amount_usd', lambda x:
                    x[cpt.loc[x.index, 'transaction_type'] == 'Inflow'].sum()),
                total_outflows=('amount_usd', lambda x:
                    abs(x[cpt.loc[x.index, 'transaction_type'] == 'Outflow'].sum())),
            ).round(2).reset_index())
corridor['net_flow'] = (corridor['total_inflows'] -
                        corridor['total_outflows']).round(2)
corridor = corridor.sort_values('total_aum_usd', ascending=False)
save(corridor, "02_joins_and_aggregations", "corridor_flow.csv")

# Mandate distribution
mandate_dist = (cp.groupby(['client_tier', 'mandate_type'])
                .agg(
                    client_count=('client_id', 'nunique'),
                    total_aum_usd=('aum_usd', 'sum'),
                ).round(2).reset_index()
                .sort_values(['client_tier', 'total_aum_usd'], ascending=[True, False]))
save(mandate_dist, "02_joins_and_aggregations", "mandate_distribution.csv")

# Shariah AUM
total_aum = cp['aum_usd'].sum()
shariah_aum = cp[cp['shariah_compliant_flag'] == True]['aum_usd'].sum()
shariah_pct = pd.DataFrame([{
    'shariah_aum':     round(shariah_aum, 2),
    'total_aum':       round(total_aum, 2),
    'shariah_aum_pct': round(shariah_aum / total_aum * 100, 2),
}])
save(shariah_pct, "02_joins_and_aggregations", "shariah_aum_pct.csv")

# FX exposure
fx_exp = (transactions.groupby('original_currency')
          .agg(
              transaction_count=('transaction_id', 'count'),
              total_volume_usd=('amount_usd', lambda x: abs(x).sum()),
              avg_transaction_usd=('amount_usd', lambda x: abs(x).mean()),
          ).round(2).reset_index()
          .sort_values('total_volume_usd', ascending=False))
fx_exp['pct_of_total'] = (fx_exp['total_volume_usd'] /
                           fx_exp['total_volume_usd'].sum() * 100).round(2)
save(fx_exp, "02_joins_and_aggregations", "fx_exposure.csv")

# ══════════════════════════════════════════════════════════════
# LEVEL 3: CTEs AND WINDOW FUNCTIONS
# ══════════════════════════════════════════════════════════════
print("\nLevel 3: CTEs and Window Functions")

# Client AUM ranking
client_aum = (cp.groupby(
    ['client_id', 'full_name', 'client_tier', 'jurisdiction', 'assigned_rm']
)['aum_usd'].sum().reset_index(name='total_aum'))

client_aum['rank_within_tier'] = (client_aum.groupby('client_tier')['total_aum']
                                   .rank(method='min', ascending=False)
                                   .astype(int))
client_aum['rank_overall']     = (client_aum['total_aum']
                                   .rank(method='min', ascending=False)
                                   .astype(int))
client_aum['pct_of_total_book'] = (client_aum['total_aum'] /
                                    client_aum['total_aum'].sum() * 100).round(4)
client_aum['total_aum'] = client_aum['total_aum'].round(2)
client_aum = client_aum.sort_values('rank_overall')
save(client_aum, "03_cte_window_functions", "client_aum_ranking.csv")

# Month-over-month flows
transactions['month'] = transactions['transaction_date'].dt.to_period('M')
monthly = (transactions.groupby('month')
           .apply(lambda x: pd.Series({
               'inflows':  x.loc[x['transaction_type'] == 'Inflow', 'amount_usd'].sum(),
               'outflows': abs(x.loc[x['transaction_type'] == 'Outflow', 'amount_usd'].sum()),
           })).reset_index())
monthly['net_flow'] = monthly['inflows'] - monthly['outflows']
monthly['prev_month_net_flow'] = monthly['net_flow'].shift(1)
monthly['mom_change_pct'] = ((monthly['net_flow'] - monthly['prev_month_net_flow']) /
                              monthly['prev_month_net_flow'].abs() * 100).round(2)
monthly = monthly.round(2)
save(monthly, "03_cte_window_functions", "monthly_flows.csv")

# Rolling 3-month average
monthly['rolling_3m_avg'] = (monthly['net_flow']
                              .rolling(3, min_periods=1)
                              .mean().round(2))
rolling = monthly[['month', 'net_flow', 'rolling_3m_avg']]
save(rolling, "03_cte_window_functions", "rolling_3m_avg.csv")

# AUM decile distribution
client_aum_dec = (cp.groupby('client_id')['aum_usd']
                  .sum().reset_index(name='total_aum')
                  .sort_values('total_aum', ascending=False))
client_aum_dec['decile'] = pd.qcut(
    client_aum_dec['total_aum'].rank(method='first', ascending=False),
    q=10, labels=range(1, 11)
).astype(int)
decile_dist = (client_aum_dec.groupby('decile')
               .agg(
                   client_count=('client_id', 'count'),
                   decile_aum=('total_aum', 'sum'),
               ).reset_index())
decile_dist['pct_of_total_aum'] = (decile_dist['decile_aum'] /
                                    decile_dist['decile_aum'].sum() * 100).round(2)
decile_dist['decile_aum'] = decile_dist['decile_aum'].round(2)
save(decile_dist, "03_cte_window_functions", "aum_decile_distribution.csv")

# Cumulative inflows per client
inflows = cpt[cpt['transaction_type'] == 'Inflow'].copy()
inflows = inflows.sort_values(['client_id', 'transaction_date'])
inflows['cumulative_inflows'] = (inflows.groupby('client_id')['amount_usd']
                                  .cumsum().round(2))
cum_inflows = inflows[['client_id', 'full_name', 'client_tier',
                        'transaction_date', 'amount_usd', 'cumulative_inflows']]
save(cum_inflows, "03_cte_window_functions", "cumulative_inflows.csv")

# ══════════════════════════════════════════════════════════════
# LEVEL 4: BUSINESS METRICS
# ══════════════════════════════════════════════════════════════
print("\nLevel 4: Business Metrics")

# Metric 1: AUM growth rate
monthly_sorted = monthly.sort_values('month')
cumulative_aum = monthly_sorted['net_flow'].cumsum()
aum_start = cumulative_aum.iloc[0]
aum_end   = cumulative_aum.iloc[-1]
growth_rate = round((aum_end - aum_start) / abs(aum_start) * 100, 2) if aum_start != 0 else 0
aum_growth = pd.DataFrame([{
    'aum_start':          round(aum_start, 2),
    'aum_end':            round(aum_end, 2),
    'aum_growth_rate_pct': growth_rate,
}])
save(aum_growth, "04_business_metrics", "aum_growth_rate.csv")

# Metric 2: Concentration risk
client_aum_conc = (cp.groupby('client_id')['aum_usd']
                   .sum().reset_index(name='total_aum')
                   .sort_values('total_aum', ascending=False))
client_aum_conc['decile'] = pd.qcut(
    client_aum_conc['total_aum'].rank(method='first', ascending=False),
    q=10, labels=range(1, 11)
).astype(int)
top10_aum   = client_aum_conc[client_aum_conc['decile'] == 1]['total_aum'].sum()
total_aum_c = client_aum_conc['total_aum'].sum()
conc_pct    = round(top10_aum / total_aum_c * 100, 2)
concentration = pd.DataFrame([{
    'top_10pct_concentration': conc_pct,
    'risk_assessment': ('ELEVATED - revenue fragility risk'
                        if conc_pct > 40 else 'ACCEPTABLE - within threshold'),
}])
save(concentration, "04_business_metrics", "concentration_risk.csv")

# Metric 3: Churn detection
last_inflow = (cpt[cpt['transaction_type'] == 'Inflow']
               .groupby('client_id')['transaction_date']
               .max().reset_index(name='last_inflow_date'))
active_clients = clients[clients['is_active'] == True]
churn = active_clients.merge(last_inflow, on='client_id')
churn['days_since_inflow'] = (today - churn['last_inflow_date']).dt.days
churn_risk = churn[churn['days_since_inflow'] > 180].copy()
aum_per_client = cp.groupby('client_id')['aum_usd'].sum().reset_index(name='current_aum_usd')
churn_risk = (churn_risk.merge(aum_per_client, on='client_id')
              [['client_id', 'full_name', 'client_tier', 'jurisdiction',
                'assigned_rm', 'last_inflow_date', 'days_since_inflow', 'current_aum_usd']]
              .sort_values('days_since_inflow', ascending=False))
save(churn_risk, "04_business_metrics", "churn_detection.csv")

# Metric 4: Client lifetime value
fee_revenue = (cpt[cpt['transaction_type'] == 'Fee']
               .groupby('client_id')['fee_amount_usd']
               .sum().abs().reset_index(name='total_fees_collected'))
tenure = clients[['client_id', 'onboarding_date', 'exit_date']].copy()
tenure['end_date'] = tenure['exit_date'].fillna(today)
tenure['relationship_years'] = ((tenure['end_date'] - tenure['onboarding_date'])
                                 .dt.days / 365).round(1)
clv = (clients[['client_id', 'full_name', 'client_tier', 'jurisdiction']]
       .merge(fee_revenue, on='client_id')
       .merge(tenure[['client_id', 'relationship_years']], on='client_id'))
clv['avg_annual_fee_usd']  = (clv['total_fees_collected'] /
                               clv['relationship_years'].replace(0, np.nan)).round(2)
clv['estimated_10yr_clv']  = (clv['avg_annual_fee_usd'] * 10).round(2)
clv['total_fees_collected'] = clv['total_fees_collected'].round(2)
clv = clv.sort_values('estimated_10yr_clv', ascending=False)
save(clv, "04_business_metrics", "client_lifetime_value.csv")

# Metric 5: Fee revenue decomposition
fee_txns = transactions[(transactions['transaction_type'] == 'Fee') &
                         (transactions['fee_type'].notna())]
fee_decomp = (fee_txns.groupby('fee_type')
              .agg(
                  transaction_count=('transaction_id', 'count'),
                  total_fee_revenue=('fee_amount_usd', lambda x: abs(x).sum()),
                  avg_fee_per_transaction=('fee_amount_usd', lambda x: abs(x).mean()),
              ).round(2).reset_index())
fee_decomp['pct_of_total_fees'] = (fee_decomp['total_fee_revenue'] /
                                    fee_decomp['total_fee_revenue'].sum() * 100).round(2)
fee_decomp = fee_decomp.sort_values('total_fee_revenue', ascending=False)
save(fee_decomp, "04_business_metrics", "fee_revenue_decomposition.csv")

# Metric 6: FX exposure by corridor
fx_corridor = (cpt[cpt['original_currency'].notna() &
                   (cpt['original_currency'] != 'USD')]
               .groupby(['jurisdiction', 'original_currency'])
               .agg(
                   transaction_count=('transaction_id', 'count'),
                   total_exposure_usd=('amount_usd', lambda x: abs(x).sum()),
               ).round(2).reset_index())
fx_corridor['pct_of_total_exposure'] = (
    fx_corridor['total_exposure_usd'] /
    fx_corridor['total_exposure_usd'].sum() * 100
).round(2)
fx_corridor = fx_corridor.sort_values('total_exposure_usd', ascending=False)
save(fx_corridor, "04_business_metrics", "fx_exposure_by_corridor.csv")

print(f"\nAll outputs saved to 03_sql_analysis/outputs/")
print("Done.")
