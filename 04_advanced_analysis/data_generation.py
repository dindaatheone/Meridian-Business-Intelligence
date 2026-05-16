# Meridian Business Intelligence
# Synthetic Data Generator
# Generates clients.csv, portfolios.csv, transactions.csv
# from the immutable data spine schema - Guidebook v1.0
#
# Run this script first before any database or analysis work.
# Output: ../01_raw_data/clients.csv
#         ../01_raw_data/portfolios.csv
#         ../01_raw_data/transactions.csv

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# ── Configuration ─────────────────────────────────────────────
RANDOM_SEED     = 42
NUM_CLIENTS     = 750
MONTHS          = 24
OUTPUT_DIR      = "../01_raw_data"

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
fake = Faker(['zh_CN', 'en_SG', 'id_ID'])

# ── Reference Data ────────────────────────────────────────────
JURISDICTIONS = {
    'China':        0.40,
    'Singapore':    0.25,
    'Indonesia':    0.20,
    'Macau':        0.10,
    'Brunei':       0.05,
}

TIERS = {
    'HNW':   {'weight': 0.50, 'aum_min': 1_000_000,   'aum_max': 5_000_000},
    'VHNW':  {'weight': 0.35, 'aum_min': 5_000_000,   'aum_max': 30_000_000},
    'UHNW':  {'weight': 0.15, 'aum_min': 30_000_000,  'aum_max': 150_000_000},
}

CURRENCIES = {
    'China':        'CNY',
    'Singapore':    'SGD',
    'Indonesia':    'IDR',
    'Macau':        'USD',
    'Brunei':       'BND',
}

MANDATES = ['Discretionary', 'Advisory', 'Execution-Only']
RISK_PROFILES = ['Conservative', 'Moderate', 'Aggressive']

TRANSACTION_TYPES = [
    'Inflow', 'Outflow', 'Fee',
    'Dividend', 'Interest', 'Rebalance', 'FX-Conversion'
]

ASSET_CLASSES = [
    'Equities', 'Fixed Income', 'Alternatives',
    'Cash', 'Structured Products', 'Private Credit'
]

FEE_TYPES = [
    'Management Fee', 'Performance Fee',
    'Advisory Fee', 'Transaction Fee'
]

RMS = [f"RM_{str(i).zfill(3)}" for i in range(1, 16)]

START_DATE = datetime(2024, 1, 1)


# ── Client Generation ─────────────────────────────────────────
def generate_clients(n):
    jurisdictions   = list(JURISDICTIONS.keys())
    j_weights       = list(JURISDICTIONS.values())
    tier_names      = list(TIERS.keys())
    t_weights       = [TIERS[t]['weight'] for t in tier_names]

    records = []
    for i in range(1, n + 1):
        jurisdiction    = random.choices(jurisdictions, weights=j_weights)[0]
        tier            = random.choices(tier_names, weights=t_weights)[0]
        aum             = round(np.random.uniform(
                            TIERS[tier]['aum_min'],
                            TIERS[tier]['aum_max']
                          ), 2)
        income          = round(aum * np.random.uniform(0.05, 0.20), 2)
        debt            = round(income * np.random.uniform(0.10, 0.65), 2)
        onboarding      = START_DATE - timedelta(
                            days=random.randint(30, 900)
                          )
        tenure_months   = round(
                            (datetime.now() - onboarding).days / 30
                          )
        shariah         = jurisdiction in ('Indonesia', 'Brunei') \
                          and random.random() < 0.25
        co_invest       = tier in ('VHNW', 'UHNW')
        is_active       = random.random() > 0.06
        exit_date       = None
        if not is_active:
            exit_date   = (onboarding + timedelta(
                            days=random.randint(180, 800)
                          )).strftime('%Y-%m-%d')

        records.append({
            'client_id':                    i,
            'full_name':                    fake.name(),
            'jurisdiction':                 jurisdiction,
            'date_of_birth':                fake.date_of_birth(
                                                minimum_age=30,
                                                maximum_age=80
                                            ).strftime('%Y-%m-%d'),
            'onboarding_date':              onboarding.strftime('%Y-%m-%d'),
            'client_tier':                  tier,
            'investable_aum_usd':           aum,
            'primary_currency':             CURRENCIES[jurisdiction],
            'product_mandate_type':         random.choice(MANDATES),
            'risk_appetite':                random.choice(RISK_PROFILES),
            'shariah_compliant_flag':       shariah,
            'relationship_tenure_months':   tenure_months,
            'assigned_rm':                  random.choice(RMS),
            'co_investment_eligible_flag':  co_invest,
            'last_rebalancing_date':        (START_DATE + timedelta(
                                                days=random.randint(0, 600)
                                            )).strftime('%Y-%m-%d'),
            'annual_income_usd':            income,
            'total_debt_usd':               debt,
            'is_active':                    is_active,
            'exit_date':                    exit_date,
        })

    return pd.DataFrame(records)


# ── Portfolio Generation ──────────────────────────────────────
def generate_portfolios(clients_df):
    records = []
    for _, client in clients_df.iterrows():
        allocs = np.random.dirichlet(
            np.ones(6), size=1
        )[0] * 100
        allocs = np.round(allocs, 2)
        allocs[-1] = round(100 - allocs[:-1].sum(), 2)

        records.append({
            'portfolio_id':             client['client_id'],
            'client_id':                client['client_id'],
            'portfolio_name':           f"MPB-{client['client_id']:05d}",
            'inception_date':           client['onboarding_date'],
            'base_currency':            'USD',
            'mandate_type':             client['product_mandate_type'],
            'aum_usd':                  client['investable_aum_usd'],
            'equity_pct':               allocs[0],
            'fixed_income_pct':         allocs[1],
            'alternatives_pct':         allocs[2],
            'cash_pct':                 allocs[3],
            'structured_pct':           allocs[4],
            'private_credit_pct':       allocs[5],
            'benchmark':                'MSCI AC Asia Pacific',
            'performance_ytd':          round(
                                            np.random.normal(0.06, 0.08), 4
                                        ),
            'performance_inception':    round(
                                            np.random.normal(0.12, 0.15), 4
                                        ),
            'last_valuation_date':      (START_DATE + timedelta(
                                            days=random.randint(500, 700)
                                        )).strftime('%Y-%m-%d'),
        })

    return pd.DataFrame(records)


# ── Transaction Generation ────────────────────────────────────
def generate_transactions(clients_df, portfolios_df):
    records = []
    txn_id = 1

    fx_rates = {
        'CNY': 7.24, 'SGD': 1.34, 'IDR': 15800,
        'USD': 1.00, 'BND': 1.34
    }

    for _, client in clients_df.iterrows():
        portfolio = portfolios_df[
            portfolios_df['client_id'] == client['client_id']
        ].iloc[0]
        currency = client['primary_currency']
        aum      = client['investable_aum_usd']

        for month_offset in range(MONTHS):
            txn_date = START_DATE + timedelta(days=month_offset * 30)

            # Monthly fee
            fee_amount = round(aum * 0.01 / 12, 2)
            records.append({
                'transaction_id':       txn_id,
                'client_id':            client['client_id'],
                'portfolio_id':         portfolio['portfolio_id'],
                'transaction_date':     txn_date.strftime('%Y-%m-%d'),
                'transaction_type':     'Fee',
                'amount_usd':           -fee_amount,
                'original_currency':    currency,
                'fx_rate_applied':      fx_rates.get(currency, 1.0),
                'asset_class':          'Cash',
                'fee_amount_usd':       fee_amount,
                'fee_type':             'Management Fee',
                'rm_id':                client['assigned_rm'],
                'notes':                'Monthly management fee',
            })
            txn_id += 1

            # Occasional inflow
            if random.random() < 0.30:
                inflow = round(aum * np.random.uniform(0.01, 0.08), 2)
                records.append({
                    'transaction_id':       txn_id,
                    'client_id':            client['client_id'],
                    'portfolio_id':         portfolio['portfolio_id'],
                    'transaction_date':     txn_date.strftime('%Y-%m-%d'),
                    'transaction_type':     'Inflow',
                    'amount_usd':           inflow,
                    'original_currency':    currency,
                    'fx_rate_applied':      fx_rates.get(currency, 1.0),
                    'asset_class':          random.choice(ASSET_CLASSES),
                    'fee_amount_usd':       0,
                    'fee_type':             None,
                    'rm_id':                client['assigned_rm'],
                    'notes':                None,
                })
                txn_id += 1

            # Occasional outflow
            if random.random() < 0.15:
                outflow = round(aum * np.random.uniform(0.005, 0.04), 2)
                records.append({
                    'transaction_id':       txn_id,
                    'client_id':            client['client_id'],
                    'portfolio_id':         portfolio['portfolio_id'],
                    'transaction_date':     txn_date.strftime('%Y-%m-%d'),
                    'transaction_type':     'Outflow',
                    'amount_usd':           -outflow,
                    'original_currency':    currency,
                    'fx_rate_applied':      fx_rates.get(currency, 1.0),
                    'asset_class':          random.choice(ASSET_CLASSES),
                    'fee_amount_usd':       0,
                    'fee_type':             None,
                    'rm_id':                client['assigned_rm'],
                    'notes':                None,
                })
                txn_id += 1

            # Quarterly dividend
            if month_offset % 3 == 0:
                dividend = round(aum * np.random.uniform(0.003, 0.008), 2)
                records.append({
                    'transaction_id':       txn_id,
                    'client_id':            client['client_id'],
                    'portfolio_id':         portfolio['portfolio_id'],
                    'transaction_date':     txn_date.strftime('%Y-%m-%d'),
                    'transaction_type':     'Dividend',
                    'amount_usd':           dividend,
                    'original_currency':    currency,
                    'fx_rate_applied':      fx_rates.get(currency, 1.0),
                    'asset_class':          'Equities',
                    'fee_amount_usd':       0,
                    'fee_type':             None,
                    'rm_id':                client['assigned_rm'],
                    'notes':                None,
                })
                txn_id += 1

    return pd.DataFrame(records)


# ── Main ──────────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating clients...")
    clients_df = generate_clients(NUM_CLIENTS)
    clients_df.to_csv(
        f"{OUTPUT_DIR}/clients.csv", index=False
    )
    print(f"  {len(clients_df)} clients generated")

    print("Generating portfolios...")
    portfolios_df = generate_portfolios(clients_df)
    portfolios_df.to_csv(
        f"{OUTPUT_DIR}/portfolios.csv", index=False
    )
    print(f"  {len(portfolios_df)} portfolios generated")

    print("Generating transactions...")
    transactions_df = generate_transactions(clients_df, portfolios_df)
    transactions_df.to_csv(
        f"{OUTPUT_DIR}/transactions.csv", index=False
    )
    print(f"  {len(transactions_df)} transactions generated")

    print("\nDone. Output written to ../01_raw_data/")
    print(f"  clients.csv:      {len(clients_df)} rows")
    print(f"  portfolios.csv:   {len(portfolios_df)} rows")
    print(f"  transactions.csv: {len(transactions_df)} rows")